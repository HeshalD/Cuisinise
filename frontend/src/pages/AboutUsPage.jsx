import React from 'react'
import Header from '../components/Header'
import AboutCuisinise from '../components/AboutUsPageHeroSection'
import Footer from '../components/Footer'
import OurStorySection from '../components/AboutUsPageOurStorySection'
import OurAgents from '../components/AboutUsPageOurAgents'
import Technology from '../components/AboutUsPageTools&Technologies'

function AboutUsPage() {
  return (
    <div className='bg-[#d4ebe0] pt-[20px]'>
        <Header/>
        <AboutCuisinise/>
        <OurStorySection/>
        <OurAgents/>
        <Technology/>
        <Footer/>
    </div>
  )
}

export default AboutUsPage