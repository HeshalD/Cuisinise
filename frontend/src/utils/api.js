// src/utils/api.js
import axios from "axios";

const baseURL = process.env.REACT_APP_API_BASE_URL || "https://cuisinise-backend.purpletree-02fc877a.centralindia.azurecontainerapps.io/api";
const api = axios.create({ baseURL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
