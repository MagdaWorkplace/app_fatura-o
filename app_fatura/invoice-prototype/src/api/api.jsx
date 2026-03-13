// Import axios library
import axios from "axios";

// Create a reusable axios instance
// This defines the base URL for all API requests
const api = axios.create({
  baseURL: "http://localhost:8000", // FastAPI backend address
});

// Export the instance so other files can use it
export default api;