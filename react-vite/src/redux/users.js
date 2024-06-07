// src/store/users.js
const SET_ALL_USERS = 'users/setAllUsers';
const UPDATE_USER_STATUS = 'users/updateUserStatus';
const SET_CURRENT_USER = 'users/setCurrentUser';

// Action Students
const setAllUsers = (users) => ({
  type: SET_ALL_USERS,
  users,
});

const updateUserStatusAction = (userId, status) => ({
  type: UPDATE_USER_STATUS,
  payload: { userId, status },
});

const setCurrentUser = (user) => ({
    type: SET_CURRENT_USER,
    user,
  });

// Thunks

// Fetches all users from the backend
export const fetchAllUsers = () => async (dispatch) => {
  const response = await fetch('/api/users/all', {
    credentials: 'include',
  });
  if (response.ok) {
    const users = await response.json();
    dispatch(setAllUsers(users));
    return users;
  }
};

// Updates the status of a user
export const updateUserStatus = (userId, status) => async (dispatch) => {
  const response = await fetch(`/api/users/${userId}/update-status`, {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status }),
  });

  if (response.ok) {
    dispatch(updateUserStatusAction(userId, status));
    return { userId, status };
  }
};

// Thunk for updating a user's status
export const thunkUpdateUserStatus = (userId, status) => async (dispatch) => {
  const response = await fetch(`/api/auth/update_status/${userId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ status })
  });

  if (response.ok) {
    dispatch(updateUserStatusAction(userId, status));
  } else {
    // Handle errors as needed
    console.error('Failed to update user status');
  }
};


// Thunk for fetching a user's information by ID
export const fetchUserById = (userId) => async (dispatch) => {
    const response = await fetch(`/api/users/${userId}`, {
      credentials: 'include',
    });
    if (response.ok) {
      const user = await response.json();
      dispatch(setCurrentUser(user));
      return user;
    }
  };

// Reducer
const initialState = { users: [], currentUser: null };

const usersReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_ALL_USERS:
      return { ...state, users: action.users };
    case UPDATE_USER_STATUS:
      return {
        ...state,
        users: state.users.map(user =>
          user.id === action.payload.userId ? { ...user, status: action.payload.status } : user
        )
      };
    case SET_CURRENT_USER:
      return { ...state, currentUser: action.user };
    default:
      return state;
  }
};

export default usersReducer;
