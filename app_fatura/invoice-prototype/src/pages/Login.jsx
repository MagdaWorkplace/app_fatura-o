/* Prototype version! */

import { useState } from "react";               // React hook for storing input state.
import { useNavigate } from "react-router-dom"; // To redirect after login.
import api from "../api/api";                    // Axios instance.
import { Link } from "react-router-dom";        // To navigate between pages.

function Login() {
  // State to store username and password from input.
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // State to store error messages
  const [error, setError] = useState("");

  // Navigate lets us redirect the user programmatically.
  const navigate = useNavigate();

  // Function called when user clicks "Login".
  const handleLogin = async (event) => {
    event.preventDefault(); // Prevent page refresh

    try {
      // Send POST request to FastAPI /login.
      const response = await api.post("/login", {
        username: username,
        password: password,
      });

      // Save the token returned by FastAPI in localStorage.
      // We will use it later to access protected routes.
      localStorage.setItem("token", response.data.access_token);

      // Redirect user to dashboard
      navigate("/dashboard");

    } catch (err) {
      // If login fails, show the error.
      if (err.response && err.response.data.detail) {
        setError(err.response.data.detail); // e.g., "Wrong password!" or "User doesn't exist!"
      } else {
        setError("Login failed. Try again.");
      }
    }
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <form
        className="bg-white p-6 rounded shadow-md w-96"
        onSubmit={handleLogin}
      >
        <h2 className="text-xl font-bold mb-4">Login</h2>

        {/* Show error if exists */}
        {error && <p className="text-red-500 mb-2">{error}</p>}

        {/* Username input */}
        <input
          type="text"
          placeholder="Username"
          className="w-full p-2 border rounded mb-2"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        {/* Password input */}
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 border rounded mb-4"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {/* Login button */}
        <button className="w-full bg-blue-500 text-white p-2 rounded">
          Login
        </button>

        {/* Link to register page */}
        <p className="mt-4 text-sm text-gray-600">
          Don't have an account? <Link to="/register" className="text-blue-500">Register</Link>
        </p>
      </form>
    </div>
  );
}

export default Login;