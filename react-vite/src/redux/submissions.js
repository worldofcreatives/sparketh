//*====> Action Types <====
export const CREATE_SUBMISSION_REQUEST = 'submissions/createSubmissionRequest';
export const CREATE_SUBMISSION_SUCCESS = 'submissions/createSubmissionSuccess';
export const CREATE_SUBMISSION_FAILURE = 'submissions/createSubmissionFailure';
export const FETCH_SUBMISSIONS_REQUEST = 'submissions/fetchSubmissionsRequest';
export const FETCH_SUBMISSIONS_SUCCESS = 'submissions/fetchSubmissionsSuccess';
export const FETCH_SUBMISSIONS_FAILURE = 'submissions/fetchSubmissionsFailure';
export const FETCH_SPECIFIC_SUBMISSION_REQUEST = 'submissions/fetchSpecificSubmissionRequest';
export const FETCH_SPECIFIC_SUBMISSION_SUCCESS = 'submissions/fetchSpecificSubmissionSuccess';
export const FETCH_SPECIFIC_SUBMISSION_FAILURE = 'submissions/fetchSpecificSubmissionFailure';
export const UPDATE_SUBMISSION_STATUS_REQUEST = 'submissions/updateSubmissionStatusRequest';
export const UPDATE_SUBMISSION_STATUS_SUCCESS = 'submissions/updateSubmissionStatusSuccess';
export const UPDATE_SUBMISSION_STATUS_FAILURE = 'submissions/updateSubmissionStatusFailure';
export const DELETE_SUBMISSION_REQUEST = 'submissions/deleteSubmissionRequest';
export const DELETE_SUBMISSION_SUCCESS = 'submissions/deleteSubmissionSuccess';
export const DELETE_SUBMISSION_FAILURE = 'submissions/deleteSubmissionFailure';
export const FETCH_ALL_SUBMISSIONS_REQUEST = 'submissions/fetchAllSubmissionsRequest';
export const FETCH_ALL_SUBMISSIONS_SUCCESS = 'submissions/fetchAllSubmissionsSuccess';
export const FETCH_ALL_SUBMISSIONS_FAILURE = 'submissions/fetchAllSubmissionsFailure';


//*====> Action Students <====
const createSubmissionRequest = () => ({
  type: CREATE_SUBMISSION_REQUEST,
});

const createSubmissionSuccess = (submission) => ({
  type: CREATE_SUBMISSION_SUCCESS,
  payload: submission,
});

const createSubmissionFailure = (error) => ({
  type: CREATE_SUBMISSION_FAILURE,
  payload: error,
});

const fetchSubmissionsRequest = () => ({
  type: FETCH_SUBMISSIONS_REQUEST,
});

const fetchSubmissionsSuccess = (submissions) => ({
  type: FETCH_SUBMISSIONS_SUCCESS,
  payload: submissions,
});
const fetchSubmissionsFailure = (error) => ({
  type: FETCH_SUBMISSIONS_FAILURE,
  payload: error,
});
const fetchSpecificSubmissionRequest = () => ({
  type: FETCH_SPECIFIC_SUBMISSION_REQUEST,
});

const fetchSpecificSubmissionSuccess = (submission) => ({
  type: FETCH_SPECIFIC_SUBMISSION_SUCCESS,
  payload: submission,
});

const fetchSpecificSubmissionFailure = (error) => ({
  type: FETCH_SPECIFIC_SUBMISSION_FAILURE,
  payload: error,
});
const updateSubmissionStatusRequest = () => ({
  type: UPDATE_SUBMISSION_STATUS_REQUEST,
});

const updateSubmissionStatusSuccess = (submission) => ({
  type: UPDATE_SUBMISSION_STATUS_SUCCESS,
  payload: submission,
});

const updateSubmissionStatusFailure = (error) => ({
  type: UPDATE_SUBMISSION_STATUS_FAILURE,
  payload: error,
});

const deleteSubmissionRequest = () => ({
  type: DELETE_SUBMISSION_REQUEST,
});

const deleteSubmissionSuccess = (subId) => ({
  type: DELETE_SUBMISSION_SUCCESS,
  payload: subId,
});

const deleteSubmissionFailure = (error) => ({
  type: DELETE_SUBMISSION_FAILURE,
  payload: error,
});

const fetchAllSubmissionsRequest = () => ({
  type: FETCH_ALL_SUBMISSIONS_REQUEST,
});

const fetchAllSubmissionsSuccess = (submissions) => ({
  type: FETCH_ALL_SUBMISSIONS_SUCCESS,
  payload: submissions,
});

const fetchAllSubmissionsFailure = (error) => ({
  type: FETCH_ALL_SUBMISSIONS_FAILURE,
  payload: error,
});



//*====> Thunk Action Students <====

