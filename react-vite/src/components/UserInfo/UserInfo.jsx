import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUserById } from '../../redux/users'; // Adjust the import path according to your project structure
import { thunkUpdateUserStatus } from '../../redux/users';
import WithParentGuard from '../WithParentGuard/WithParentGuard';
import './UserInfo.css';


const UserInfo = () => {
  const { userId } = useParams(); // Get the user ID from URL
  const dispatch = useDispatch();
  const [currentStatus, setCurrentStatus] = useState('');

  useEffect(() => {
    if (userId) {
      dispatch(fetchUserById(userId)); // Fetch user info when component mounts or userId changes
    }
  }, [dispatch, userId]);

  // Select the current user from the Redux store
  const user = useSelector(state => state.users.currentUser);

  useEffect(() => {
    if (user) {
      setCurrentStatus(user.status);
    }
  }, [user]);

  const handleStatusUpdate = (status) => {
    dispatch(thunkUpdateUserStatus(userId, status));
    setCurrentStatus(status); // Update local state immediately
  };

  if (!user) {
    return <div>Loading user information...</div>;
  }

  return (
    <div>
      <h2>User Information</h2>
      <p><strong>Username:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Status:</strong> {currentStatus}</p>

      <button
        onClick={() => handleStatusUpdate('Accepted')}
        className={currentStatus === 'Accepted' ? 'highlighted' : ''}
      >
        Accept
      </button>
      <button
        onClick={() => handleStatusUpdate('Denied')}
        className={currentStatus === 'Denied' ? 'highlighted' : ''}
      >
        Deny
      </button>
      <button
        onClick={() => handleStatusUpdate('Pre-Apply')}
        className={currentStatus === 'Pre-Apply' ? 'highlighted' : ''}
      >
        Pre-Apply
      </button>
      <button
        onClick={() => handleStatusUpdate('Applied')}
        className={currentStatus === 'Applied' ? 'highlighted' : ''}
      >
        Applied
      </button>
      <button
        onClick={() => handleStatusUpdate('Premium Monthly')}
        className={currentStatus === 'Premium Monthly' ? 'highlighted' : ''}
      >
        Premium Monthly
      </button>
      <button
        onClick={() => handleStatusUpdate('Premium Annual')}
        className={currentStatus === 'Premium Annual' ? 'highlighted' : ''}
      >
        Premium Annual
      </button>

      <p><strong>Type:</strong> {user.type}</p>
      {user.student && (
        <>
          <h3>Student Information</h3>
          <p><strong>First Name:</strong> {user.student.first_name}</p>
          <p><strong>Last Name:</strong> {user.student.last_name}</p>
          <p><strong>Stage Name:</strong> {user.student.stage_name}</p>
          <p><strong>Bio:</strong> {user.student.bio}</p>
          <p><strong>Phone:</strong> {user.student.phone}</p>
          <p><strong>Address:</strong> {user.student.address}</p>
          <p><strong>Portfolio URL:</strong> {user.student.portfolio_url}</p>
          <p><strong>Previous Projects:</strong> {user.student.previous_projects}</p>
          <p><strong>Instagram:</strong> {user.student.instagram}</p>
          <p><strong>Twitter:</strong> {user.student.twitter}</p>
          <p><strong>Facebook:</strong> {user.student.facebook}</p>
          <p><strong>YouTube:</strong> {user.student.youtube}</p>
          <p><strong>Other Social Media:</strong> {user.student.other_social_media}</p>
          <p><strong>Reference Name:</strong> {user.student.reference_name}</p>
          <p><strong>Reference Email:</strong> {user.student.reference_email}</p>
          <p><strong>Reference Phone:</strong> {user.student.reference_phone}</p>
          <p><strong>Reference Relationship:</strong> {user.student.reference_relationship}</p>
          <p><strong>Genres:</strong> {user.student.genres.map(genre => genre.name).join(', ')}</p>
          <p><strong>Types:</strong> {user.student.types.map(type => type.name).join(', ')}</p>
        </>
      )}
    </div>
  );
};

export default WithParentGuard(UserInfo); // Wrap the component with the HOC


// import React, { useEffect } from 'react';
// import { useParams } from 'react-router-dom';
// import { useDispatch, useSelector } from 'react-redux';
// import { fetchUserById } from '../../redux/users'; // Adjust the import path according to your project structure
// import { thunkUpdateUserStatus } from '../../redux/users';
// import WithParentGuard from '../WithParentGuard/WithParentGuard';
// import './UserInfo.css';


// const UserInfo = () => {
//   const { userId } = useParams(); // Get the user ID from URL
//   const dispatch = useDispatch();

//   useEffect(() => {
//     if (userId) {
//       dispatch(fetchUserById(userId)); // Fetch user info when component mounts or userId changes
//     }
//   }, [dispatch, userId]);


//   // Select the current user from the Redux store
//   const user = useSelector(state => state.users.currentUser);

//   const handleStatusUpdate = (status) => {
//     dispatch(thunkUpdateUserStatus(userId, status));
//   };

//   if (!user) {
//     return <div>Loading user information...</div>;
//   }

//   return (
//     <div>
//       <h2>User Information</h2>
//       <p><strong>Username:</strong> {user.username}</p>
//       <p><strong>Email:</strong> {user.email}</p>
//       <p><strong>Status:</strong> {user.status}</p>

//       <button onClick={() => handleStatusUpdate('Accepted')}>Accept</button>
//       <button onClick={() => handleStatusUpdate('Denied')}>Deny</button>
//       <button onClick={() => handleStatusUpdate('Pre-Apply')}>Pre-Apply</button>
//       <button onClick={() => handleStatusUpdate('Applied')}>Applied</button>
//       <button onClick={() => handleStatusUpdate('Premium Monthly')}>Premium Monthly</button>
//       <button onClick={() => handleStatusUpdate('Premium Annual')}>Premium Annual</button>



//       <p><strong>Type:</strong> {user.type}</p>
//       {user.student && (
//         <>
//           <h3>Student Information</h3>
//           <p><strong>First Name:</strong> {user.student.first_name}</p>
//           <p><strong>Last Name:</strong> {user.student.last_name}</p>
//           <p><strong>Stage Name:</strong> {user.student.stage_name}</p>
//             <p><strong>Bio:</strong> {user.student.bio}</p>
//             <p><strong>Phone:</strong> {user.student.phone}</p>
//             <p><strong>Address:</strong> {user.student.address}</p>
//             <p><strong>Portfolio URL:</strong> {user.student.portfolio_url}</p>
//             <p><strong>Previous Projects:</strong> {user.student.previous_projects}</p>
//             <p><strong>Instagram:</strong> {user.student.instagram}</p>
//             <p><strong>Twitter:</strong> {user.student.twitter}</p>
//             <p><strong>Facebook:</strong> {user.student.facebook}</p>
//             <p><strong>YouTube:</strong> {user.student.youtube}</p>
//             <p><strong>Other Social Media:</strong> {user.student.other_social_media}</p>
//             <p><strong>Reference Name:</strong> {user.student.reference_name}</p>
//             <p><strong>Reference Email:</strong> {user.student.reference_email}</p>
//             <p><strong>Reference Phone:</strong> {user.student.reference_phone}</p>
//             <p><strong>Reference Relationship:</strong> {user.student.reference_relationship}</p>
//             <p><strong>Genres:</strong> {user.student.genres.map(genre => genre.name).join(', ')}</p>
//             <p><strong>Types:</strong> {user.student.types.map(type => type.name).join(', ')}</p>
//         </>
//       )}
//     </div>
//   );
// };

// export default WithParentGuard(UserInfo); // Wrap the component with the HOC
