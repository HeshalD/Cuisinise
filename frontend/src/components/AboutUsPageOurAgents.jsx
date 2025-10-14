import React from 'react';
import { FaUtensils, FaMapMarkerAlt, FaYoutube, FaSpellCheck, FaSitemap, FaFileAlt } from 'react-icons/fa';
import { MdRestaurantMenu } from 'react-icons/md';

export default function OurAgents() {
  return (
    <section className="w-full min-h-screen bg-[#B2FFD6] py-20 px-8">
      <div className="container mx-auto max-w-6xl">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-700 mb-4">
            Our Agents
          </h2>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Cuisinise uses 4 intelligent AI agents to make food discovery simple, personalized, and accurate.
          </p>
        </div>

        {/* Agents Grid */}
        <div className="space-y-6">
          {/* First Row - 4 Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Cuisine Classifier */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 flex flex-col items-center text-center hover:bg-green-600 hover:scale-105 group cursor-pointer">
              <div className="w-16 h-16 bg-gray-600 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white transition-all duration-300">
                <FaUtensils className="text-white text-3xl group-hover:text-green-600 transition-all duration-300" />
              </div>
              <h3 className="text-xl font-bold text-gray-700 mb-3 group-hover:text-white transition-all duration-300">
                Cuisine Classifier
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed group-hover:text-white transition-all duration-300">
                Identifies and groups cuisines accurately.
              </p>
            </div>

            {/* Recipe Recommender */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 flex flex-col items-center text-center hover:bg-green-600 hover:scale-105 group cursor-pointer">
              <div className="w-16 h-16 bg-gray-600 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white transition-all duration-300">
                <MdRestaurantMenu className="text-white text-3xl group-hover:text-green-600 transition-all duration-300" />
              </div>
              <h3 className="text-xl font-bold text-gray-700 mb-3 group-hover:text-white transition-all duration-300">
                Recipe Recommender
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed group-hover:text-white transition-all duration-300">
                Suggests dishes and recipes you'll love.
              </p>
            </div>

            {/* Restaurant Finder */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 flex flex-col items-center text-center hover:bg-green-600 hover:scale-105 group cursor-pointer">
              <div className="w-16 h-16 bg-gray-600 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white transition-all duration-300">
                <FaMapMarkerAlt className="text-white text-3xl group-hover:text-green-600 transition-all duration-300" />
              </div>
              <h3 className="text-xl font-bold text-gray-700 mb-3 group-hover:text-white transition-all duration-300">
                Restaurant Finder
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed group-hover:text-white transition-all duration-300">
                Finds the best nearby restaurants.
              </p>
            </div>

            {/* Menu Analyzer */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 flex flex-col items-center text-center hover:bg-green-600 hover:scale-105 group cursor-pointer">
              <div className="w-16 h-16 bg-gray-600 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white transition-all duration-300">
                <FaFileAlt className="text-white text-3xl group-hover:text-green-600 transition-all duration-300" />
              </div>
              <h3 className="text-xl font-bold text-gray-700 mb-3 group-hover:text-white transition-all duration-300">
                Menu Analyzer
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed group-hover:text-white transition-all duration-300">
                Scans and understands restaurant menus.
              </p>
            </div>
          </div>

          {/* Second Row - 3 Cards Centered */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {/* YouTube Recommender */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 flex flex-col items-center text-center hover:bg-green-600 hover:scale-105 group cursor-pointer">
              <div className="w-16 h-16 bg-gray-600 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white transition-all duration-300">
                <FaYoutube className="text-white text-3xl group-hover:text-green-600 transition-all duration-300" />
              </div>
              <h3 className="text-xl font-bold text-gray-700 mb-3 group-hover:text-white transition-all duration-300">
                YouTube Recommender
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed group-hover:text-white transition-all duration-300">
                Recommends related cooking videos.
              </p>
            </div>

            {/* Spell Corrector */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 flex flex-col items-center text-center hover:bg-green-600 hover:scale-105 group cursor-pointer">
              <div className="w-16 h-16 bg-gray-600 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white transition-all duration-300">
                <FaSpellCheck className="text-white text-3xl group-hover:text-green-600 transition-all duration-300" />
              </div>
              <h3 className="text-xl font-bold text-gray-700 mb-3 group-hover:text-white transition-all duration-300">
                Spell Corrector
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed group-hover:text-white transition-all duration-300">
                Fixes typos for smoother searches.
              </p>
            </div>

            {/* Coordinator Agent */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 flex flex-col items-center text-center hover:bg-green-600 hover:scale-105 group cursor-pointer">
              <div className="w-16 h-16 bg-gray-600 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white transition-all duration-300">
                <FaSitemap className="text-white text-3xl group-hover:text-green-600 transition-all duration-300" />
              </div>
              <h3 className="text-xl font-bold text-gray-700 mb-3 group-hover:text-white transition-all duration-300">
                Coordinator Agent
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed group-hover:text-white transition-all duration-300">
                Manages all agents to ensure accurate results.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}