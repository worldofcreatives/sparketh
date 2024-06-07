// SubmissionDetails.jsx
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { fetchSpecificSubmission } from '../../redux/submissions';
import './SubmissionDetails.css';
import WithParentGuard from '../WithParentGuard/WithParentGuard';

const SubmissionDetails = () => {
  const { oppId, subId } = useParams();
  const dispatch = useDispatch();
  const { submission, loading, error } = useSelector((state) => state.submissions);

  useEffect(() => {
    if (oppId && subId) {
      dispatch(fetchSpecificSubmission(oppId, subId));
    }
  }, [dispatch, oppId, subId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!submission) return <div>Submission not found</div>;

  return (
    <div className="submission-details-container">
      <div className='submission-details'>
      <h2>Submission Details</h2>
      <p><strong>Name:</strong> {submission.name}</p>
      <p><strong>Status:</strong> {submission.status}</p>
      <p><strong>Notes:</strong> {submission.notes}</p>
      <p><strong>BPM:</strong> {submission.bpm}</p>
      <p><strong>Collaborators:</strong> {submission.collaborators}</p>
      {/* Add more details you want to display */}
      </div>
    </div>
  );
};

export default WithParentGuard(SubmissionDetails);

