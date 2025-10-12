export default function ChatMessage({ msg }) {
    const isUser = msg.role === "user";
    return (
      <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
        <div
          className={`p-3 rounded-2xl max-w-lg ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-900"
          }`}
        >
          {msg.text}
        </div>
      </div>
    );
  }
  