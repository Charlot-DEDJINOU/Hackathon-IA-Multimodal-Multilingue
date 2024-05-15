import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Footer from "./components/commons/Footer";
import Header from "./components/commons/Header"
import Home from "./views/Home";
import Login from "./views/Login";
import Register from "./views/Register";
import PayementForm from "./views/PayementForm";

function App() {

  return (
    <React.StrictMode>
      <Router>
          <div className="flex flex-col min-h-screen">
            <Header />
            <main className="flex-grow">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={ <Login />} />
                <Route path="/register" element={ <Register />} />
                <Route path="/payement" element={ <PayementForm />} />
              </Routes>
            </main>
            <Footer />
          </div>
      </Router>
    </React.StrictMode>
  );
}

export default App;