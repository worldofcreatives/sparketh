import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { createNewSubmission } from '../../redux/submissions';
import { useNavigate } from 'react-router-dom';
import "./SubmissionForm.css";

const SubmissionForm = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector((state) => state.session.user);

  const [submissionData, setSubmissionData] = useState({
    // Your form fields here
    name: '',
    notes: '',
    bpm: '',
    collaborators: '',
    file: null,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSubmissionData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleFileChange = (e) => {
    setSubmissionData((prev) => ({
      ...prev,
      file: e.target.files[0],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    Object.keys(submissionData).forEach((key) => {
      formData.append(key, submissionData[key]);
    });
    await dispatch(createNewSubmission(formData));
  };

  const renderSubmitButton = () => {
    if (user.type === 'Parent' || user.status === 'Accepted' || user.status === 'Premium') {
      return <button type="submit" className="submit-button">Submit</button>;
    } else if (user.status === 'Pre-Apply' || user.status === 'Denied') {
      return (
        <button type="button" className="submit-button" onClick={() => navigate('/apply')}>
          Want to submit your music? Click here to apply to 7packs
        </button>
      );
    } else if (user.status === 'Applied') {
      return (
        <button type="button" className="submit-button" disabled onClick={() => navigate('/apply')}>
          Want to submit your music? Your 7packs application is pending
        </button>
      );
    }
  };


  return (
    <form onSubmit={handleSubmit}>
      {/* Your form fields here */}
      <div>
        <label htmlFor="name">Name:</label>
        <input type="text" id="name" name="name" value={submissionData.name} onChange={handleChange} required />
      </div>
      <div>
        <label htmlFor="notes">Notes:</label>
        <textarea id="notes" name="notes" value={submissionData.notes} onChange={handleChange} />
      </div>
      <div>
        <label htmlFor="bpm">BPM:</label>
        <input type="number" id="bpm" name="bpm" value={submissionData.bpm} onChange={handleChange} />
      </div>
      <div>
        <label htmlFor="collaborators">Collaborators:</label>
        <input type="text" id="collaborators" name="collaborators" value={submissionData.collaborators} onChange={handleChange} />
      </div>
      <div>
        <label htmlFor="file">File:</label>
        <input type="file" id="file" name="file" onChange={handleFileChange} />
      </div>

      {renderSubmitButton()}
    </form>
  );
};

export default SubmissionForm;


// import { useEffect, useState } from 'react';
// import { useDispatch, useSelector } from 'react-redux';
// import { createNewSubmission } from '../../redux/submissions';
// import { useLocation, useNavigate } from 'react-router-dom';
// import "./SubmissionForm.css";

// const SubmissionForm = ({ opportunityId }) => {
//   const dispatch = useDispatch();
//   const [submissionDetails, setSubmissionDetails] = useState({
//     name: '',
//     notes: '',
//     bpm: '',
//     collaborators: '',
//     file: null,
//   });
//   const location = useLocation();
//   const navigate = useNavigate();
//   const [loading, setLoading] = useState(false);
//   const [successMessage, setSuccessMessage] = useState('');
//   const [errorMessage, setErrorMessage] = useState('');
//   const user = useSelector((state) => state.session.user);
//   const [submissionCount, setSubmissionCount] = useState(0);
//   const [hasSubmittedToOpportunity, setHasSubmittedToOpportunity] = useState(false);

//   useEffect(() => {
//     const fetchSubmissionData = async () => {
//       const countResponse = await fetch(`/api/opportunities/${opportunityId}/submissions/count`);
//       const countData = await countResponse.json();
//       setSubmissionCount(countData.submission_count);

//       const submissionResponse = await fetch(`/api/opportunities/${opportunityId}/submissions/user`);
//       const submissionData = await submissionResponse.json();
//       setHasSubmittedToOpportunity(submissionData.has_submitted);
//     };

//     if (user.status === 'Accepted' || user.status === 'Premium Monthly' || user.status === 'Premium Annual') {
//       fetchSubmissionData();
//     }
//   }, [user.status, opportunityId]);

//   useEffect(() => {
//     setSuccessMessage('');
//     setErrorMessage('');
//   }, [location]);

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setSubmissionDetails({
//       ...submissionDetails,
//       [name]: value,
//     });
//   };

//   const handleFileChange = (e) => {
//     setSubmissionDetails({
//       ...submissionDetails,
//       file: e.target.files[0],
//     });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setLoading(true);
//     setSuccessMessage('');
//     setErrorMessage('');

//     const formData = new FormData();
//     formData.append('name', submissionDetails.name);
//     formData.append('notes', submissionDetails.notes);
//     formData.append('bpm', submissionDetails.bpm);
//     formData.append('collaborators', submissionDetails.collaborators);
//     if (submissionDetails.file) {
//       formData.append('file', submissionDetails.file);
//     }

//     try {
//       if (user.status === 'Accepted' || user.status === 'Premium Monthly' || user.status === 'Premium Annual') {
//         if (user.status === 'Accepted' && submissionCount >= 3) {
//           setErrorMessage('Submission limit reached for the current month.');
//           setLoading(false);
//           return;
//         }
//         if ((user.status === 'Premium Monthly' || user.status === 'Premium Annual') && submissionCount >= 30) {
//           setErrorMessage('Submission limit reached for the current month.');
//           setLoading(false);
//           return;
//         }
//         if (hasSubmittedToOpportunity) {
//           setErrorMessage('You have already submitted to this opportunity.');
//           setLoading(false);
//           return;
//         }
//       }

//       await dispatch(createNewSubmission(formData, opportunityId));
//       setSuccessMessage('Submission created successfully!');
//       setSubmissionDetails({
//         name: '',
//         notes: '',
//         bpm: '',
//         collaborators: '',
//         file: null,
//       });
//     } catch (error) {
//       setErrorMessage(error.message || 'Failed to submit the form.');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const renderSubmitButton = () => {
//     if (user.type === 'Parent' || user.status === 'Accepted' || user.status === 'Premium Monthly' || user.status === 'Premium Annual' || user.status === 'Major7eague') {
//       return <button className='submit-button' type="submit">Submit</button>;
//     } else if (user.status === 'Pre-Apply' || user.status === 'Denied') {
//       return (
//         <button className='submit-button' type="button" onClick={() => navigate('/apply')}>
//           Want to submit your music? Click here to apply to 7packs
//         </button>
//       );
//     } else if (user.status === 'Applied') {
//       return (
//         <button className='submit-button' type="button" disabled onClick={() => navigate('/apply')}>
//           Your 7packs application is pending. Only approved students can apply to opps.
//         </button>
//       );
//     }
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <div>
//         <label htmlFor="name">Name:</label>
//         <input
//           id="name"
//           name="name"
//           value={submissionDetails.name}
//           onChange={handleChange}
//           type='text'
//           required
//         />
//       </div>
//       <div>
//         <label htmlFor="notes">Notes:</label>
//         <textarea
//           id="notes"
//           name="notes"
//           value={submissionDetails.notes}
//           onChange={handleChange}
//         />
//       </div>
//       <div>
//         <label htmlFor="bpm">BPM:</label>
//         <input
//           type="number"
//           id="bpm"
//           name="bpm"
//           value={submissionDetails.bpm}
//           onChange={handleChange}
//         />
//       </div>
//       <div>
//         <label htmlFor="collaborators">Collaborators:</label>
//         <input
//           type="text"
//           id="collaborators"
//           name="collaborators"
//           value={submissionDetails.collaborators}
//           onChange={handleChange}
//         />
//       </div>
//       <div>
//         <label htmlFor="file">Audio:</label>
//         <input
//           type="file"
//           id="file"
//           name="file"
//           accept=".mp3, .wav"
//           onChange={handleFileChange}
//           required
//         />
//       </div>
//       {renderSubmitButton()}
//       {successMessage && <div>{successMessage}</div>}
//       {errorMessage && <div className="error">{errorMessage}</div>}
//     </form>
//   );
// };

// export default SubmissionForm;
