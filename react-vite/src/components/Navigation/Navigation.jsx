import { NavLink, useNavigate } from "react-router-dom";
import "./Navigation.css";
import { useDispatch, useSelector } from "react-redux";
import { thunkLogout } from "../../redux/session";

function Navigation() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const sessionUser = useSelector((state) => state.session.user);
  const isAuthenticated = sessionUser !== null;
  // Assuming the user type is available as sessionUser.type
  const isParent = sessionUser?.type === "Parent";

  const logout = (e) => {
    e.preventDefault();
    dispatch(thunkLogout());
    navigate("/");
  };

  return (
    <nav className="navigation">
      <a href="/" className="logo-link">
        <img className="logo" src="https://uploads-ssl.webflow.com/5d6dde2cb8496e3f669a4b75/65e8b7a32db811c3f6f252ac_logo.jpg" alt="PackTune Logo" />
      </a>
      <ul className="nav-links">
        {isAuthenticated && (
          <>
            <div className="content-nav">
              {isParent && (
                <>
                  <li>
                    <NavLink to="/charts" activeClassName="active">
                      <i className="fas fa-th-large"></i> Dashboard
                    </NavLink>
                  </li>
                </>
              )}

              <li>
                <NavLink to="/opps" activeClassName="active">
                  <i className="fas fa-key"></i> Opps
                </NavLink>
              </li>

              <li>
                <NavLink to="/submissions" activeClassName="active">
                  <i className="fas fa-music"></i> Subs
                </NavLink>
              </li>

              {isParent && (
                <>
                  <li>
                    <NavLink to="/opps/form" activeClassName="active">
                      <i className="fas fa-plus"></i> Add New Opp
                    </NavLink>
                  </li>
                </>
              )}

              <li>
                <NavLink to="/profile" activeClassName="active">
                  <i className="fas fa-user"></i> Profile
                </NavLink>
              </li>

              <li>
                <button onClick={logout} className="logout-button">
                  Logout
                </button>
              </li>
            </div>
          </>
        )}
        {!isAuthenticated && (
          <>
            <li>
              <NavLink className="log-in" to="/login">
                Login
              </NavLink>
            </li>
            <li>
              <NavLink className="sign-up" to="/signup">
                Sign Up
              </NavLink>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Navigation;


// import { NavLink, useNavigate } from "react-router-dom";
// // import ProfileButton from "./ProfileButton";
// import "./Navigation.css";
// import { useDispatch, useSelector } from "react-redux";
// import { thunkLogout } from "../../redux/session";

// function Navigation() {
//   const dispatch = useDispatch();
//   const navigate = useNavigate();
//   const sessionUser = useSelector((state) => state.session.user);
//   const isAuthenticated = sessionUser !== null;

//   const logout = (e) => {
//     e.preventDefault();
//     dispatch(thunkLogout());
//     navigate("/");
//   };

// return (
//   <nav className="navigation">
//     <a href="/" className="logo-link">
//       <img className="logo" src="https://uploads-ssl.webflow.com/5d6dde2cb8496e3f669a4b75/65e8b7a32db811c3f6f252ac_logo.jpg" alt="PackTune Logo" />
//     </a>
//     <ul className="nav-links">
//       {isAuthenticated && (
//         <>
//           <div className="content-nav">
//             {/* <li>
//               <NavLink to="/" activeClassName="active">Home</NavLink>
//             </li> */}
//             <li>
//               <NavLink to="/myopps" activeClassName="active">
//               <i class="fas fa-th-large"></i>
//               Dashboard</NavLink>
//             </li>

//             <li>
//               <NavLink to="/opps" activeClassName="active">
//               <i class="fas fa-music"></i>
//               Opps</NavLink>
//             </li>

//             <li>
//               <NavLink to="/opps/form" activeClassName="active">
//               <i class="fas fa-plus"></i>
//               Add New Opp</NavLink>
//             </li>

//             <li>
//               <NavLink to="/profile" activeClassName="active">
//               <i class="fas fa-user"></i>
//               Profile</NavLink>
//             </li>

//             <li>
//               <button onClick={logout} className="logout-button">
//                 Logout
//               </button>
//             </li>
//           </div>
//         </>
//       )}
//       {!isAuthenticated && (
//         <>
//           <li>
//             <NavLink className="log-in" to="/login">
//               Login
//             </NavLink>
//           </li>
//           <li>
//             <NavLink
//               className="sign-up" to="/signup">
//               Sign Up
//             </NavLink>
//           </li>
//         </>
//       )}
//     </ul>
//   </nav>
// );
// }

// export default Navigation;
