import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate, useParams } from 'react-router-dom';
import { fetchSubmissionsForOpportunity, updateSubmissionStatus } from '../../redux/submissions';
import SubmissionItem from '../SubmissionItem';
import MusicPlayer from '../MusicPlayer/MusicPlayer';
import './Submissions.css';
import Waveform from '../Waveform';
import WithParentGuard from '../WithParentGuard/WithParentGuard';

const Submissions = () => {
  const { oppId } = useParams();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.session);
  const { submissions, loading, error } = useSelector((state) => state.submissions);
  const isParent = user && user.type === 'Parent';
  const [currentSong, setCurrentSong] = useState({ url: '', name: '' });
  const [currentStatusFilter, setCurrentStatusFilter] = useState('');
  const navigate = useNavigate();
  const [playingSubmissionId, setPlayingSubmissionId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [minBpm, setMinBpm] = useState(0);
  const [maxBpm, setMaxBpm] = useState(200);
  const [currentSubmissionStatus, setCurrentSubmissionStatus] = useState('');

  // Whenever the playingSubmissionId changes, update the currentSubmissionStatus
  useEffect(() => {
    const currentSubmission = submissions.find(sub => sub.id === playingSubmissionId);
    setCurrentSubmissionStatus(currentSubmission ? currentSubmission.status : '');
  }, [playingSubmissionId, submissions]);


  useEffect(() => {
    if (isParent || user) dispatch(fetchSubmissionsForOpportunity(oppId));
  }, [dispatch, oppId, isParent, user]);

  const playSong = (songUrl, songName, submissionId) => {
    if (currentSong.url === songUrl && playingSubmissionId === submissionId) {
      setCurrentSong({ url: '', name: '' });
      setPlayingSubmissionId(null); // Reset the playing ID
    } else {
      setCurrentSong({ url: songUrl, name: songName });
      setPlayingSubmissionId(submissionId);
    }
  };

  const filteredSubmissions = submissions.filter(submission => {
    const matchesStatus = currentStatusFilter ? submission.status === currentStatusFilter : true;
    // Ensure username and name are not undefined before calling toLowerCase
    const username = submission.username || '';
    const name = submission.name || '';
    const matchesSearch = username.toLowerCase().includes(searchQuery.toLowerCase()) || name.toLowerCase().includes(searchQuery.toLowerCase());
    const bpm = parseInt(submission.bpm, 10) || 0; // Ensure bpm is a number and provide a default if undefined
    const matchesBpm = bpm >= minBpm && (!maxBpm || bpm <= maxBpm);
    return matchesStatus && matchesSearch && matchesBpm;
  });


  // Function to handle BPM input changes
  const handleMinBpmChange = (e) => {
    setMinBpm(e.target.value ? parseInt(e.target.value, 10) : 0);
  };

  const handleMaxBpmChange = (e) => {
    setMaxBpm(e.target.value ? parseInt(e.target.value, 10) : 200);
  };

  // Function to handle search input changes
  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const playStatus = (status) => {
    setCurrentStatusFilter(status);
  };

  const getNextSubmissionIndex = (direction) => {
    const currentIndex = filteredSubmissions.findIndex(submission => submission.id === playingSubmissionId);
    let nextIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;
    if (nextIndex >= filteredSubmissions.length) nextIndex = 0;
    if (nextIndex < 0) nextIndex = filteredSubmissions.length - 1;
    return nextIndex;
  };

  const handleSkip = () => {
    const nextIndex = getNextSubmissionIndex('next');
    const nextSong = filteredSubmissions[nextIndex];
    playSong(nextSong.file_url, nextSong.name, nextSong.id);
  };

  const handleBack = () => {
    const prevIndex = getNextSubmissionIndex('prev');
    const prevSong = filteredSubmissions[prevIndex];
    playSong(prevSong.file_url, prevSong.name, prevSong.id);
  };

  const handleAccept = () => {
    if (playingSubmissionId) {
      const newStatus = currentSubmissionStatus === 'Accepted' ? 'Pending' : 'Accepted';
      dispatch(updateSubmissionStatus(oppId, playingSubmissionId, newStatus))
        .then(() => {
          setCurrentSubmissionStatus(newStatus);
          console.log("Status updated to:", newStatus);
        });
    }
  };

  const handleReject = () => {
    if (playingSubmissionId) {
      const newStatus = currentSubmissionStatus === 'Rejected' ? 'Pending' : 'Rejected';
      dispatch(updateSubmissionStatus(oppId, playingSubmissionId, newStatus))
        .then(() => {
          setCurrentSubmissionStatus(newStatus);
          console.log("Status updated to:", newStatus);
        });
    }
  };


  const handleDownloadCurrentSong = () => {
    const currentSubmission = submissions.find(submission => submission.id === playingSubmissionId);
    if (currentSubmission) {
      // Trigger the download for the current submission
      // This will use the logic you've already defined in SubmissionItem for downloads
      // You might need to abstract that logic into a utility function that both components can use
    }
  };

console.log(playingSubmissionId)
console.log(currentSong)


useEffect(() => {
  const handleKeyDown = (event) => {
    switch (event.key) {
      case 'ArrowLeft':
        handleBack();
        break;
      case 'ArrowRight':
        handleSkip();
        break;
      case 'ArrowUp':
        if (playingSubmissionId) {
          event.preventDefault(); // Prevent scrolling
          // Change status to "Accepted"
          dispatch(updateSubmissionStatus(oppId, playingSubmissionId, 'Accepted')).then(() => {
            // After updating, you may need to refresh the submissions list or handle UI update
            // This is just a placeholder, replace it with actual logic as needed
            console.log('Status updated to Accepted');
          });
        }
        break;
      case 'ArrowDown':
        if (playingSubmissionId) {
          event.preventDefault(); // Prevent scrolling
          // Change status to "Rejected"
          dispatch(updateSubmissionStatus(oppId, playingSubmissionId, 'Rejected')).then(() => {
            // After updating, you may need to refresh the submissions list or handle UI update
            // This is just a placeholder, replace it with actual logic as needed
            console.log('Status updated to Rejected');
          });
        }
        break;
      default:
        break;
    }
  };

  document.addEventListener('keydown', handleKeyDown);

  // Cleanup function to remove the event listener
  return () => {
    document.removeEventListener('keydown', handleKeyDown);
  };
}, [dispatch, oppId, playingSubmissionId, handleBack, handleSkip]); // Make sure to include all dependencies here




  const statusButtons = ['All Submissions', 'Pending', 'Reviewing', 'Accepted', 'Rejected'].map(status => (
    <button key={status} onClick={() => playStatus(status === 'All Submissions' ? '' : status)}>{status}</button>
  ));

const downloadAllFiles = async () => {
  // Directly use filteredSubmissions since it already contains the submission objects you need
  try {
    const response = await fetch(`/api/aws/download-all/packtune`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // Send the full submission objects
      body: JSON.stringify(filteredSubmissions)
    });

    if (!response.ok) {
      throw new Error(`Failed to download files: ${response.statusText}`);
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    const statusText = currentStatusFilter ? currentStatusFilter : 'all';
    link.download = `submissions-${statusText}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error(`Error during bulk file download: ${error.message}`);
  }
};



const handleStatusChange = (status) => {
  setCurrentStatusFilter(status === 'All Submissions' ? '' : status);
};

// Dynamically apply a 'highlighted' class to the active tab
const getButtonClass = (status) => {
  const isActive = (status === 'All Submissions' && currentStatusFilter === '') || currentStatusFilter === status;
  return isActive ? 'tab-active' : 'tab-inactive';
};

  if (loading) return <div>Loading submissions...</div>;
  if (error) {
    navigate('/opps');
    return <div>You are not authorized to view these submissions.</div>;
  }

  return (
    <div className='sub-page'>
      <div className='sub-top'>
        <h2>Submissions</h2>
        <div className='tab-bar'>
          {['All Submissions', 'Pending', 'Accepted', 'Rejected'].map(status => (
            <button
              key={status}
              onClick={() => handleStatusChange(status)}
              className={getButtonClass(status)} // Apply the dynamic class here
            >
              {status}
            </button>
          ))}
        </div>
        <div className='search-download-sec'>
          <input
            type="text"
            placeholder="Search by name or username..."
            value={searchQuery}
            onChange={handleSearchChange}
            className='sub-search'
            />
          <button onClick={downloadAllFiles} className="download-all-button">
            Download All {currentStatusFilter || 'Submissions'}
          </button>
        </div>
        {filteredSubmissions.map(submission => (
          <SubmissionItem
            key={`${submission.id}-${submission.status}`} // Change here
            submission={submission}
            onPlay={() => playSong(submission.file_url, submission.name, submission.id)}
            isPlaying={submission.id === playingSubmissionId}
          />
        ))}
      </div>
      {/* <Waveform audioUrl={currentSong.url} /> */}
      {currentSong.url && (
        <div className="music-player-wrapper">
          <MusicPlayer
            audioUrl={currentSong.url}
            songName={currentSong.name}
            onBack={handleBack}
            onSkip={handleSkip}
            onAccept={handleAccept}
            onReject={handleReject}
            onDownload={handleDownloadCurrentSong}
            currentStatus={currentSubmissionStatus}
          />
        </div>
      )}
    </div>
  );

};

export default WithParentGuard(Submissions); // Wrap the component with the HOC