// Create a new submission for a specific opportunity
export const createNewSubmission = (formData, oppId) => async (dispatch) => {
  dispatch(createSubmissionRequest());
  try {
    const response = await fetch(`/api/opportunities/${oppId}/submit`, {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(createSubmissionSuccess(data));
    } else {
      throw new Error('Failed to create submission');
    }
  } catch (error) {
    dispatch(createSubmissionFailure(error.toString()));
  }
};

// Fetch all submissions for a specific opportunity
export const fetchSubmissionsForOpportunity = (oppId) => async (dispatch) => {
  dispatch(fetchSubmissionsRequest());
  try {
    const response = await fetch(`/api/opportunities/${oppId}/submissions`);
    if (response.ok) {
      const data = await response.json();
      dispatch(fetchSubmissionsSuccess(data));
    } else {
      throw new Error('Failed to fetch submissions');
    }
  } catch (error) {
    dispatch(fetchSubmissionsFailure(error.toString()));
  }
};

// Fetch a specific submission for a specific opportunity
export const fetchSpecificSubmission = (oppId, subId) => async (dispatch) => {
  dispatch(fetchSpecificSubmissionRequest());
  try {
    const response = await fetch(`/api/opportunities/${oppId}/submissions/${subId}`);
    if (response.ok) {
      const data = await response.json();
      dispatch(fetchSpecificSubmissionSuccess(data));
    } else {
      throw new Error('Failed to fetch the specific submission');
    }
  } catch (error) {
    dispatch(fetchSpecificSubmissionFailure(error.toString()));
  }
};

// Update the status of a specific submission
export const updateSubmissionStatus = (oppId, subId, newStatus) => async (dispatch) => {
    dispatch(updateSubmissionStatusRequest());
    try {
      const response = await fetch(`/api/opportunities/${oppId}/submissions/${subId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });
      if (response.ok) {
        const updatedSubmission = await response.json();
        dispatch(updateSubmissionStatusSuccess(updatedSubmission));
      } else {
        throw new Error('Failed to update submission status');
      }
    } catch (error) {
      dispatch(updateSubmissionStatusFailure(error.toString()));
    }
  };

// Delete a specific submission
export const deleteSubmission = (oppId, subId) => async (dispatch) => {
  dispatch(deleteSubmissionRequest());
  try {
    const response = await fetch(`/api/opportunities/${oppId}/submissions/${subId}`, {
      method: 'DELETE',
    });
    if (response.ok) {
      dispatch(deleteSubmissionSuccess(subId));
    } else {
      throw new Error('Failed to delete submission');
    }
  } catch (error) {
    dispatch(deleteSubmissionFailure(error.toString()));
  }
};

// Fetch all submissions sitewide
export const fetchAllSubmissions = () => async (dispatch) => {
  dispatch(fetchAllSubmissionsRequest());
  try {
    const response = await fetch('/api/opportunities/submissions'); // Adjust the URL to your API endpoint
    if (!response.ok) throw new Error('Failed to fetch submissions');

    const data = await response.json();
    dispatch(fetchAllSubmissionsSuccess(data));
  } catch (error) {
    dispatch(fetchAllSubmissionsFailure(error.toString()));
  }
};



//*====> Reducer <====
const initialState = {
  loading: false,
  updating: false,
  deleting: false,
  submission: null,
  submissions: [],
  deleteError: '',
  error: '',
};

const submissionReducer = (state = initialState, action) => {
  switch (action.type) {
    case CREATE_SUBMISSION_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case CREATE_SUBMISSION_SUCCESS:
      return {
        ...state,
        loading: false,
        submission: action.payload,
        error: '',
      };
    case CREATE_SUBMISSION_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload,
        submission: null,
      };
    case FETCH_SUBMISSIONS_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case FETCH_SUBMISSIONS_SUCCESS:
      return {
        ...state,
        loading: false,
        submissions: action.payload,
        error: '',
      };
    case FETCH_SUBMISSIONS_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload,
        submissions: [],
      };
    case FETCH_SPECIFIC_SUBMISSION_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case FETCH_SPECIFIC_SUBMISSION_SUCCESS:
      return {
        ...state,
        loading: false,
        submission: action.payload,
        error: '',
      };
    case FETCH_SPECIFIC_SUBMISSION_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload,
        submission: null,
      };
    case UPDATE_SUBMISSION_STATUS_REQUEST:
      return {
        ...state,
        updating: true,
      };
    // case UPDATE_SUBMISSION_STATUS_SUCCESS:
    //   return {
    //     ...state,
    //     updating: false,
    //     submission: action.payload, // You may need to adjust this based on how you want to reflect the update in your state
    //     updateError: '',
    //   };
    case UPDATE_SUBMISSION_STATUS_SUCCESS: {
      const updatedSubmissions = state.submissions.map((submission) => {
        if (submission.id === action.payload.id) {
          return { ...submission, status: action.payload.status };
        }
        return submission;
      });
      return {
        ...state,
        submissions: updatedSubmissions,
      };
    }
    case UPDATE_SUBMISSION_STATUS_FAILURE:
      return {
        ...state,
        updating: false,
        updateError: action.payload,
      };
    case DELETE_SUBMISSION_REQUEST:
      return {
        ...state,
        deleting: true,
      };
    case DELETE_SUBMISSION_SUCCESS:
      return {
        ...state,
        deleting: false,
        submissions: state.submissions.filter(submission => submission.id !== action.payload),
        deleteError: '',
      };
    case DELETE_SUBMISSION_FAILURE:
      return {
        ...state,
        deleting: false,
        deleteError: action.payload,
      };
    case FETCH_ALL_SUBMISSIONS_REQUEST:
      return { ...state, loading: true };
    case FETCH_ALL_SUBMISSIONS_SUCCESS:
      return { ...state, loading: false, submissions: action.payload };
    case FETCH_ALL_SUBMISSIONS_FAILURE:
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
};

export default submissionReducer;

