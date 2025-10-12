import express from "express";
import axios from "axios";
import Chat from "../models/Chat.js";
import Message from "../models/Message.js";
import { auth } from "../middleware/auth.js";

const router = express.Router();
const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";

// Create new chat
router.post("/", auth, async (req, res) => {
  const chat = await Chat.create({ userId: req.userId });
  res.json(chat);
});

// Get all chats for user
router.get("/", auth, async (req, res) => {
  const chats = await Chat.find({ userId: req.userId }).sort({
    lastActivityAt: -1,
  });
  res.json(chats);
});

// Get messages for chat
router.get("/:chatId/messages", auth, async (req, res) => {
  const messages = await Message.find({ chatId: req.params.chatId }).sort({
    createdAt: 1,
  });
  res.json(messages);
});

// Update chat summary manually
router.post("/:chatId/summary", auth, async (req, res) => {
  try {
    await updateChatSummary(req.params.chatId);
    const chat = await Chat.findById(req.params.chatId);
    res.json({ 
      success: true, 
      summary: chat.summary,
      message: "Chat summary updated successfully" 
    });
  } catch (error) {
    console.error("Failed to update chat summary:", error);
    res.status(500).json({ 
      success: false, 
      error: "Failed to update chat summary" 
    });
  }
});

// Get chat summary
router.get("/:chatId/summary", auth, async (req, res) => {
  try {
    const chat = await Chat.findById(req.params.chatId);
    if (!chat) {
      return res.status(404).json({ error: "Chat not found" });
    }
    res.json({ summary: chat.summary });
  } catch (error) {
    console.error("Failed to get chat summary:", error);
    res.status(500).json({ error: "Failed to get chat summary" });
  }
});

// Post new message (user message)
router.post("/:chatId/messages", auth, async (req, res) => {
  const { text } = req.body;
  const chatId = req.params.chatId;

  const msg = await Message.create({
    chatId: req.params.chatId,
    userId: req.userId,
    role: "user",
    text,
  });

  const chat = await Chat.findById(chatId);
  
  // Generate title for new chats (if title is still "New Chat")
  if (chat.title === "New Chat") {
    try {
      const titleResponse = await axios.post(`${FASTAPI_URL}/generate-title`, {
        query: text,
      });
      const newTitle = titleResponse.data.title;
      await Chat.findByIdAndUpdate(chatId, { title: newTitle });
      chat.title = newTitle; // Update local chat object for response
    } catch (err) {
      console.error("Title generation failed:", err.message);
      // Continue without updating title if generation fails
    }
  }

  let coordinatorResponse;
  try {
    const history = await Message.find({ chatId })
      .sort({ createdAt: -1 })
      .limit(10)
      .lean();

      const payload = {
        query: text,
        user_id: req.userId,
        location: chat.location || "Colombo",
        top_k: 5,
        summary: chat.summary || "",
        history: history.reverse().map(m => ({
          role: m.role,
          text: m.text,
        })),
      };
    const response = await axios.post(`${FASTAPI_URL}/query`, payload);
    coordinatorResponse = response.data;
  } catch (err) {
    console.error("Coordinator error:", err.message);
    coordinatorResponse = {
      results: {
        error: "Coordinator failed to process query.",
      },
    };
  }

  const agentReply =
    coordinatorResponse.results?.formatted_summary ||
    coordinatorResponse.results?.error ||
    "Sorry, something went wrong.";

  const agentMsg = await Message.create({
    chatId,
    role: "agent",
    agentId: "coordinator",
    text: agentReply,
  });

  await Chat.findByIdAndUpdate(chatId, { lastActivityAt: new Date() });

  // Update chat summary after every few messages
  const messageCount = await Message.countDocuments({ chatId });
  if (messageCount % 5 === 0) { // Update summary every 5 messages
    updateChatSummary(chatId).catch(err => 
      console.error("Failed to update chat summary:", err)
    );
  }

  res.json({
    user_message: msg,
    agent_message: agentMsg,
    coordinator_meta: coordinatorResponse,
    chat: chat, // Include updated chat info with new title
  });
});

async function updateChatSummary(chatId) {
  const messages = await Message.find({ chatId })
    .sort({ createdAt: 1 })
    .lean();

  const historyText = messages.map(m => `${m.role}: ${m.text}`).join("\n");

  try {
    const { data } = await axios.post(`${FASTAPI_URL}/summarize`, {
      history: historyText,
    });
    await Chat.findByIdAndUpdate(chatId, { summary: data.summary });
  } catch (err) {
    console.error("Summary update failed:", err.message);
  }
}

export default router;
