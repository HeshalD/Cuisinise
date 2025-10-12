import mongoose from "mongoose";

const MessageSchema = new mongoose.Schema({
  chatId: { type: mongoose.Schema.Types.ObjectId, ref: "Chat", required: true },
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  role: { type: String, enum: ["user", "agent"], required: true },
  agentId: String,
  text: { type: String, required: true },
  createdAt: { type: Date, default: Date.now },
});

export default mongoose.model("Message", MessageSchema);
