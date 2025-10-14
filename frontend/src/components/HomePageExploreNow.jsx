import React from 'react';
import { Link } from 'react-router-dom';

const CheckNowCTA = () => {
  return (
    <section className="py-16 px-8 bg-gradient-to-b from-[#B2FFD6] to-[#d4ebe0]">
      <div className="max-w-7xl mx-auto">
        <div className="bg-gradient-to-b from-green-400 to-green-500 rounded-3xl py-16 px-8 text-center">
          <p className="text-white font-gilroyMedium text-lg mb-4">
            So with all that being said,
          </p>
          <h2 className="text-white font-gilroyRegular text-4xl md:text-5xl mb-8">
            Ready to discover your next favorite meal?
          </h2>
          <Link to='/chat'className="bg-white text-green-500 font-gilroyBold px-10 py-3 rounded-full hover:bg-green-300 hover:text-white transition-colors duration-150 ease-in-out hover:scale-105 hover:shadow-lg text-lg">
            Check Now
          </Link>
        </div>
      </div>
    </section>
  );
};

export default CheckNowCTA;