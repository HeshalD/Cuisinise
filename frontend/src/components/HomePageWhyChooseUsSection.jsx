import image1 from '../images/Home - search.png'
import image2 from '../images/Platform.png'
import image3 from '../images/fast.png'
import image4 from '../images/experience.png'

const WhyChooseUs = () => {
    const features = [
      {
        title: "AI-Powered Search",
        description: "Get smart, personalized food and restaurant results.",
        icon: image1
      },
      {
        title: "All-in-One Platform ",
        description: "Explore dishes, recipes, and restaurants in one place.",
        icon: image2
      },
      {
        title: "Fast & Easy",
        description: "Find what you crave in just a few seconds.",
        icon: image3
      },
      {
        title: "Personalized Experience",
        description: "We learn your tastes to give better suggestions every time.",
        icon: image4
      }
    ];
  
    return (
      <div className="w-full h-[600px] mx-auto px-4 py-12 bg-gradient-to-t from-[#B2FFD6] to-[#d4ebe0]">
        {/* Header Section */}
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-700 mb-6">
              Why Choose Us?
        </h2>
          <p className="text-xl font-gilroyRegular text-[#4C6B6E] mb-6">
            Discover why Cusinise is the smarter way to find your next meal.
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
                </span>
              </div>
              
              {/* Content */}
              <h3 className="text-xl font-gilroyBold text-[#4C6B6E] group-hover:text-white mb-3 transition-colors duration-300">
                {feature.title}
              </h3>
              <p className="text-gray-600 font-gilroyRegular leading-relaxed group-hover:text-gray-200 transition-colors duration-300">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  export default WhyChooseUs;