/* Prototype version! */

// Import routing tools from react-router-dom.
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Import the pages (components).
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

function App() {

  return (

    // BrowserRouter enables navigation between pages
    <BrowserRouter>

      {/* Routes container holds all route definitions */}
      <Routes>

        {/* When user visits "/" show Login page */}
        <Route path="/" element={<Login />} />

        {/* When user visits "/register" show Register page */}
        <Route path="/register" element={<Register />} />

        {/* When user visits "/dashboard" show Dashboard page */}
        <Route path="/dashboard" element={<Dashboard />} />

      </Routes>

    </BrowserRouter>

  );
}

// Export App so main.jsx can render it.
export default App;