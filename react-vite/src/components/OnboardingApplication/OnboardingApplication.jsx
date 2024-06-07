import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUserProfile, updateProfile, updateGenresAndTypes } from '../../redux/profile';
import { thunkUpdateUserStatus } from '../../redux/session';
import { useNavigate } from 'react-router-dom';
import './OnboardingApplication.css';

const GENRE_CHOICES = [
  { id: 1, name: "Afro" },
  { id: 2, name: "Country" },
  { id: 3, name: "Dancehall" },
  { id: 4, name: "Disco" },
  { id: 5, name: "Funk" },
  { id: 6, name: "Hip Hop" },
  { id: 7, name: "Latin" },
  { id: 8, name: "Neo Soul" },
  { id: 9, name: "Pop" },
  { id: 10, name: "R&B" },
  { id: 11, name: "Reggae" },
  { id: 12, name: "Rock" },
  { id: 13, name: "Other" },
];

const TYPE_CHOICES = [
  { id: 1, name: "Songwriter" },
  { id: 2, name: "Musician" },
  { id: 3, name: "Producer" },
  { id: 4, name: "Artist" },
];

const OnboardingApplication = () => {
  const dispatch = useDispatch();
  const userProfile = useSelector((state) => state.profile.userProfile);
  const navigate = useNavigate();
  const user = useSelector((state) => state.session.user);

  const [profileData, setProfileData] = useState({
    bio: '',
    profile_pic: null,
    first_name: '',
    last_name: '',
    stage_name: '',
    phone: '',
    address_1: '',
    address_2: '',
    city: '',
    state: '',
    postal_code: '',
    portfolio_url: '',
    previous_projects: '',
    instagram: '',
    twitter: '',
    facebook: '',
    youtube: '',
    other_social_media: '',
    reference_name: '',
    reference_email: '',
    reference_phone: '',
    reference_relationship: '',
  });

  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [currentStep, setCurrentStep] = useState(1);
  const [isNextEnabled, setIsNextEnabled] = useState(false);

  useEffect(() => {
    dispatch(fetchUserProfile()).then((userProfile) => {
      if (user && user.status !== "Pre-Apply") {
        navigate('/profile'); // Redirect if status is not Pre-Apply
      } else {
        if (userProfile && userProfile.type === 'Student') {
          const { student } = userProfile;
          setProfileData({
            bio: student.bio || '',
            first_name: student.first_name || '',
            last_name: student.last_name || '',
            stage_name: student.stage_name || '',
            phone: student.phone || '',
            address_1: student.address_1 || '',
            address_2: student.address_2 || '',
            city: student.city || '',
            state: student.state || '',
            postal_code: student.postal_code || '',
            portfolio_url: student.portfolio_url || '',
            previous_projects: student.previous_projects || '',
            instagram: student.instagram || '',
            twitter: student.twitter || '',
            facebook: student.facebook || '',
            youtube: student.youtube || '',
            other_social_media: student.other_social_media || '',
            reference_name: student.reference_name || '',
            reference_email: student.reference_email || '',
            reference_phone: student.reference_phone || '',
            reference_relationship: student.reference_relationship || '',
          });
          setSelectedGenres(student.genres.map(genre => genre.id));
          setSelectedTypes(student.types.map(type => type.id));
        }
      }
    });
  }, [dispatch]);

  useEffect(() => {
    validateCurrentStep();
  }, [profileData, selectedGenres, selectedTypes, currentStep]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleFileChange = (e) => {
    setProfileData(prev => ({
      ...prev,
      [e.target.name]: e.target.files[0],
    }));
  };

  const handleGenreChange = (e) => {
    const { value, checked } = e.target;
    const genreId = parseInt(value, 10);
    if (checked) {
      setSelectedGenres(prevGenres => [...prevGenres, genreId]);
    } else {
      setSelectedGenres(prevGenres => prevGenres.filter(id => id !== genreId));
    }
  };

  const handleTypeChange = (e) => {
    const { value, checked } = e.target;
    const typeId = parseInt(value, 10);
    if (checked) {
      setSelectedTypes(prevTypes => [...prevTypes, typeId]);
    } else {
      setSelectedTypes(prevTypes => prevTypes.filter(id => id !== typeId));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check for selected genres and types
    if (selectedGenres.length === 0 || selectedTypes.length === 0) {
      alert("Please select at least one genre and one type.");
      return; // Prevent form submission
    }

    // Prepare formData for profile and preferences update
    const formData = new FormData();
    Object.keys(profileData).forEach(key => {
      // Append all profile data except selectedGenres and selectedTypes
      if (key !== "selectedGenres" && key !== "selectedTypes") {
        formData.append(key, profileData[key]);
      }
    });

    // Append genres and types
    selectedGenres.forEach(genreId => formData.append("genres", genreId));
    selectedTypes.forEach(typeId => formData.append("types", typeId));

    try {
      // Update the profile
      await dispatch(updateProfile(formData));
      // Update genres and types preferences
      await dispatch(updateGenresAndTypes({ genres: selectedGenres, types: selectedTypes }));

      // Upon successful profile and preferences update, update the user's status to "Applied"
      await dispatch(thunkUpdateUserStatus());

      // Navigate to profile or another page as needed after the update
      navigate('/welcome');
    } catch (error) {
      console.error("Failed to update profile or status:", error);
      // Handle error (e.g., show an error message to the user)
    }
  };

  const validateCurrentStep = () => {
    let isValid = true;
    switch (currentStep) {
      case 1:
        isValid = profileData.first_name && profileData.last_name && profileData.stage_name &&
                  profileData.bio && profileData.phone && profileData.address_1 &&
                  profileData.city && profileData.state && profileData.postal_code;
        break;
      case 2:
        isValid = profileData.portfolio_url && profileData.previous_projects;
        break;
      case 3:
        isValid = profileData.reference_name && profileData.reference_email && profileData.reference_phone &&
                  profileData.reference_relationship && selectedGenres.length > 0 && selectedTypes.length > 0;
        break;
      default:
        isValid = false;
    }
    setIsNextEnabled(isValid);
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div>
            <h2>Step 1: Basic Information</h2>
            <div>
              <label htmlFor="first_name">First Name:</label>
              <input type="text" id="first_name" name="first_name" value={profileData.first_name} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="last_name">Last Name:</label>
              <input type="text" id="last_name" name="last_name" value={profileData.last_name} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="stage_name">Stage Name:</label>
              <input type="text" id="stage_name" name="stage_name" value={profileData.stage_name} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="profile_pic">Profile Picture:</label>
              <input type="file" id="profile_pic" name="profile_pic" onChange={handleFileChange} accept="image/*" />
            </div>
            <div>
              <label htmlFor="bio">Bio:</label>
              <textarea id="bio" name="bio" value={profileData.bio} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="phone">Phone:</label>
              <input type="text" id="phone" name="phone" value={profileData.phone} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="address_1">Address 1:</label>
              <input type="text" id="address_1" name="address_1" value={profileData.address_1} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="address_2">Address 2 (optional):</label>
              <input type="text" id="address_2" name="address_2" value={profileData.address_2} onChange={handleChange} />
            </div>
            <div>
              <label htmlFor="city">City:</label>
              <input type="text" id="city" name="city" value={profileData.city} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="state">State:</label>
              <input type="text" id="state" name="state" value={profileData.state} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="postal_code">Postal Code:</label>
              <input type="text" id="postal_code" name="postal_code" value={profileData.postal_code} onChange={handleChange} required />
            </div>
          </div>
        );
      case 2:
        return (
          <div>
            <h2>Step 2: Portfolio and Projects</h2>
            <div>
              <label htmlFor="portfolio_url">Portfolio URL:</label>
              <input type="text" id="portfolio_url" name="portfolio_url" value={profileData.portfolio_url} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="previous_projects">Previous Projects:</label>
              <textarea id="previous_projects" name="previous_projects" value={profileData.previous_projects} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="instagram">Instagram:</label>
              <input type="text" id="instagram" name="instagram" value={profileData.instagram} onChange={handleChange} />
            </div>
            <div>
              <label htmlFor="twitter">Twitter:</label>
              <input type="text" id="twitter" name="twitter" value={profileData.twitter} onChange={handleChange} />
            </div>
            <div>
              <label htmlFor="facebook">Facebook:</label>
              <input type="text" id="facebook" name="facebook" value={profileData.facebook} onChange={handleChange} />
            </div>
            <div>
              <label htmlFor="youtube">YouTube:</label>
              <input type="text" id="youtube" name="youtube" value={profileData.youtube} onChange={handleChange} />
            </div>
            <div>
              <label htmlFor="other_social_media">Other Social Media:</label>
              <textarea id="other_social_media" name="other_social_media" value={profileData.other_social_media} onChange={handleChange} />
            </div>
          </div>
        );
      case 3:
        return (
          <div>
            <h2>Step 3: References and Preferences</h2>
            <div>
              <label htmlFor="reference_name">Reference Name:</label>
              <input type="text" id="reference_name" name="reference_name" value={profileData.reference_name} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="reference_email">Reference Email:</label>
              <input type="email" id="reference_email" name="reference_email" value={profileData.reference_email} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="reference_phone">Reference Phone:</label>
              <input type="text" id="reference_phone" name="reference_phone" value={profileData.reference_phone} onChange={handleChange} required />
            </div>
            <div>
              <label htmlFor="reference_relationship">Reference Relationship:</label>
              <input type="text" id="reference_relationship" name="reference_relationship" value={profileData.reference_relationship} onChange={handleChange} required />
            </div>
            <fieldset>
              <legend>Choose Your Genres:</legend>
              {GENRE_CHOICES.map(genre => (
                <div key={genre.id} className="check-item">
                  <input
                    type="checkbox"
                    id={`genre-${genre.id}`}
                    name="genres"
                    value={genre.id}
                    checked={selectedGenres.includes(genre.id)}
                    onChange={handleGenreChange}
                  />
                  <label htmlFor={`genre-${genre.id}`}>{genre.name}</label>
                </div>
              ))}
            </fieldset>
            <fieldset>
              <legend>Choose Your Types:</legend>
              {TYPE_CHOICES.map(type => (
                <div key={type.id} className="check-item">
                  <input
                    type="checkbox"
                    id={`type-${type.id}`}
                    name="types"
                    value={type.id}
                    checked={selectedTypes.includes(type.id)}
                    onChange={handleTypeChange}
                  />
                  <label htmlFor={`type-${type.id}`}>{type.name}</label>
                </div>
              ))}
            </fieldset>
          </div>
        );
      default:
        return null;
    }
  };

  const nextStep = () => {
    setCurrentStep(prevStep => prevStep + 1);
  };

  const prevStep = () => {
    setCurrentStep(prevStep => prevStep - 1);
  };

  return (
    <div className="onboarding-application">
      <h1>Apply to 7Packs</h1>
      <p>The opportunity you've been waiting for is right around this corner.</p>
      <div className="step-indicator">
        <span className={currentStep === 1 ? 'active' : ''}>Step 1</span>
        <span className={currentStep === 2 ? 'active' : ''}>Step 2</span>
        <span className={currentStep === 3 ? 'active' : ''}>Step 3</span>
      </div>
      <form onSubmit={handleSubmit}>
        {renderStepContent()}
        <div className="navigation-buttons">
          {currentStep > 1 && <button type="button" onClick={prevStep}>Previous</button>}
          {currentStep < 3 && <button type="button" onClick={nextStep} disabled={!isNextEnabled}>Next</button>}
          {currentStep === 3 && <button type="submit" disabled={!isNextEnabled}>Submit</button>}
        </div>
      </form>
    </div>
  );
};

