import { useEffect, useState } from 'react';
import OpportunitiesChart from '../OpportunitiesChart';
import SubmissionsChart from '../SubmissionsChart';
import './Charts.css'; // Assuming your styles are here
import UsersChart from '../UsersChart';
import WithParentGuard from '../WithParentGuard/WithParentGuard';

const Charts = () => {
  // State to track which chart is currently selected
  const [selectedChart, setSelectedChart] = useState(localStorage.getItem('selectedChart') || 'opportunities');

  useEffect(() => {
    localStorage.setItem('selectedChart', selectedChart);
  }, [selectedChart]);

  return (
    <div>
      <button
        onClick={() => setSelectedChart('opportunities')}
        className={selectedChart === 'opportunities' ? 'active' : ''}
      >
        Opportunities Chart
      </button>
      <button
        onClick={() => setSelectedChart('submissions')}
        className={selectedChart === 'submissions' ? 'active' : ''}
      >
        Submissions Chart
      </button>
      <button
        onClick={() => setSelectedChart('users')}
        className={selectedChart === 'users' ? 'active' : ''}
      >
        Users Chart
      </button>

      {selectedChart === 'opportunities' && <OpportunitiesChart />}
      {selectedChart === 'submissions' && <SubmissionsChart />}
      {selectedChart === 'users' && <UsersChart />}
    </div>
  );
};

export default WithParentGuard(Charts); // Wrap the component with the HOC
