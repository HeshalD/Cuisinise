// src/utils/api.js
import axios from "axios";

const baseURL = "https://cuisinise.onrender.com/api"; // ✅ add /api suffix

const api = axios.create({ baseURL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
