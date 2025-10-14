import React from 'react';
import about1 from '../images/about1.jpeg'
import about2 from '../images/about2.jpeg'

export default function AboutCuisinise() {
  return (
    <section className="w-full min-h-screen bg-[#d4ebe0] py-20 px-8">
      <div className="container mx-auto max-w-6xl">
        <div className="flex items-center justify-between gap-16">
          {/* Left Side - Text Content */}
          <div className="flex-1">
            <h2 className="text-5xl font-bold text-gray-700 mb-8">
              About Cuisinise
            </h2>
            <p className="text-gray-600 text-lg leading-relaxed max-w-md">
              Cuisinise is an AI-powered platform that helps you find the best dishes and restaurants effortlessly.
            </p>
          </div>

          {/* Right Side - Images */}
          <div className="flex-1 relative">
            <div className="flex gap-6 items-center">
              {/* Image 1 - Chef cooking with smoke */}
              <div className="w-[300px] h-[400px] rounded-tr-3xl rounded-bl-3xl overflow-hidden shadow-2xl bg-gray-800 transform hover:-rotate-6 transition-all duration-300">
                <div className="w-full h-full flex items-center justify-center">
                  <img src={about2} alt="about2" className='w-full h-full object-cover' />
                </div>
              </div>

              {/* Image 2 - Restaurant kitchen */}
              <div className="w-[300px] h-[400px] rounded-tr-3xl rounded-bl-3xl overflow-hidden shadow-2xl bg-gray-800 transform translate-y-[150px] hover:rotate-6 transition-all duration-300">
                <div className="w-full h-full flex items-center justify-center">
                  <div className="w-full h-full flex items-center justify-center">
                  <img src={about1} alt="about1" className='w-full h-full object-cover' />
                </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}