import { useState } from "react";

export default function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSend(text);
    setText("");
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 mb-[20px] bg-[#d4ebe0] border-t border-[#d4ebe0] border-b flex">
      <input
        type="text"
        value={text}
        disabled={disabled}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your question..."
        className="flex-1 border rounded-xl px-4 py-2 outline-none"
      />
      <button
        type="submit"
        disabled={disabled}
        className="ml-2 px-4 py-2 bg-green-400 text-white rounded-xl"
      >
        Send
      </button>
    </form>
  );
}
