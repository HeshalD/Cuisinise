import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import logoImage from '../images/Cusinise Logo White.png';
import { FaUser } from 'react-icons/fa';

const Header = () => {
  return (
    <header className="bg-gradient-to-br from-[#D7FDF0] to-[#B2FFD6] py-2 px-0 shadow-md shadow-rounded-full ml-[10px] mr-[10px] rounded-[40px] mb-[20px]">
      <div className="max-w-7xl mx-auto flex items-center">
        
            <Link to="/home">
              <img src={logoImage} alt='Cusinise Logo' className="w-48 h-16 object-contain ml-[-100px]"/>
            </Link>

        {/* Navigation */}
        <nav className="ml-auto flex items-center gap-12 justify-end">
          <NavLink
            to="/home"
            end
            className={({ isActive }) => `font-gilroyMedium text-lg transition-colors duration-150 ease-in-out ${isActive ? 'text-[#5DC774]' : 'text-[#4C6E6B] hover:text-[#5DC774]'}`}
          >
            Home
          </NavLink>
          <NavLink
            to="/about-us"
            className={({ isActive }) => `font-gilroyMedium text-lg transition-colors duration-150 ease-in-out ${isActive ? 'text-[#5DC774]' : 'text-[#4C6E6B] hover:text-[#5DC774]'}`}
          >
            About
          </NavLink>
          <NavLink
            to="/chat"
            className={({ isActive }) => `font-gilroyMedium text-lg transition-colors duration-150 ease-in-out ${isActive ? 'text-[#5DC774]' : 'text-[#4C6E6B] hover:text-[#5DC774]'}`}
          >
            Chat
          </NavLink>
          <NavLink
            to="/how-it-works"
            className={({ isActive }) => `font-gilroyMedium text-lg transition-colors duration-150 ease-in-out ${isActive ? 'text-[#5DC774]' : 'text-[#4C6E6B] hover:text-[#5DC774]'}`}
          >
            How It Works
          </NavLink>


          <NavLink
            to="/profile"
            className={({ isActive }) => `font-gilroyMedium text-lg transition-colors duration-150 ease-in-out ${isActive ? 'text-[#5DC774]' : 'text-[#4C6E6B] hover:text-[#5DC774] mr-[-80px]'}`}
          >
            <FaUser size={25} />
          </NavLink>
        </nav>
      </div>
    </header>
  );
};

export default Header;