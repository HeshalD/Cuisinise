import React, { useState } from 'react';
import { FaUser, FaEnvelope, FaLock } from 'react-icons/fa';
import { useContext } from 'react';
import api from '../utils/api';
import { AuthContext } from '../context/AuthContext';
import Logo from '../images/Cusinise Logo White.png';
import SignUpLogin from '../images/signUpImage.png'

export default function SignUp() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });
  const { login } = useContext(AuthContext);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSignup = async (e) => {
    e?.preventDefault();
    const { name, email, password } = formData;
    // Register user
    await api.post('/auth/register', { name, email, password });
    // Immediately login to get token
    const res = await api.post('/auth/login', { email, password });
    login(res.data.user, res.data.token);
    window.location.href = '/dashboard';
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Food Image */}
      <div className="w-2/7 bg-[#D7FDF0] relative z-[999] overflow-visible flex items-center justify-center">
        <div className="absolute inset-0 bg-[#75A19D] rounded-tr-[70px] rounded-br-[70px]"></div>
        
        {/* Placeholder for food image */}
        <div className="relative z-[999] h-full ml-auto flex items-center justify-end">
          <div className="text-white/20 text-center">
            <img src={SignUpLogin} alt="Sign Up Login" className="ml-[250px] h-1/2 max-h-[700px] w-full object-contain z-[999] pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Right Side - Sign Up Form */}
      <div className="w-5/6 bg-[#D7FDF0] flex items-center justify-center relative z-0">
        <div className="absolute inset-0 bg-[#D7FDF0] -z-10 pointer-events-none"></div>
        
        {/* Bowl Icon Top Right */}
        <div className="absolute top-8 right-8 text-gray-700 opacity-60">
          <img src={Logo} alt="Cuisinise logo" className="h-10 w-10 object-contain" />
        </div>

        {/* Form Container */}
        <div className="relative z-10 w-full max-w-md px-8">
          <h1 className="text-6xl font-bold text-gray-700 mb-12">Sign Up</h1>

          <div className="space-y-6">
            {/* Username Input */}
            <div className="relative">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 z-10 pointer-events-none">
                <FaUser size={20} />
              </div>
              <input
                type="text"
                name="name"
                placeholder="Username"
                value={formData.name}
                onChange={handleChange}
                className="w-full bg-white/70 backdrop-blur-sm rounded-full py-4 pl-14 pr-6 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white/50 transition-all"
              />
            </div>

            {/* Email Input */}
            <div className="relative">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 z-10 pointer-events-none">
                <FaEnvelope size={20}/>
              </div>
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                className="w-full bg-white/70 backdrop-blur-sm rounded-full py-4 pl-14 pr-6 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white/50 transition-all"
              />
            </div>

            {/* Password Input */}
            <div className="relative">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 z-10 pointer-events-none">
                <FaLock size={20}/>
              </div>
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                className="w-full bg-white/70 backdrop-blur-sm rounded-full py-4 pl-14 pr-6 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white/50 transition-all"
              />
            </div>

            {/* Sign Up Button */}
            <button
              onClick={handleSignup}
              className="w-full bg-green-400 hover:bg-green-500 text-white font-semibold rounded-full py-4 mt-8 transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              Sign Up
            </button>
          </div>

          {/* Login Link */}
          <div className="text-center mt-6">
            <p className="text-gray-600">
              Already Have An Account?{' '}
              <a href="/" className="text-gray-700 font-semibold hover:text-gray-800 transition-colors cursor-pointer">
                Login
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}