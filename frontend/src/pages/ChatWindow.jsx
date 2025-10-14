import { useEffect, useState, useRef } from "react";
import axios from "../utils/api";
import ChatMessage from "../components/ChatMessage";
import ChatInput from "../components/ChatInput";
import Loader from "../components/Loader";

export default function ChatWindow({ chat, onChatCreated }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (chat?._id) {
      axios.get(`/chats/${chat._id}/messages`).then(res => setMessages(res.data));
    } else {
      setMessages([]);
    }
  }, [chat]);

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    setLoading(true);
    
    try {
      let chatId = chat?._id;
      
      // If no chat exists, create a new one first
      if (!chatId) {
        const newChatResponse = await axios.post("/chats");
        chatId = newChatResponse.data._id;
        onChatCreated(newChatResponse.data);
      }
      
      const res = await axios.post(`/chats/${chatId}/messages`, { text });
      const { user_message, agent_message } = res.data;
      setMessages(prev => [...prev, user_message, agent_message]);
    } catch (error) {
      console.error("Error sending message:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Greeting message for new chat
  const greetingMessage = {
    _id: "greeting",
    role: "agent",
    text: "👋 Hi! I'm your food exploration assistant. I can help you discover recipes, find restaurants, analyze menus, and much more! What would you like to explore today?",
    createdAt: new Date()
  };

  return (
    <div className="flex flex-col flex-1 h-screen bg-[#d4ebe0]">
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {!chat && (
          <ChatMessage key="greeting" msg={greetingMessage} />
        )}
        {messages.map((msg) => (
          <ChatMessage key={msg._id} msg={msg} />
        ))}
        {loading && <Loader />}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSend={sendMessage} disabled={loading} />
    </div>
  );
}
