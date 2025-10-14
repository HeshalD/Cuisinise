import React from 'react';
import { SiGithub, SiPython, SiMongodb, SiNodedotjs, SiExpress, SiReact } from 'react-icons/si';

export default function OurStorySection() {
  return (
    <section className="w-full min-h-screen bg-gradient-to-b from-[#d4ebe0] to-[#B2FFD6] py-16 px-8">
      <div className="container mx-auto max-w-7xl space-y-8">
        {/* Our Story Section */}
        <div className="relative flex items-stretch">
          {/* Left Side - White Background with Text */}
          <div className="bg-white backdrop-blur-sm p-12 flex-1 rounded-l-3xl z-10">
            <h2 className="text-4xl font-bold text-gray-700 mb-6">
              Our Story
            </h2>
            <p className="text-gray-600 text-lg leading-relaxed max-w-xl">
              Cuisinise was created to make finding food easier, smarter, and more enjoyable. Using intelligent AI agents, our platform analyzes menus, classifies cuisines, recommends recipes, and helps you discover the best restaurants nearby.
            </p>
          </div>
          
          {/* Right Side - Teal Triangle */}
          <div className="bg-[#7a9b9e] flex-1 relative">
            <div className="absolute inset-0 bg-[#7a9b9e] rounded-r-3xl"></div>
            {/* Triangle cutout effect */}
            <div className="absolute left-0 top-0 bottom-0 w-32">
              <svg className="h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                <polygon points="0,0 100,50 0,100" fill="white" fillOpacity="1"/>
              </svg>
            </div>
          </div>
        </div>

        {/* Our Mission and Technology Section */}
        <div className="relative flex items-stretch">
          {/* Left Side - Teal Background with Mission */}
          <div className="bg-[#7a9b9e] p-12 flex-1 relative rounded-l-3xl">
            <h2 className="text-4xl font-bold text-white mb-6">
              Our Mission
            </h2>
            <p className="text-white/90 text-lg leading-relaxed max-w-xl">
              To empower people to explore, experience, and enjoy food effortlessly through intelligent technology that personalizes recipes, identifies cuisines, and connects users with the best dining options around them.
            </p>
          </div>
          
          {/* Right Side - White Background with Technology */}
          <div className="bg-white/90 backdrop-blur-sm p-12 flex-1 relative rounded-r-3xl z-10">
            
            <div className="relative z-10">
              <h2 className="text-4xl font-bold text-gray-700 mb-4">
                The Technology Behind Us
              </h2>
              <p className="text-gray-600 text-lg mb-8">
                Cuisinise combines AI and web technologies for a smooth experience.
              </p>
              
              {/* Technology Icons */}
              <div className="flex items-center gap-6 flex-wrap">
                <SiGithub className="text-gray-700 text-5xl" />
                <SiPython className="text-gray-700 text-5xl" />
                <SiMongodb className="text-gray-700 text-5xl" />
                <SiNodedotjs className="text-gray-700 text-5xl" />
                <SiExpress className="text-gray-700 text-5xl" />
                <SiReact className="text-gray-700 text-5xl" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}