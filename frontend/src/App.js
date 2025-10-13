import './App.css';
import { Routes, Route } from "react-router-dom"
import ChatDashboard from './pages/ChatDashboard';
import Login from './pages/Login';
import Signup from './pages/Signup';
import AuthProvider from './context/AuthContext';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePageHeroSection from './components/HomePageHeroSection';
import HomePageHowItWorks from './components/HomePageHowItWorks';
import Homepage from './pages/Homepage';
import HomePageWhyChooseUsSection from './components/HomePageWhyChooseUsSection';
import HowCuisiniseWorksPage from './pages/HowCuisiniseWorksPage';

function App() {

  return (
    <AuthProvider>
      <div >
        <Routes>
          <Route path="/" element={<Login/>}/>
          <Route path="/signup" element={<Signup/>}/>
          <Route path="/chat" element={<ChatDashboard/>}/>
          <Route path='/header' element={<Header/>}/>
          <Route path='/footer' element={<Footer/>}/>
          <Route path='/hero' element={<HomePageHeroSection/>}/>
          <Route path='/hiw' element={<HomePageHowItWorks/>}/>
          <Route path='/home' element={<Homepage/>}/>
          <Route path='wcu' element={<HomePageWhyChooseUsSection/>}/>
          <Route path='/how-it-works' element={<HowCuisiniseWorksPage/>}/>
        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;
