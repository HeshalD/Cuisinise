import React from 'react';
import Food1 from '../images/home1.png'
import Food2 from '../images/work2.jpeg'
import Food3 from '../images/work3.jpeg'
import Food4 from '../images/work4.jpeg'
import Food5 from '../images/home6.jpeg'
import { Link } from 'react-router-dom';

export default function HowCuisiniseWorks() {
  return (
    <section className="relative w-full min-h-screen bg-gradient-to-b from-[#d4ebe0] to-[#d4ebe0] py-16 px-8 overflow-hidden">
      {/* Decorative Green Blobs */}
      <div className="absolute top-20 right-[-200px] w-[597px] h-[597px] bg-green-400 rounded-full"></div>
      <div className="absolute top-[500px] left-[-200px] w-[586px] h-[586px] bg-green-500 rounded-full"></div>
      <div className="absolute top-[800px] left-0 w-96 h-96 bg-green-400 rounded-full"></div>
      <div className="absolute top-[1100px] right-[-150px] w-[439px] h-[439px] bg-green-500 rounded-full"></div>
      <div className="absolute top-[1700px] left-[-100px] w-96 h-96 bg-green-400 rounded-full"></div>
      <div className="absolute bottom-40 right-[-200px] w-[486px] h-[486px] bg-green-400 rounded-full"></div>

      {/* Content Container */}
      <div className="relative z-10 w-full max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-20">
          <h2 className="text-5xl font-bold text-gray-700 mb-3">
            How Cuisinise Works
          </h2>
          <p className="text-green-500 text-xl">
            Discover how Food Explore helps you find the best food around!
          </p>
        </div>

        {/* Step 1 - Text Left, Image Right */}
        <div className="flex items-start justify-between mb-24 gap-12">
          <div className="flex items-start gap-4 flex-1 mr-auto max-w-3xl">
            <div className="flex-shrink-0 w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center text-white font-bold text-lg">
              1
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-700 mb-2">
                Tell Us What You're Craving
              </h3>
              <p className="text-gray-600 text-xl leading-relaxed">
                Enter the type of food, cuisine, or dish you want to explore.
              </p>
              <p className="text-gray-600 text-l leading-relaxed mt-1">
                You can also mention your preferred location to get nearby options.
              </p>
            </div>
          </div>
          <div className="flex-shrink-1  w-[400px] h-[400px] rounded-full overflow-hidden shadow-2xl group cursor-pointer">
            <div className="w-full h-full bg-gray-800 flex items-center justify-center rotating-image">
              <img src={Food2} alt="Food" className="w-full h-full object-cover object-center scale-[120%]" />
            </div>
          </div>
        </div>

        {/* Step 2 - Image Left, Text Right */}
        <div className="flex items-center justify-between mb-24 gap-12">
          <div className="flex-shrink-0  w-[400px] h-[400px] mt-[-100px] rounded-full overflow-hidden shadow-2xl group cursor-pointer">
            <div className="w-full h-full bg-gray-800 flex items-center justify-center rotating-image">
              <img src={Food3} alt="Food" className="w-full h-full object-cover object-center scale-[120%]" />
            </div>
          </div>
          <div className="flex items-start gap-4 flex-1 ml-auto max-w-3xl text-left">
            <div className="flex-shrink-0 w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center text-white font-bold text-lg">
              2
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-700 mb-2">
                Menu Analyzer in Action
              </h3>
              <p className="text-gray-600 text-xl leading-relaxed">
                Our Menu Analyzer Agent scans restaurant menus and identifies dishes that match your taste and preferences.
              </p>
              <p className="text-gray-600 text-l leading-relaxed mt-1">
                It helps you understand ingredients, nutrition, and dish details.
              </p>
            </div>
          </div>
        </div>

        {/* Step 3 - Text Left, Image Right */}
        <div className="flex items-center justify-between mb-24 gap-12">
          <div className="flex items-start gap-4 flex-1 mr-auto max-w-3xl">
            <div className="flex-shrink-0 w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center text-white font-bold text-lg">
              3
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-700 mb-2">
                Cuisine Classifier Learns Your Taste
              </h3>
              <p className="text-gray-600 text-xl leading-relaxed">
                Our Cuisine Classifier Agent categorizes dishes into cuisines like Italian, Indian, Chinese, or Sri Lankan.
              </p>
              <p className="text-gray-600 text-l leading-relaxed mt-1">
                It learns your food choices to give more accurate results.
              </p>
            </div>
          </div>
          <div className="flex-shrink-0 w-[400px] h-[400px] mt-[100px] rounded-full overflow-hidden shadow-2xl group cursor-pointer">
            <div className="w-full h-full bg-gray-800 flex items-center justify-center rotating-image">
              <img src={Food4} alt="Food" className="w-full h-full object-cover object-center scale-[120%]" />
            </div>
          </div>
        </div>

        {/* Step 4 - Image Left, Text Right */}
        <div className="flex items-center justify-between mb-24 gap-12">
          <div className="flex-shrink-0 w-[400px] h-[400px] rounded-full overflow-hidden shadow-2xl group cursor-pointer">
            <div className="w-full h-full bg-gray-800 flex items-center justify-center rotating-image">
              <img src={Food5} alt="Food" className="w-full h-full object-cover object-center scale-[120%]" />
            </div>
          </div>
          <div className="flex items-start gap-4 flex-1 ml-auto max-w-3xl text-left">
            <div className="flex-shrink-0 w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center text-white font-bold text-lg">
              4
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-700 mb-2">
                Recipe Recommender Gives You Options
              </h3>
              <p className="text-gray-600 text-xl leading-relaxed">
                The Recipe Recommender Agent suggests recipes based on your selected food type.
              </p>
              <p className="text-gray-600 text-l leading-relaxed mt-1">
                Perfect for trying out by making dishes at home or explore similar items.
              </p>
            </div>
          </div>
        </div>

        {/* Step 5 - Text Left, Image Right */}
        <div className="flex items-center justify-between mb-20 gap-12">
          <div className="flex items-start gap-4 flex-1 mr-auto max-w-3xl">
            <div className="flex-shrink-0 w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center text-white font-bold text-lg">
              5
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-700 mb-2">
                Restaurant Finder Shows You Where to Go
              </h3>
              <p className="text-gray-600 text-xl leading-relaxed">
                Finally, the Restaurant Finder Agent locates the best restaurants near your location that serve your chosen dishes or cuisines.
              </p>
              <p className="text-gray-600 text-l leading-relaxed mt-1">
                It displays contact info, ratings, and directions.
              </p>
            </div>
          </div>
          <div className="flex-shrink-0 w-[400px] h-[400px] rounded-full overflow-hidden shadow-2xl group cursor-pointer">
            <div className="w-full h-full bg-gray-800 flex items-center justify-center rotating-image">
              <img src={Food1} alt="Food" className="w-full h-full object-cover object-center scale-[120%]" />
            </div>
          </div>
        </div>

        {/* CTA Button */}
        <div className="text-center mt-16">
          <Link to='/chat' className="bg-green-400 hover:bg-green-500 text-white text-xl font-semibold px-[80px] py-[20px] rounded-full transition-all duration-300 transform hover:scale-105 shadow-lg">
            Get Start
          </Link>
        </div>
      </div>

      {/* Global Animation Styles */}
      <style jsx>{`
        @keyframes slowRotate {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
        
        .rotating-image {
          animation: slowRotate 30s linear infinite;
        }
        
        .group:hover .rotating-image {
          animation-play-state: paused;
        }
      `}</style>
    </section>
  );
}