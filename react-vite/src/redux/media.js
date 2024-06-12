//*====> Action Types <====
export const UPLOAD_MEDIA_REQUEST = 'media/uploadMediaRequest';
export const UPLOAD_MEDIA_SUCCESS = 'media/uploadMediaSuccess';
export const UPLOAD_MEDIA_FAILURE = 'media/uploadMediaFailure';

//*====> Action Students <====
const uploadMediaRequest = () => ({
  type: UPLOAD_MEDIA_REQUEST,
});

const uploadMediaSuccess = (media) => ({
  type: UPLOAD_MEDIA_SUCCESS,
  payload: media,
});

const uploadMediaFailure = (error) => ({
  type: UPLOAD_MEDIA_FAILURE,
  payload: error,
});

//*====> Thunk Action Students <====
export const uploadMedia = (mediaData) => async (dispatch) => {
  dispatch(uploadMediaRequest());
  try {
    const response = await fetch('/api/media/upload', {
      method: 'POST',
      body: mediaData, // FormData object, no need to set Content-Type header
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(uploadMediaSuccess(data));
    } else {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to upload media');
    }
  } catch (error) {
    dispatch(uploadMediaFailure(error.toString()));
  }
};

//*====> Reducer <====
const initialState = {
  loading: false,
  mediaItems: [],
  error: null,
};

const mediaReducer = (state = initialState, action) => {
  switch (action.type) {
    case UPLOAD_MEDIA_REQUEST:
      return { ...state, loading: true };
    case UPLOAD_MEDIA_SUCCESS:
      return { ...state, loading: false, mediaItems: [...state.mediaItems, action.payload], error: null };
    case UPLOAD_MEDIA_FAILURE:
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
};

export default mediaReducer;
