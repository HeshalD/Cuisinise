import { useState } from "react";
import ChatListSidebar from "./ChatListSidebar";
import ChatWindow from "./ChatWindow";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function ChatDashboard() {
  const [selectedChat, setSelectedChat] = useState(null);
  const [profileOpen, setProfileOpen] = useState(false);
  const { user, logout } = useContext(AuthContext);

  const handleChatCreated = (newChat) => {
    setSelectedChat(newChat);
  };

  return (
    <div className="bg-gray-700">
    <Header/>
    <div className="flex h-screen relative">
      <ChatListSidebar
        onSelectChat={setSelectedChat}
        selectedChatId={selectedChat?._id}
      />
      <ChatWindow chat={selectedChat} onChatCreated={handleChatCreated} />
    </div>
    <Footer/>
    </div>
  );
}
