//*====> Action Types <====
export const CREATE_FEEDBACK_REQUEST = 'feedback/createFeedbackRequest';
export const CREATE_FEEDBACK_SUCCESS = 'feedback/createFeedbackSuccess';
export const CREATE_FEEDBACK_FAILURE = 'feedback/createFeedbackFailure';
export const FETCH_FEEDBACK_REQUEST = 'feedback/fetchFeedbackRequest';
export const FETCH_FEEDBACK_SUCCESS = 'feedback/fetchFeedbackSuccess';
export const FETCH_FEEDBACK_FAILURE = 'feedback/fetchFeedbackFailure';

//*====> Action Students <====
const createFeedbackRequest = () => ({
  type: CREATE_FEEDBACK_REQUEST,
});

const createFeedbackSuccess = (feedback) => ({
  type: CREATE_FEEDBACK_SUCCESS,
  payload: feedback,
});

const createFeedbackFailure = (error) => ({
  type: CREATE_FEEDBACK_FAILURE,
  payload: error,
});
const fetchFeedbackRequest = () => ({
  type: FETCH_FEEDBACK_REQUEST,
});

const fetchFeedbackSuccess = (feedbacks) => ({
  type: FETCH_FEEDBACK_SUCCESS,
  payload: feedbacks,
});

const fetchFeedbackFailure = (error) => ({
  type: FETCH_FEEDBACK_FAILURE,
  payload: error,
});


//*====> Thunk Action Students <====

// Create feedback for a submission
export const createFeedbackForSubmission = (oppId, subId, feedbackData) => async (dispatch) => {
  dispatch(createFeedbackRequest());
  try {
    const response = await fetch(`/api/opportunities/${oppId}/submissions/${subId}/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(feedbackData),
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(createFeedbackSuccess(data));
    } else {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to create feedback');
    }
  } catch (error) {
    dispatch(createFeedbackFailure(error.toString()));
  }
};

// Fetch feedback for a submission
export const fetchFeedbackForSubmission = (oppId, subId) => async (dispatch) => {
  dispatch(fetchFeedbackRequest());
  try {
    const response = await fetch(`/api/opportunities/${oppId}/submissions/${subId}/feedback`);
    if (response.ok) {
      const data = await response.json();
      dispatch(fetchFeedbackSuccess(data));
    } else {
      throw new Error('Failed to fetch feedback');
    }
  } catch (error) {
    dispatch(fetchFeedbackFailure(error.toString()));
  }
};


//*====> Reducer <====
const initialState = {
  loading: false,
  loadingFeedback: false,
  feedbacks: [],
  error: null,
  feedbackError: null,
};

const feedbackReducer = (state = initialState, action) => {
  switch (action.type) {
    case CREATE_FEEDBACK_REQUEST:
      return { ...state, loading: true };
    case CREATE_FEEDBACK_SUCCESS:
      return { ...state, loading: false, feedbacks: [...state.feedbacks, action.payload], error: null };
    case CREATE_FEEDBACK_FAILURE:
      return { ...state, loading: false, error: action.payload };
    case FETCH_FEEDBACK_REQUEST:
      return { ...state, loadingFeedback: true };
    case FETCH_FEEDBACK_SUCCESS:
      return { ...state, loadingFeedback: false, feedbacks: action.payload, feedbackError: null };
    case FETCH_FEEDBACK_FAILURE:
      return { ...state, loadingFeedback: false, feedbackError: action.payload };
    default:
      return state;
  }
};

export default feedbackReducer;
