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
      history: history.reverse().map((m) => ({
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

  res.json({
    user_message: msg,
    agent_message: agentMsg,
    coordinator_meta: coordinatorResponse,
  });
});

export default router;
