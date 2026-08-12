import axios from "axios";
import { API_BASE_URL } from "./api/api";

// Create axios instance with central API base URL
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor for adding JWT token and logging
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  // Log request
  console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`, {
    config,
    timestamp: new Date().toISOString()
  });

  return config;
});

// Response interceptor for logging and error handling
api.interceptors.response.use(
  (response) => {
    // Log successful response
    console.log(`API Response: ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`, {
      response,
      timestamp: new Date().toISOString()
    });
    return response;
  },
  (error) => {
    // Log error response
    console.error(`API Error: ${error.config?.method?.toUpperCase()} ${error.config?.url} - ${error.response?.status || 'Network Error'}`, {
      error,
      timestamp: new Date().toISOString()
    });

    // Handle 401 Unauthorized - token expired or invalid
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      if (typeof window !== "undefined" && !["/login", "/register"].includes(window.location.pathname)) {
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default api;