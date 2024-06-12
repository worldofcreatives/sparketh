import { useNavigate } from 'react-router-dom';

import './LandingPage.css';

const LandingPage = () => {

  const navigate = useNavigate();

  const navigateToSignup = () => {
    navigate('/signup');
  };



  return (
    <div className="landing-page">
      <header className="landing-header">
        <img src="https://uploads-ssl.webflow.com/5d6dde2cb8496e3f669a4b75/65eb381ae9b42d28e7f3d469_music-blob.jpg" alt="header-image" className="landing-header-img"/>
        <h1>Exclusive Opportunities for Talented Students</h1>
        <p>Explore the ultimate platform for artists, producers, and music lovers to get their foot in the door.</p>
        <button onClick={navigateToSignup}>Sign Up</button>
      </header>
        <a href="https://www.linkedin.com/in/ipaintidraw">👉 Connect with the guy who built this</a>
    </div>
  );
};

export default LandingPage;
