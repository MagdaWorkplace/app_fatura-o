/* Prototype version! */

import { useState } from "react";             // React hook for storing form inputs.
import { useNavigate, Link } from "react-router-dom"; // Navigation and links.
import api from "../api/api";                  // Axios instance to connect to FastAPI.

function Register() {
  // State to store form inputs
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");       // For error messages.
  const navigate = useNavigate();               // Redirect after successful register.

  // Function called when user submits the form.
  const handleRegister = async (event) => {
    event.preventDefault(); // Prevent page reload.

    try {
      // Send POST request to backend.
      await api.post("/register", { username, email, password });

      // If successful, redirect to login.
      navigate("/");

    } catch (err) {
      // Show backend error if exists.
      if (err.response && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Registration failed. Try again.");
      }
    }
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <form
        className="bg-white p-6 rounded shadow-md w-96"
        onSubmit={handleRegister}
      >
        <h2 className="text-xl font-bold mb-4">Register</h2>

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

        {/* Email input */}
        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 border rounded mb-2"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        {/* Password input */}
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 border rounded mb-4"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {/* Submit button */}
        <button className="w-full bg-green-500 text-white p-2 rounded">
          Register
        </button>

        {/* Link to login */}
        <p className="mt-4 text-sm text-gray-600">
          Already have an account? <Link to="/" className="text-blue-500">Login</Link>
        </p>
      </form>
    </div>
  );
}

export default Register;