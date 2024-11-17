import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import Survey from "./pages/Survey";
import Register from "./components/Register";
import MeetingForm from "./components/MeetingForm";
import Matching from "./components/Matching";
import NavBar from "./components/NavBar";

function App() {
  return (
    <Router>
      <div className="app-container">
        <div className="navbar-container">
          <NavBar />
        </div>
        <div className="background"></div>
        <div className="content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/survey" element={<Survey />} />
            <Route path="/register" element={<Register />} />
            <Route path="/meeting" element={<MeetingForm />} />
            <Route path="/matching" element={<Matching />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
