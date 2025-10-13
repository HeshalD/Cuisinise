// src/pages/Login.jsx
import React, { useState, useContext } from 'react';
import { FaEnvelope, FaLock } from 'react-icons/fa';
import api from '../utils/api';
import { AuthContext } from '../context/AuthContext';
import Logo from '../images/Cusinise Logo White.png';
import SignUpLogin from '../images/signUpImage.png'

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useContext(AuthContext);

  const handleLogin = async (e) => {
    e?.preventDefault();
    const res = await api.post('/auth/login', { email, password });
    login(res.data.user, res.data.token);
    window.location.href = '/dashboard';
  };

  return (
    <div className="min-h-screen flex">
      <div className="w-2/7 bg-[#D7FDF0] relative z-[999] overflow-visible flex items-center justify-center">
        <div className="absolute inset-0 bg-[#75A19D] rounded-tr-[70px] rounded-br-[70px]"></div>
        <div className="relative z-[999] h-full ml-auto flex items-center justify-end">
          <div className="text-white/20 text-center">
            <img src={SignUpLogin} alt="Sign Up Login" className="ml-[250px] h-1/2 max-h-[700px] w-full object-contain z-[999] pointer-events-none" />
          </div>
        </div>
      </div>

      <div className="w-5/6 bg-[#D7FDF0] flex items-center justify-center relative z-0">
        <div className="absolute inset-0 bg-[#D7FDF0] -z-10 pointer-events-none"></div>
        <div className="absolute top-8 right-8 text-gray-700 opacity-60">
          <img src={Logo} alt="Cuisinise logo" className="h-10 w-10 object-contain" />
        </div>

        <div className="relative z-10 w-full max-w-md px-8">
          <h1 className="text-6xl font-bold text-gray-700 mb-12">Login</h1>

          <div className="space-y-6">
            <div className="relative">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 z-10 pointer-events-none">
                <FaEnvelope size={20}/>
              </div>
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-white/70 backdrop-blur-sm rounded-full py-4 pl-14 pr-6 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white/50 transition-all"
              />
            </div>

            <div className="relative">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 z-10 pointer-events-none">
                <FaLock size={20}/>
              </div>
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-white/70 backdrop-blur-sm rounded-full py-4 pl-14 pr-6 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white/50 transition-all"
              />
            </div>

            <button
              onClick={handleLogin}
              className="w-full bg-green-400 hover:bg-green-500 text-white font-semibold rounded-full py-4 mt-8 transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              Login
            </button>
          </div>

          <div className="text-center mt-6">
            <p className="text-gray-600">
              Don't have an account?{' '}
              <a href="/signup" className="text-gray-700 font-semibold hover:text-gray-800 transition-colors cursor-pointer">
                Sign Up
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
