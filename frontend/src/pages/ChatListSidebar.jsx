import { useEffect, useState } from "react";
import axios from "../utils/api";

export default function ChatListSidebar({ onSelectChat, selectedChatId }) {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    axios.get("/chats").then(res => setChats(res.data));
  }, []);

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
          className={`p-3 cursor-pointer mb-[10px] hover:bg-[#7a9b9e] transition-colors duration-250 ease-in-out hover:rounded-[10px]  ${
            selectedChatId === chat._id ? "bg-[#7a9b9e] hover:rounded-[10px] rounded-[10px]" : ""
          }`}
        >
          {chat.title || "Untitled Chat"}
        </div>
      ))}
    </div>
  );
}
