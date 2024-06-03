import {
  legacy_createStore as createStore,
  applyMiddleware,
  compose,
  combineReducers,
} from "redux";
import thunk from "redux-thunk";
import sessionReducer from "./session";
import opportunitiesReducer from "./opportunities";
import submissionReducer from "./submissions";
import feedbackReducer from "./feedback";
import mediaReducer from "./media";
import userOpportunitiesReducer from "./useropps";
import profileReducer from "./profile";
import usersReducer from "./users";

const rootReducer = combineReducers({
  session: sessionReducer,
  profile: profileReducer,
  opportunities: opportunitiesReducer,
  submissions: submissionReducer,
  feedback: feedbackReducer,
  media: mediaReducer,
  userOpportunities: userOpportunitiesReducer,
  users: usersReducer,
});

let enhancer;
if (import.meta.env.MODE === "production") {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = (await import("redux-logger")).default;
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const configureStore = (preloadedState) => {
  return createStore(rootReducer, preloadedState, enhancer);
};

export default configureStore;
