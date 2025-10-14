import express from "express";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import User from "../models/User.js";
import { auth } from "../middleware/auth.js";

const router = express.Router();
const JWT_SECRET = process.env.JWT_SECRET || "supersecret";

router.post("/register", async (req, res) => {
  if (!req.body) return res.status(400).json({ error: "Missing request body" });
  const { name, email, password } = req.body || {};
  if (!name || !email || !password)
    return res.status(400).json({ error: "name, email and password are required" });

  const passwordHash = await bcrypt.hash(password, 10);
  const user = await User.create({ name, email, passwordHash });
  res.json({ success: true, user: { id: user._id, name, email } });
});

router.post("/login", async (req, res) => {
  if (!req.body) return res.status(400).json({ error: "Missing request body" });
  const { email, password } = req.body || {};
  if (!email || !password)
    return res.status(400).json({ error: "email and password are required" });

  const user = await User.findOne({ email });
  if (!user || !(await user.comparePassword(password)))
    return res.status(401).json({ error: "Invalid credentials" });

  const token = jwt.sign({ id: user._id }, JWT_SECRET, { expiresIn: "7d" });
  res.json({ success: true, token, user: { id: user._id, name: user.name } });
});

router.delete("/account", auth, async (req, res) => {
  const user = await User.findById(req.userId);
  if (!user) return res.status(404).json({ error: "User not found" });
  await User.deleteOne({ _id: req.userId });
  res.json({ success: true });
});

export default router;
