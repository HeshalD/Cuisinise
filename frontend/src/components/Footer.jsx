import React from "react";
import { NavLink, Link } from "react-router-dom";
import { FaEnvelope, FaMapMarkerAlt } from "react-icons/fa";
import logoImage from '../images/Cusinise Logo White.png';

const Footer = () => {
  return (
    <footer className="bg-gradient-to-t from-[#B2FFD6] to-[#d4ebe0] py-12 px-8">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Logo and Description */}
          <div className="flex flex-col items-center">
            <div className="mb-4">
              <Link to="/">
                <img
                  src={logoImage}
                  alt="Cuisinise Logo"
                  className="w-52 h-20 object-contain"
                />
              </Link>
            </div>
            <h3 className="text-[#496663] font-semibold text-[30px] mb-3">
              Cuisinise
            </h3>
          </div>

          {/* Overview */}
          <div>
            <h3 className="text-[#496663] font-semibold text-lg mb-4">
              Overview
            </h3>
            <ul className="space-y-2">
              <li>
                <NavLink
                  to="/"
                  end
                  className={({ isActive }) => `transition-colors ${isActive ? 'text-[#5DC774]' : 'text-[#6b7280] hover:text-[#5DC774]'}`}
                >
                  Home
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/about-us"
                  className={({ isActive }) => `transition-colors ${isActive ? 'text-[#5DC774]' : 'text-[#6b7280] hover:text-[#5DC774]'}`}
                >
                  About
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/chat"
                  className={({ isActive }) => `transition-colors ${isActive ? 'text-[#5DC774]' : 'text-[#6b7280] hover:text-[#5DC774]'}`}
                >
                  Chat
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/how-it-works"
                  className={({ isActive }) => `transition-colors ${isActive ? 'text-[#5DC774]' : 'text-[#6b7280] hover:text-[#5DC774]'}`}
                >
                  How It Works
                </NavLink>
              </li>
            </ul>
          </div>

          {/* Social Media */}
          <div>
            <h3 className="text-[#496663] font-semibold text-lg mb-4">
              Social Media
            </h3>
            <ul className="space-y-2">
              <li>
                <a
                  href="#"
                  className="text-[#6b7280] hover:text-[#5DC774] transition-colors"
                >
                  Instagram
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#6b7280] hover:text-[#5DC774] transition-colors"
                >
                  Linkedin
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#6b7280] hover:text-[#5DC774] transition-colors"
                >
                  Facebook
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#6b7280] hover:text-[#5DC774] transition-colors"
                >
                  Twitter
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-[#6b7280] hover:text-[#5DC774] transition-colors"
                >
                  Github
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-[#496663] font-semibold text-lg mb-4">
              Contact Info
            </h3>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <FaEnvelope className="text-[#496663] text-xl mt-1 flex-shrink-0" />
                <div>
                  <p className="text-[#6b7280]">
                    Email: support@cuisinise.com
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <FaMapMarkerAlt className="text-[#496663] text-xl mt-1 flex-shrink-0" />
                <div>
                  <p className="text-[#6b7280]">Location: Colombo, Sri Lanka</p>
                </div>
              </div>
            </div>
            <div className="mt-6">
              <a
                href="#"
                className="text-[#496663] hover:text-[#5DC774] transition-colors"
              >
                Privacy Policy
              </a>
              <span className="text-[#6b7280] mx-2">|</span>
              <a
                href="#"
                className="text-[#496663] hover:text-[#5DC774] transition-colors"
              >
                Terms of Service
              </a>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-[#496663] opacity-50 my-8"></div>

        {/* Copyright */}
        <div className="text-center">
          <p className="text-[#496663]">
            © 2025 Cuisinise (Pvt) Ltd. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