export default OnboardingApplication;





// import React, { useEffect, useState } from 'react';
// import { useDispatch, useSelector } from 'react-redux';
// import { fetchUserProfile, updateProfile, updateGenresAndTypes } from '../../redux/profile';
// import { thunkUpdateUserStatus } from '../../redux/session';
// import { useNavigate } from 'react-router-dom';
// import "./OnboardingApplication.css";

// const GENRE_CHOICES = [
//   { id: 1, name: "Afro" },
//   { id: 2, name: "Country" },
//   { id: 3, name: "Dancehall" },
//   { id: 4, name: "Disco" },
//   { id: 5, name: "Funk" },
//   { id: 6, name: "Hip Hop" },
//   { id: 7, name: "Latin" },
//   { id: 8, name: "Neo Soul" },
//   { id: 9, name: "Pop" },
//   { id: 10, name: "R&B" },
//   { id: 11, name: "Reggae" },
//   { id: 12, name: "Rock" },
//   { id: 13, name: "Other" },
// ];

// const TYPE_CHOICES = [
//   { id: 1, name: "Songwriter" },
//   { id: 2, name: "Musician" },
//   { id: 3, name: "Producer" },
//   { id: 4, name: "Artist" },
// ];

// const OnboardingApplication = () => {
//   const dispatch = useDispatch();
//   const userProfile = useSelector((state) => state.profile.userProfile);
//   const navigate = useNavigate();
//   const user = useSelector((state) => state.session.user);

