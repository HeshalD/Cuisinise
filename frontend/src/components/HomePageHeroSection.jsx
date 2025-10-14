import React from 'react';
import Food1 from '../images/home1.png'
import Food2 from '../images/home 2.png'
import Food3 from '../images/home3.png'
import { Link } from 'react-router-dom';

export default function HomePageHeroSection() {
  return (
    <section className="relative w-full h-screen overflow-hidden">
      {/* Background Split */}
      <div className="absolute inset-0 flex bg-gradient-to-br from-[#c8e6d7] to-[#d4ebe0]">
        {/* Left side - Light mint green */}
        <div className="w-1/2 bg-gradient-to-br from-[#c8e6d7] to-[#d4ebe0]"></div>
        {/* Right side - Blue-gray */}
        <div className="w-1/2 bg-[#7a9b9e] rounded-tl-[70px] rounded-bl-[70px]"></div>
      </div>

      {/* Content Container */}
      <div className="relative z-10 h-full flex items-center">
        <div className="container mx-auto px-12 lg:px-16">
          <div className="max-w-xl">
            {/* Heading */}
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-700 leading-tight mb-6">
              Discover <span className="text-green-500">Food</span><br />
              You'll Love -<br />
              Anywhere,<br />
              Anytime.
            </h1>

            {/* Subtitle */}
            <p className="text-gray-600 text-lg mb-8 max-w-md">
              Explore cuisines, find recipes, and locate restaurants tailored just for you.
            </p>

            {/* CTA Button */}
            <Link to='/chat' className="bg-green-400 hover:bg-green-500 text-white font-semibold px-8 py-3 rounded-full transition-all duration-300 transform hover:scale-105 shadow-lg">
              Explore
            </Link>
          </div>
        </div>
      </div>

      {/* Food Images - Absolute Positioned */}
      <div className="absolute top-0 right-0 w-1/2 h-full">
        {/* Top Center - Grilled Meat Dish */}
        <div className="absolute top-12 left-0 -translate-x-1/2 w-[400px] h-[400px] rounded-full overflow-hidden shadow-2xl group cursor-pointer">
          <div className="w-full h-full flex items-center justify-center">
            <img 
              src={Food1} 
              className="w-full h-full object-cover object-center scale-[1.15] transition-all duration-700 ease-out group-hover:scale-[1.18] animate-spin-slow"
              style={{
                animation: 'slowRotate 30s linear infinite'
              }}
            />
          </div>
        </div>

        {/* Top Right - Egg Dish */}
        <div className="absolute top-8 right-0 translate-x-1/4 w-72 h-72 rounded-full overflow-hidden shadow-2xl group cursor-pointer">
          <div className="w-full h-full flex items-center justify-center">
            <img 
              src={Food2} 
              className="w-full h-full object-cover object-center scale-[1.15] transition-all duration-700 ease-out group-hover:scale-[1.18]"
              style={{
                animation: 'slowRotate 25s linear infinite'
              }}
            />
          </div>
        </div>

        {/* Bottom Center Right - Shrimp Pasta */}
        <div className="absolute bottom-10 right-40 w-[350px] h-[350px] rounded-full overflow-hidden shadow-2xl group cursor-pointer">
          <div className="w-full h-full flex items-center justify-center">
            <img 
              src={Food3} 
              className="w-full h-full object-cover object-center scale-[1.15] transition-all duration-700 ease-out group-hover:scale-[1.18]"
              style={{
                animation: 'slowRotate 35s linear infinite'
              }}
            />
          </div>
        </div>
      </div>

      {/* Animation Styles */}
      <style jsx>{`
        @keyframes slowRotate {
          from {
            transform: rotate(0deg) scale(1.15);
          }
          to {
            transform: rotate(360deg) scale(1.15);
          }
        }
        
        .group:hover img {
          animation-play-state: paused;
        }
      `}</style>
    </section>
  );
}