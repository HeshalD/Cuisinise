import { useEffect, useState } from "react";
import axios from "../utils/api";
import { FiTrash2 } from "react-icons/fi";

export default function ChatListSidebar({ onSelectChat, selectedChatId }) {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    axios.get("/chats").then(res => setChats(res.data));
  }, []);

  const handleDelete = async (e, chatId) => {
    e.stopPropagation();
    try {
      const confirmed = window.confirm("Are you sure you want to remove this chat?");
      if (!confirmed) return;
      await axios.delete(`/chats/${chatId}`);
      setChats(prev => prev.filter(c => c._id !== chatId));
      if (selectedChatId === chatId) {
        onSelectChat(null);
      }
    } catch (err) {
      console.error("Failed to delete chat", err);
    }
  };

  return (
    <div className="w-64 bg-gray-700 text-white h-screen overflow-y-auto pt-[20px]">
      <button
        className="w-full p-3 text-left hover:bg-[#7a9b9e] hover:rounded-[10px]"
        onClick={() => onSelectChat(null)} // new chat
      >
        + New Chat
      </button>

      {chats.map(chat => (
        <div
          key={chat._id}
          onClick={() => onSelectChat(chat)}
          className={`group p-3 cursor-pointer mb-[10px] hover:bg-[#7a9b9e] transition-colors duration-250 ease-in-out hover:rounded-[10px]  ${
            selectedChatId === chat._id ? "bg-[#7a9b9e] hover:rounded-[10px] rounded-[10px]" : ""
          }`}
        >
          <div className="flex items-center justify-between gap-2">
            <span className="truncate">{chat.title || "Untitled Chat"}</span>
            <button
              className="opacity-0 group-hover:opacity-100 transition-opacity duration-150 text-red-300 hover:text-red-200 p-1 rounded hover:bg-red-600/30"
              onClick={(e) => handleDelete(e, chat._id)}
              aria-label="Remove chat"
              title="Remove"
            >
              <FiTrash2 size={16} />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