//   const [profileData, setProfileData] = useState({
//     bio: '',
//     profile_pic: null,
//     first_name: '',
//     last_name: '',
//     stage_name: '',
//     phone: '',
//     address_1: '',
//     address_2: '',
//     city: '',
//     state: '',
//     postal_code: '',
//     portfolio_url: '',
//     previous_projects: '',
//     instagram: '',
//     twitter: '',
//     facebook: '',
//     youtube: '',
//     other_social_media: '',
//     reference_name: '',
//     reference_email: '',
//     reference_phone: '',
//     reference_relationship: '',
//   });

//   const [selectedGenres, setSelectedGenres] = useState([]);
//   const [selectedTypes, setSelectedTypes] = useState([]);

//   useEffect(() => {
//     dispatch(fetchUserProfile()).then((userProfile) => {
//       if (user && user.status !== "Pre-Apply") {
//         navigate('/profile'); // Redirect if status is not Pre-Apply
//       } else {
//         if (userProfile && userProfile.type === 'Student') {
//           const { student } = userProfile;
//           setProfileData({
//             bio: student.bio || '',
//             first_name: student.first_name || '',
//             last_name: student.last_name || '',
//             stage_name: student.stage_name || '',
//             phone: student.phone || '',
//             address_1: student.address_1 || '',
//             address_2: student.address_2 || '',
//             city: student.city || '',
//             state: student.state || '',
//             postal_code: student.postal_code || '',
//             portfolio_url: student.portfolio_url || '',
//             previous_projects: student.previous_projects || '',
//             instagram: student.instagram || '',
//             twitter: student.twitter || '',
//             facebook: student.facebook || '',
//             youtube: student.youtube || '',
//             other_social_media: student.other_social_media || '',
//             reference_name: student.reference_name || '',
//             reference_email: student.reference_email || '',
//             reference_phone: student.reference_phone || '',
//             reference_relationship: student.reference_relationship || '',
//           });
//           setSelectedGenres(student.genres.map(genre => genre.id));
//           setSelectedTypes(student.types.map(type => type.id));
//         }
//       }
//     });
//   }, [dispatch]);

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setProfileData(prev => ({
//       ...prev,
//       [name]: value,
//     }));
//   };

//   const handleFileChange = (e) => {
//     setProfileData(prev => ({
//       ...prev,
//       [e.target.name]: e.target.files[0],
//     }));
//   };

//   const handleGenreChange = (e) => {
//     const { value, checked } = e.target;
//     const genreId = parseInt(value, 10);
//     if (checked) {
//       setSelectedGenres(prevGenres => [...prevGenres, genreId]);
//     } else {
//       setSelectedGenres(prevGenres => prevGenres.filter(id => id !== genreId));
//     }
//   };

//   const handleTypeChange = (e) => {
//     const { value, checked } = e.target;
//     const typeId = parseInt(value, 10);
//     if (checked) {
//       setSelectedTypes(prevTypes => [...prevTypes, typeId]);
//     } else {
//       setSelectedTypes(prevTypes => prevTypes.filter(id => id !== typeId));
//     }
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     // Check for selected genres and types
//     if (selectedGenres.length === 0 || selectedTypes.length === 0) {
//       alert("Please select at least one genre and one type.");
//       return; // Prevent form submission
//     }

//     // Prepare formData for profile and preferences update
//     const formData = new FormData();
//     Object.keys(profileData).forEach(key => {
//       // Append all profile data except selectedGenres and selectedTypes
//       if (key !== "selectedGenres" && key !== "selectedTypes") {
//         formData.append(key, profileData[key]);
//       }
//     });

//     // Append genres and types
//     selectedGenres.forEach(genreId => formData.append("genres", genreId));
//     selectedTypes.forEach(typeId => formData.append("types", typeId));

//     try {
//       // Update the profile
//       await dispatch(updateProfile(formData));
//       // Update genres and types preferences
//       await dispatch(updateGenresAndTypes({ genres: selectedGenres, types: selectedTypes }));

//       // Upon successful profile and preferences update, update the user's status to "Applied"
//       await dispatch(thunkUpdateUserStatus());

//       // Navigate to profile or another page as needed after the update
//       navigate('/profile');
//     } catch (error) {
//       console.error("Failed to update profile or status:", error);
//       // Handle error (e.g., show an error message to the user)
//     }
//   };

//   if (!userProfile) {
//     return <div>Loading...</div>;
//   }

//   // Form rendering logic remains mostly the same, with added genre and type selection for both user types
//   return (
//     <form onSubmit={handleSubmit}>
//       <div>
//         <label htmlFor="first_name">First Name:</label>
//         <input type="text" id="first_name" name="first_name" value={profileData.first_name} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="last_name">Last Name:</label>
//         <input type="text" id="last_name" name="last_name" value={profileData.last_name} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="stage_name">Stage Name:</label>
//         <input type="text" id="stage_name" name="stage_name" value={profileData.stage_name} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="profile_pic">Profile Picture:</label>
//         <input type="file" id="profile_pic" name="profile_pic" onChange={handleFileChange} accept="image/*" />
//       </div>
//       <div>
//         <label htmlFor="bio">Bio:</label>
//         <textarea id="bio" name="bio" value={profileData.bio} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="phone">Phone:</label>
//         <input type="text" id="phone" name="phone" value={profileData.phone} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="address_1">Address 1:</label>
//         <input type="text" id="address_1" name="address_1" value={profileData.address_1} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="address_2">Address 2 (optional):</label>
//         <input type="text" id="address_2" name="address_2" value={profileData.address_2} onChange={handleChange} />
//       </div>
//       <div>
//         <label htmlFor="city">City:</label>
//         <input type="text" id="city" name="city" value={profileData.city} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="state">State:</label>
//         <input type="text" id="state" name="state" value={profileData.state} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="postal_code">Postal Code:</label>
//         <input type="text" id="postal_code" name="postal_code" value={profileData.postal_code} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="portfolio_url">Portfolio URL:</label>
//         <input type="text" id="portfolio_url" name="portfolio_url" value={profileData.portfolio_url} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="previous_projects">Previous Projects:</label>
//         <textarea id="previous_projects" name="previous_projects" value={profileData.previous_projects} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="instagram">Instagram:</label>
//         <input type="text" id="instagram" name="instagram" value={profileData.instagram} onChange={handleChange} />
//       </div>
//       <div>
//         <label htmlFor="twitter">Twitter:</label>
//         <input type="text" id="twitter" name="twitter" value={profileData.twitter} onChange={handleChange} />
//       </div>
//       <div>
//         <label htmlFor="facebook">Facebook:</label>
//         <input type="text" id="facebook" name="facebook" value={profileData.facebook} onChange={handleChange} />
//       </div>
//       <div>
//         <label htmlFor="youtube">YouTube:</label>
//         <input type="text" id="youtube" name="youtube" value={profileData.youtube} onChange={handleChange} />
//       </div>
//       <div>
//         <label htmlFor="other_social_media">Other Social Media:</label>
//         <textarea id="other_social_media" name="other_social_media" value={profileData.other_social_media} onChange={handleChange} />
//       </div>
//       <div>
//         <label htmlFor="reference_name">Reference Name:</label>
//         <input type="text" id="reference_name" name="reference_name" value={profileData.reference_name} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="reference_email">Reference Email:</label>
//         <input type="email" id="reference_email" name="reference_email" value={profileData.reference_email} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="reference_phone">Reference Phone:</label>
//         <input type="text" id="reference_phone" name="reference_phone" value={profileData.reference_phone} onChange={handleChange} required />
//       </div>
//       <div>
//         <label htmlFor="reference_relationship">Reference Relationship:</label>
//         <input type="text" id="reference_relationship" name="reference_relationship" value={profileData.reference_relationship} onChange={handleChange} required />
//       </div>
//       <fieldset>
//         <legend>Choose Your Genres:</legend>
//         {GENRE_CHOICES.map(genre => (
//           <div key={genre.id} className="check-item">
//             <input
//               type="checkbox"
//               id={`genre-${genre.id}`}
//               name="genres"
//               value={genre.id}
//               checked={selectedGenres.includes(genre.id)}
//               onChange={handleGenreChange}
//             />
//             <label htmlFor={`genre-${genre.id}`}>{genre.name}</label>
//           </div>
//         ))}
//       </fieldset>
//       <fieldset>
//         <legend>Choose Your Types:</legend>
//         {TYPE_CHOICES.map(type => (
//           <div key={type.id} className="check-item">
//             <input
//               type="checkbox"
//               id={`type-${type.id}`}
//               name="types"
//               value={type.id}
//               checked={selectedTypes.includes(type.id)}
//               onChange={handleTypeChange}
//             />
//             <label htmlFor={`type-${type.id}`}>{type.name}</label>
//           </div>
//         ))}
//       </fieldset>

//       <button type="submit">Submit</button>
//     </form>
//   );
// };

// export default OnboardingApplication;
