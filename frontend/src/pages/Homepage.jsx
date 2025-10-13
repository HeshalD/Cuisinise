import React from 'react'
import Header from '../components/Header'
import HomePageHeroSection from '../components/HomePageHeroSection'
import HomePageHowItWorks from '../components/HomePageHowItWorks'
import HomePageWhyChooseUsSection from '../components/HomePageWhyChooseUsSection'
import HomePageOurTechnology from '../components/HomePageOurTechnology'
import HomePageExploreNow from '../components/HomePageExploreNow'
import Footer from '../components/Footer'

function Homepage() {
  return (
    <div className='bg-[#c8e6d7] h-screen z-10 py-[20px]'>
      <Header className='z-0'/>
      <HomePageHeroSection className='z-10'/>
      <HomePageHowItWorks/>
      <HomePageWhyChooseUsSection/>
      <HomePageOurTechnology/>
      <HomePageExploreNow/>
      <Footer/>
    </div>
  )
}

export default Homepage