import './App.css';
import { Routes, Route } from "react-router-dom"
import ChatDashboard from './pages/ChatDashboard';
import Login from './pages/Login';
import Signup from './pages/Signup';
import AuthProvider from './context/AuthContext';

function App() {

  return (
    <AuthProvider>
      <div >
        <Routes>
          <Route path="/" element={<Login/>}/>
          <Route path="/signup" element={<Signup/>}/>
          <Route path="/dashboard" element={<ChatDashboard/>}/>
        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;
