import { useState } from "react";
import ChatListSidebar from "./ChatListSidebar";
import ChatWindow from "./ChatWindow";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

export default function ChatDashboard() {
  const [selectedChat, setSelectedChat] = useState(null);
  const [profileOpen, setProfileOpen] = useState(false);
  const { user, logout } = useContext(AuthContext);

  const handleChatCreated = (newChat) => {
    setSelectedChat(newChat);
  };

  return (
    <div className="flex h-screen relative">
      <div className="fixed top-3 left-3 z-50">
        <button
          onClick={() => setProfileOpen((o) => !o)}
          className="flex items-center gap-2 px-2 py-1 rounded-full bg-white shadow border hover:bg-gray-50"
        >
          <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-gray-200 text-gray-700 text-sm font-semibold">
            {(user?.name || user?.email || "U").toString().trim().charAt(0).toUpperCase()}
          </span>
          <span className="text-sm text-gray-800 max-w-[140px] truncate">
            {user?.name || user?.email || "User"}
          </span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-gray-600">
            <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.24 4.5a.75.75 0 01-1.08 0l-4.24-4.5a.75.75 0 01.02-1.06z" clipRule="evenodd" />
          </svg>
        </button>

        {profileOpen && (
          <div className="mt-2 w-64 rounded-lg border bg-white shadow-lg p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-700 font-semibold">
                {(user?.name || user?.email || "U").toString().trim().charAt(0).toUpperCase()}
              </div>
              <div className="min-w-0">
                <div className="text-sm font-semibold text-gray-900 truncate">{user?.name || "User"}</div>
                <div className="text-xs text-gray-600 truncate">{user?.email || ""}</div>
              </div>
            </div>
            <div className="space-y-2">
              <a href="#" className="block text-sm text-gray-800 hover:text-blue-600">Profile</a>
              <button
                onClick={() => {
                  setProfileOpen(false);
                  logout();
                  window.location.href = "/";
                }}
                className="w-full text-left text-sm text-red-600 hover:text-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
      <ChatListSidebar
        onSelectChat={setSelectedChat}
        selectedChatId={selectedChat?._id}
      />
      <ChatWindow chat={selectedChat} onChatCreated={handleChatCreated} />
    </div>
  );
}
