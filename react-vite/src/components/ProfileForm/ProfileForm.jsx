import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUserProfile, updateProfile } from '../../redux/profile';
import "./ProfileForm.css";
import { useNavigate } from 'react-router-dom';

const ProfileForm = () => {
  const dispatch = useDispatch();
  const userProfile = useSelector((state) => state.profile.userProfile); // Make sure the path matches your Redux state
  const navigate = useNavigate();
  const [profileData, setProfileData] = useState({
    bio: '',
    profile_pic: null,
    logo: null,
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

  useEffect(() => {
    dispatch(fetchUserProfile()).then((userProfile) => {
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
      }
    });
  }, [dispatch]);

  const handleGenreChange = (e) => {
    const { value, checked } = e.target;
    setProfileData(prev => ({
      ...prev,
      genres: checked
        ? [...(Array.isArray(prev.genres) ? prev.genres : []), value] // Ensure prev.genres is always treated as an array
        : (Array.isArray(prev.genres) ? prev.genres : []).filter(genre => genre !== value),
    }));
  };

  const handleTypeChange = (e) => {
    const { value, checked } = e.target;
    setProfileData(prev => ({
      ...prev,
      types: checked
        ? [...(Array.isArray(prev.types) ? prev.types : []), value] // Ensure prev.types is always treated as an array
        : (Array.isArray(prev.types) ? prev.types : []).filter(type => type !== value),
    }));
  };


  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfileData({
      ...profileData,
      [name]: value,
    });
  };

  const handleFileChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.files[0],
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    Object.keys(profileData).forEach((key) => {
        if (Array.isArray(profileData[key])) {
            profileData[key].forEach(value => formData.append(key, value));
        } else if (profileData[key] !== null) {
            formData.append(key, profileData[key]);
        }
    });

    await dispatch(updateProfile(formData));
    navigate('/profile');
};


  if (!userProfile) {
    return <div>Loading...</div>;
  }

  return (
    <div className="profile-form-container">
    <form onSubmit={handleSubmit} className="profile-form">
      <div>
        <label htmlFor="bio">Bio:</label>
        <textarea id="bio" name="bio" value={profileData.bio} onChange={handleChange} />
      </div>
      {/* Conditionally render inputs based on user type */}
      {userProfile.type === 'Student' && (
        <>
          <div>
            <label htmlFor="profile_pic">Profile Picture:</label>
            <input type="file" id="profile_pic" name="profile_pic" onChange={handleFileChange} accept="image/*" />
          </div>
          <div>
            <label htmlFor="first_name">First Name:</label>
            <input type="text" id="first_name" name="first_name" value={profileData.first_name} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="last_name">Last Name:</label>
            <input type="text" id="last_name" name="last_name" value={profileData.last_name} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="stage_name">Stage Name:</label>
            <input type="text" id="stage_name" name="stage_name" value={profileData.stage_name} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="phone">Phone:</label>
            <input type="text" id="phone" name="phone" value={profileData.phone} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="address_1">Address 1:</label>
            <input type="text" id="address_1" name="address_1" value={profileData.address_1} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="address_2">Address 2 (optional):</label>
            <input type="text" id="address_2" name="address_2" value={profileData.address_2} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="city">City:</label>
            <input type="text" id="city" name="city" value={profileData.city} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="state">State:</label>
            <input type="text" id="state" name="state" value={profileData.state} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="postal_code">Postal Code:</label>
            <input type="text" id="postal_code" name="postal_code" value={profileData.postal_code} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="portfolio_url">Portfolio URL:</label>
            <input type="text" id="portfolio_url" name="portfolio_url" value={profileData.portfolio_url} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="previous_projects">Previous Projects:</label>
            <textarea id="previous_projects" name="previous_projects" value={profileData.previous_projects} onChange={handleChange} />
          </div>
              {/* Social Media Links */}
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

          {/* Reference Information */}
          <div>
            <label htmlFor="reference_name">Reference Name:</label>
            <input type="text" id="reference_name" name="reference_name" value={profileData.reference_name} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="reference_email">Reference Email:</label>
            <input type="email" id="reference_email" name="reference_email" value={profileData.reference_email} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="reference_phone">Reference Phone:</label>
            <input type="text" id="reference_phone" name="reference_phone" value={profileData.reference_phone} onChange={handleChange} />
          </div>
          <div>
            <label htmlFor="reference_relationship">Reference Relationship:</label>
            <input type="text" id="reference_relationship" name="reference_relationship" value={profileData.reference_relationship} onChange={handleChange} />
          </div>
              </>
            )}
            {userProfile.type === 'Parent' && (
              <div>
                <label htmlFor="logo">Parent Logo:</label>
                <input type="file" id="logo" name="logo" onChange={handleFileChange} accept="image/*" />
              </div>
            )}
            <button type="submit">Update Profile</button>
    </form>
    </div>
  );
};

export default ProfileForm;
