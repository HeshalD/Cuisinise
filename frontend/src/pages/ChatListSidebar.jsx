import { useEffect, useState } from "react";
import axios from "../utils/api";

export default function ChatListSidebar({ onSelectChat, selectedChatId }) {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    axios.get("/chats").then(res => setChats(res.data));
  }, []);

  return (
    <div className="w-64 bg-gray-900 text-white h-screen overflow-y-auto border-r border-gray-700">
      <div className="p-4 text-xl font-bold border-b border-gray-700">Food Explorer</div>
      <button
        className="w-full p-3 text-left hover:bg-gray-800"
        onClick={() => onSelectChat(null)} // new chat
      >
        + New Chat
      </button>

      {chats.map(chat => (
        <div
          key={chat._id}
          onClick={() => onSelectChat(chat)}
          className={`p-3 cursor-pointer hover:bg-gray-800 ${
            selectedChatId === chat._id ? "bg-gray-800" : ""
          }`}
        >
          {chat.title || "Untitled Chat"}
        </div>
      ))}
    </div>
  );
}
