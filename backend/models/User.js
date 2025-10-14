import mongoose from "mongoose";
import bcrypt from "bcrypt";

const UserSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, unique: true, required: true },
  passwordHash: { type: String, required: true },
  createdAt: { type: Date, default: Date.now },
});

UserSchema.methods.comparePassword = function (pw) {
  return bcrypt.compare(pw, this.passwordHash);
};

export default mongoose.model("User", UserSchema);
