import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUserProfile } from '../../redux/profile';
import './ProfilePage.css';
import { useNavigate } from 'react-router-dom';
import SubscriptionComponent from '../SubscriptionComponent/SubscriptionComponent';

const ProfilePage = () => {
  const dispatch = useDispatch();
  const userProfile = useSelector((state) => state.profile.userProfile);
  const user = useSelector((state) => state.session.user);
  const navigate = useNavigate();
  const defaultProfilePic = 'https://uploads-ssl.webflow.com/5d6dde2cb8496e3f669a4b75/665e8d5f51c4aab200bca30f_profilepic.jpeg'; // Link to default profile image

  useEffect(() => {
    dispatch(fetchUserProfile());
  }, [dispatch]);

  if (!userProfile) {
    return <div>Loading...</div>;
  }

  const { student, parent } = userProfile;

  return (
    <div className="profile-page">
      {userProfile.type === 'Student' && student && (
        <>
          <div className="header-section">
          <img
              src={student.profile_pic || defaultProfilePic}
              alt="Profile"
              className="profile-pic"
            />
              <div className="header-info">
              <h2>{student.stage_name}</h2>
              <p><strong>Status:</strong> {user.status}</p>
              <p>{student.bio}</p>
              <div className="buttons-list">
                <button onClick={() => navigate('/profile/edit')}>Edit Profile</button>
                <button onClick={() => navigate('/profile/update')}>Update Genre or Type</button>
              </div>
            </div>
          </div>


          {(user.status === 'Pre-Apply') ? (
        <>
          <div className='card'>
            <h1>You need to apply to 7PACKS to apply to opportunities:</h1>
            <button onClick={() => navigate('/apply')}>Apply to 7Packs for Free</button>
          </div>
        </>
      ) : (
        <>
        </>
      )}

          {(user.status === 'Premium Monthly' || user.status === 'Premium Annual' || user.status === 'Accepted') ? (
        <SubscriptionComponent />
      ) : (
        <>
        </>
      )}
          <div className="profile-info">
            <div className="card">
              <h2>Contact Information</h2>
              <div className="info-grid">
                <p><strong>First Name:</strong> {student.first_name}</p>
                <p><strong>Last Name:</strong> {student.last_name}</p>
                <p><strong>Phone:</strong> {student.phone}</p>
                <p><strong>Address:</strong> {`${student.address_1} ${student.address_2 || ''}, ${student.city}, ${student.state} ${student.postal_code}`}</p>
                <p><strong>Portfolio URL:</strong> <a href={student.portfolio_url} target="_blank" rel="noopener noreferrer">{student.portfolio_url}</a></p>
                <p><strong>Previous Projects:</strong> {student.previous_projects}</p>
                <p><strong>Instagram:</strong> <a href={`https://instagram.com/${student.instagram}`} target="_blank" rel="noopener noreferrer">{student.instagram}</a></p>
                <p><strong>Twitter:</strong> <a href={`https://twitter.com/${student.twitter}`} target="_blank" rel="noopener noreferrer">{student.twitter}</a></p>
                <p><strong>Facebook:</strong> <a href={student.facebook} target="_blank" rel="noopener noreferrer">{student.facebook}</a></p>
                <p><strong>YouTube:</strong> <a href={student.youtube} target="_blank" rel="noopener noreferrer">{student.youtube}</a></p>
                <p><strong>Other Social Media:</strong> {student.other_social_media}</p>
                <p><strong>Reference Name:</strong> {student.reference_name}</p>
                <p><strong>Reference Email:</strong> {student.reference_email}</p>
                <p><strong>Reference Phone:</strong> {student.reference_phone}</p>
                <p><strong>Reference Relationship:</strong> {student.reference_relationship}</p>
              </div>

              <div className="genres-types">
                <div>
                  <strong>Genres:</strong>
                  {student.genres && student.genres.length > 0 ? (
                    <ul>
                      {student.genres.map((genre) => (
                        <li key={genre.id}>{genre.name}</li>
                      ))}
                    </ul>
                  ) : (
                    <p>No genres listed.</p>
                  )}
                </div>

                <div>
                  <strong>Types:</strong>
                  {student.types && student.types.length > 0 ? (
                    <ul>
                      {student.types.map((type) => (
                        <li key={type.id}>{type.name}</li>
                      ))}
                    </ul>
                  ) : (
                    <p>No types listed.</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {userProfile.type === 'Parent' && parent && (
        <>
          <div className="header-section">
            {parent.logo && <img src={parent.logo} alt="Logo" className="profile-pic" />}
            <div className="header-info">
              <h2>{parent.name}</h2>
              <p>{parent.bio}</p>
              <div className="buttons-list">
                <button onClick={() => navigate('/profile/edit')}>Edit Profile</button>
                <button onClick={() => navigate('/profile/update')}>Update Genre or Type</button>
              </div>
            </div>
          </div>
          <div className="profile-info">
            <div className="card">
              <h2>Parent Information</h2>
              <div>
                <p><strong>Name:</strong> {parent.name}</p>
                <p><strong>Bio:</strong> {parent.bio}</p>
                {/* Display other parent-specific information here */}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ProfilePage;



// import { useEffect } from 'react';
// import { useDispatch, useSelector } from 'react-redux';
// import { fetchUserProfile } from '../../redux/profile';
// import './ProfilePage.css';
// import { useNavigate } from 'react-router-dom';

// const ProfilePage = () => {
//   const dispatch = useDispatch();
//   const userProfile = useSelector((state) => state.profile.userProfile);
//   const user = useSelector((state) => state.session.user);
//   const navigate = useNavigate();

//   useEffect(() => {
//     dispatch(fetchUserProfile());
//   }, [dispatch]);

//   if (!userProfile) {
//     return <div>Loading...</div>;
//   }

//   const { student, parent } = userProfile;

//   return (
//     <div className="profile-page">
//       <h1>Profile Information</h1>
//       <div className='buttons-list'>
//       <button onClick={() => navigate('/profile/edit')}>Edit Profile</button>
//       <button onClick={() => navigate('/profile/update')}>Update Genre or Type</button>
//       </div>
//       {userProfile.type === 'Student' && student && (
//         <div className='profile-info'>
//           <h2>Student Profile</h2>
//           {student.profile_pic && <img src={student.profile_pic} alt="Profile" className='profile-pic'/>}
//           <p><strong>Status:</strong> {user.status}</p>
//           <p><strong>Stage Name:</strong> {student.stage_name}</p>
//           <p><strong>Bio:</strong> {student.bio}</p>
//           <p><strong>First Name:</strong> {student.first_name}</p>
//           <p><strong>Last Name:</strong> {student.last_name}</p>
//           <p><strong>Phone:</strong> {student.phone}</p>
//           <p><strong>Address:</strong> {`${student.address_1} ${student.address_2 || ''}, ${student.city}, ${student.state} ${student.postal_code}`}</p>
//           <p><strong>Portfolio URL:</strong> <a href={student.portfolio_url}>{student.portfolio_url}</a></p>
//           <p><strong>Previous Projects:</strong> {student.previous_projects}</p>
//           <p><strong>Instagram:</strong> <a href={`https://instagram.com/${student.instagram}`}>{student.instagram}</a></p>
//           <p><strong>Twitter:</strong> <a href={`https://twitter.com/${student.twitter}`}>{student.twitter}</a></p>
//           <p><strong>Facebook:</strong> <a href={student.facebook}>{student.facebook}</a></p>
//           <p><strong>YouTube:</strong> <a href={student.youtube}>{student.youtube}</a></p>
//           <p><strong>Other Social Media:</strong> {student.other_social_media}</p>
//           <p><strong>Reference Name:</strong> {student.reference_name}</p>
//           <p><strong>Reference Email:</strong> {student.reference_email}</p>
//           <p><strong>Reference Phone:</strong> {student.reference_phone}</p>
//           <p><strong>Reference Relationship:</strong> {student.reference_relationship}</p>
//           {/* Display Genres */}
//           <div>
//             <strong>Genres:</strong>
//             {student.genres && student.genres.length > 0 ? (
//               <ul>
//                 {student.genres.map((genre) => (
//                   <li key={genre.id}>{genre.name}</li>
//                 ))}
//               </ul>
//             ) : (
//               <p>No genres listed.</p>
//             )}
//           </div>
//           {/* Display Types */}
//           <div>
//             <strong>Types:</strong>
//             {student.types && student.types.length > 0 ? (
//               <ul>
//                 {student.types.map((type) => (
//                   <li key={type.id}>{type.name}</li>
//                 ))}
//               </ul>
//             ) : (
//               <p>No types listed.</p>
//             )}
//           </div>
//         </div>
//       )}
//       {userProfile.type === 'Parent' && parent && (
//         <div className='profile-info'>
//           <h2>Parent Profile</h2>
//           {parent.logo && <img src={parent.logo} alt="Logo" className='profile-pic'/>}
//           <p><strong>Name:</strong> {parent.name}</p>
//           <p><strong>Bio:</strong> {parent.bio}</p>
//           {/* Display other parent-specific information here */}
//         </div>
//       )}
//     </div>
//   );
// };

// export default ProfilePage;
