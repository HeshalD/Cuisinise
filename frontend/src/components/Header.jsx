import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import logoImage from '../images/Cusinise Logo White.png';
import { FaUser } from 'react-icons/fa';
import { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';

const Header = () => {
  const { user, token, logout } = useContext(AuthContext);
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  const handleDeleteAccount = async () => {
    const ok = window.confirm('Are you sure you want to delete your account? This action cannot be undone.');
    if (!ok) return;
    const confirmText = window.prompt('To confirm deletion, type "delete" (without quotes).');
    if (!confirmText || confirmText.trim().toLowerCase() !== 'delete') {
      return;
    }
    try {
      const res = await fetch('/auth/account', {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data?.error || 'Failed to delete account');
      }
      window.alert('Your account has been deleted.');
      setIsOpen(false);
      logout();
      window.location.href = '/';
    } catch (e) {
      window.alert(e.message || 'Failed to delete account');
    }
  };
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

          <div
            className="relative mr-[-80px]"
          >
            <button
              type="button"
              aria-haspopup="menu"
              aria-expanded={isOpen}
              className="text-[#4C6E6B] hover:text-[#5DC774] transition-colors"
              onClick={() => setIsOpen((v) => !v)}
            >
              <FaUser size={25} />
            </button>

            {isOpen && (
              <div
                role="menu"
                className="absolute right-0 mt-3 w-56 rounded-2xl bg-white shadow-lg ring-1 ring-black/5 p-2 z-50"
              >
                <div className="px-3 py-2">
                  <p className="text-sm text-gray-500">Signed in as</p>
                  <p className="font-gilroyMedium text-gray-800 truncate">{user?.name || 'User'}</p>
                </div>
                <div className="my-1 h-px bg-gray-100" />
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-3 py-2 rounded-xl text-[#4C6E6B] hover:bg-gray-50 hover:text-[#5DC774] transition-colors"
                  role="menuitem"
                >
                  Logout
                </button>
                <button
                  onClick={handleDeleteAccount}
                  className="w-full text-left px-3 py-2 rounded-xl text-red-600 hover:bg-red-50 hover:text-red-700 transition-colors"
                  role="menuitem"
                >
                  Delete Account
                </button>
              </div>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
};


export default Header;