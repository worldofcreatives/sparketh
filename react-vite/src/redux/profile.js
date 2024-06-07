// src/store/profile.js
const SET_USER_PROFILE = 'profile/setUserProfile';
const UPDATE_USER_PROFILE = 'profile/updateUserProfile';
const UPDATE_GENRES_TYPES = 'profile/updateGenresTypes';


// Action Students
const setUserProfile = (profile) => ({
  type: SET_USER_PROFILE,
  profile,
});

const updateUserProfile = (profile) => ({
  type: UPDATE_USER_PROFILE,
  profile,
});

const updateGenresTypes = (genresTypes) => ({
  type: UPDATE_GENRES_TYPES,
  payload: genresTypes,
});


// Thunks

// Fetches the user profile from the backend
export const fetchUserProfile = () => async (dispatch) => {
  const response = await fetch('/api/profiles/');
  if (response.ok) {
    const data = await response.json();
    dispatch(setUserProfile(data));
    return data;
  }
};

// Updates the user profile on the backend
export const updateProfile = (formData) => async (dispatch) => {
  const response = await fetch('/api/profiles/', {
    method: 'PUT',
    credentials: 'include',
    body: formData, // Directly use formData here without JSON.stringify
  });

  if (response.ok) {
    const profile = await response.json();
    dispatch(updateUserProfile(profile));
    return profile;
  }
};

export const updateGenresAndTypes = (genresTypes) => async (dispatch) => {
  const response = await fetch('/api/profiles/update_genres_types', {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(genresTypes),
  });

  if (response.ok) {
    const updatedData = await response.json();
    dispatch(updateGenresTypes(updatedData));
    return updatedData;
  }
};



// Reducer
const initialState = { userProfile: null };

const profileReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_USER_PROFILE:
      return { ...state, userProfile: action.profile };
    case UPDATE_USER_PROFILE:
      // Handle general profile updates
      return { ...state, userProfile: { ...state.userProfile, ...action.profile } };
    case UPDATE_GENRES_TYPES:
      // Specifically handle updates to genres and types
      return {
        ...state,
        userProfile: {
          ...state.userProfile,
          student: {
            ...state.userProfile.student,
            genres: action.payload.genres,
            types: action.payload.types,
          },
        },
      };
    default:
      return state;
  }
};

export default profileReducer;
