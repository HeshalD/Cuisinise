import React from 'react'
import image1 from '../images/smart ai.png'
import image2 from '../images/technology.png'
import image3 from '../images/agent.png'
import image4 from '../images/experience.png'

const OurTechnology = () => {
  const features = [
    {
      title: "Placeholder Feature 1",
      description: "Our AI-powered platform makes discovering new dishes, cuisines, and restaurants fast, smart, and effortless.",
      icon: image1
    },
    {
      title: "Placeholder Feature 2",
      description: "We leverage intelligent technology to bring users personalized recipes, menus, and dining options in real time.",
      icon: image2
    },
    {
      title: "Placeholder Feature 3",
      description: "Smart AI agents analyze menus, classify cuisines, and recommend recipes and restaurants, making food discovery simple and reliable.",
      icon: image3
    },
    {
      title: "Placeholder Feature 4",
      description: "Using modern AI and web technologies, we provide accurate, personalized, and enjoyable food exploration for every user.",
      icon: image4
    }
  ];

  return (
    <div className="w-full h-[600px] mx-auto px-4 py-12 bg-[#B2FFD6]">
      {/* Header Section */}
      <div className="text-center mb-16">
        <h2 className="text-5xl font-bold text-gray-700 mb-6">Our Technology</h2>
        <p className="text-xl font-gilroyRegular text-[#4C6B6E] mb-6">
          We use modern AI-driven technology to deliver accurate, personalized, and easy-to-use food recommendations, recipes, and restaurant suggestions for users everywhere.
        </p>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {features.map((feature, index) => (
          <div
            key={index}
            className="bg-[#d4ebe0] rounded-lg p-6 shadow-lg  hover:shadow-xl hover:scale-105 hover:bg-green-600 transition-all duration-300 cursor-pointer group"
          >
            {/* Icon Container */}
            <div className="w-16 h-16 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
              <span className="text-2xl">
                {feature.icon ? (
                  <div
                    className="w-10 h-10 bg-[#4C6B6E] group-hover:bg-white transition-colors duration-300"
                    style={{
                      WebkitMaskImage: `url(${feature.icon})`,
                      maskImage: `url(${feature.icon})`,
                      WebkitMaskRepeat: 'no-repeat',
                      maskRepeat: 'no-repeat',
                      WebkitMaskSize: 'contain',
                      maskSize: 'contain',
                      WebkitMaskPosition: 'center',
                      maskPosition: 'center'
                    }}
                  />
                ) : (
                  <div className="w-10 h-10 bg-[#4C6B6E] group-hover:bg-white transition-colors duration-300" />
                )}
              </span>
            </div>

            <p className="text-gray-600 font-gilroyRegular leading-relaxed group-hover:text-gray-200 transition-colors duration-300">
              {feature.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default OurTechnology;
