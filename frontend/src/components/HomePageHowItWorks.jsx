import React from 'react';
import Image1 from '../images/home4.jpeg'
import Image2 from '../images/home5.jpeg'
import Image3 from '../images/home6.jpeg'
import Image4 from '../images/home7.jpeg'   

export default function HomePageHowItWorks() {
  return (
    <section className="w-full min-h-screen bg-[#d4ebe0] py-20 px-8">
      <div className="container mx-auto">
        <div className="flex items-center justify-between gap-16">
          {/* Left Side - Image Grid */}
          <div className="flex-1 relative ml-[100px]">
            <div className="grid grid-cols-2 gap-6 max-w-2xl">
              {/* Top Left - Image 1 */}
              <div className="rounded-tr-[50px] rounded-bl-[50px] overflow-hidden shadow-xl bg-gray-800 h-[400px] w-[300px] self-end justify-self-end">
                <div className="w-full h-full flex items-center justify-center">
                  <img src={Image1} alt="Image 1" className="w-full h-full object-cover" />
                </div>
              </div>

              {/* Top Right - Image 2 */}
              <div className="rounded-tl-[50px] rounded-br-[50px] overflow-hidden shadow-xl bg-gray-800 h-[250px] w-[400px] self-end justify-self-start">
                <div className="w-full h-full flex items-center justify-center">
                  <img src={Image2} alt="Image 2" className="w-full h-full object-cover" />
                </div>
              </div>

              {/* Bottom Left - Image 3 */}
              <div className="rounded-tl-[50px] rounded-br-[50px] overflow-hidden shadow-xl bg-gray-800 h-[250px] w-[400px] self-start justify-self-end">
                <div className="w-full h-full flex items-center justify-center">
                  <img src={Image3} alt="Image 3" className="w-full h-full object-cover" />
                </div>
              </div>

              {/* Bottom Right - Image 4 */}
              <div className="rounded-tr-[50px] rounded-bl-[50px] overflow-hidden shadow-xl bg-gray-800 h-[400px] w-[300px] self-start justify-self-start">
                <div className="w-full h-full flex items-center justify-center">
                  <img src={Image4} alt="Image 4" className="w-full h-full object-cover" />
                </div>
              </div>
            </div>
          </div>

          {/* Right Side - Text Content */}
          <div className="flex-1 max-w-lg">
            <h2 className="text-5xl font-bold text-gray-700 mb-6">
              How It Works,
            </h2>
            <p className="text-gray-600 text-lg leading-relaxed">
              Food Explore uses smart AI agents to understand what you're craving.
            </p>
            <p className="text-gray-600 text-lg leading-relaxed mt-4">
              Just type a dish or cuisine, and our system analyzes menus, classifies cuisines, recommends recipes, and finds the best restaurants near you.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}