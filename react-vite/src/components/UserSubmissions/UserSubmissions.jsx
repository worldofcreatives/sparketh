import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import './UserSubmissions.css';

const UserSubmissions = () => {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const user = useSelector((state) => state.session.user);

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        const response = await fetch('/api/opportunities/submissions/user');
        if (response.ok) {
          const data = await response.json();
          setSubmissions(data);
        } else {
          setError('Failed to load submissions.');
        }
      } catch (err) {
        setError('An error occurred. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchSubmissions();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="user-submissions">
      <h1>Your Submissions</h1>
      {submissions.length === 0 ? (
        <p>No submissions found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Opportunity</th>
              <th>Status</th>
              <th>Notes</th>
              <th>BPM</th>
              <th>Collaborators</th>
              <th>Submitted At</th>
            </tr>
          </thead>
          <tbody>
            {submissions.map((submission) => (
              <tr key={submission.id}>
                <td>{submission.name}</td>
                <td>
                  <Link to={`/opportunities/${submission.opportunity_id}`}>
                    {submission.opportunity_name}
                  </Link>
                </td>
                <td>{submission.status}</td>
                <td className="notes">
                  <span title={submission.notes}>
                    {submission.notes.length > 30 ? `${submission.notes.substring(0, 30)} ...(hover over to read the rest)` : submission.notes}
                  </span>
                </td>
                <td>{submission.bpm}</td>
                <td>{submission.collaborators}</td>
                <td>{new Date(submission.created_date).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default UserSubmissions;
