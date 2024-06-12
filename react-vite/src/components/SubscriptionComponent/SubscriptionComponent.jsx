import React, { useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchUserProfile } from '../../redux/profile';
import './SubscriptionComponent.css';

const stripePromise = loadStripe('pk_test_51O1YnuBIxhjYY7P2cloS3EG1c3Bv84hHkvSJz331km8OA1VmhhRH0BzAFNGRb2vSQy6Yyjfy9uQO8XhLDv5FBwmP00Z4t3vSpc');

const SubscriptionComponent = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.session.user);
  const navigate = useNavigate();

  useEffect(() => {
    dispatch(fetchUserProfile());
  }, [dispatch]);

  const handleCheckout = async (priceId) => {
    const stripe = await stripePromise;
    const response = await fetch('/api/stripe/create-checkout-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ price_id: priceId }),
    });

    const session = await response.json();
    await stripe.redirectToCheckout({ sessionId: session.id });
  };

  const handleManageSubscription = async () => {
    const response = await fetch('/api/stripe/create-portal-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ customer_id: user.stripe_customer_id }),
    });

    const session = await response.json();
    window.location.href = session.url;  // Redirect to the customer portal URL

    // After user returns from the customer portal, refresh the user data
    window.addEventListener('focus', () => {
      dispatch(fetchUserProfile());
    }, { once: true });
  };

  const renderPricingTables = () => (
    <div className="pricing-tables">
      <div className="pricing-table">
        <h2>Monthly Subscription</h2>
        <p>$77 per month</p>
        <button onClick={() => handleCheckout('price_1PLVpIBIxhjYY7P2UNEsuWfr')} className="subscribe-button">
          Subscribe Monthly
        </button>
        <div className="pricing-details">
          <ul>
            <li>Submit up to three ideas per opportunity</li>
            <li>Submit to thirty submissions per month</li>
            <li>2.5% fee on successful placements</li>
          </ul>
        </div>
      </div>
      <div className="pricing-table">
        <h2>Annual Subscription</h2>
        <p>$777 per year</p>
        <button onClick={() => handleCheckout('price_1PLVpbBIxhjYY7P2e7zv0EU2')} className="subscribe-button">
          Subscribe Annually
        </button>
        <div className="pricing-details">
          <ul>
          <li>Submit up to three ideas per opportunity</li>
            <li>Submit to thirty submissions per month</li>
            <li>2.5% fee on successful placements</li>
          </ul>
        </div>
      </div>
    </div>
  );

  return (
    <div className="subscription-component">

      {(user.status === 'Premium Monthly' || user.status === 'Premium Annual') ? (
        <>
        <h1>Enjoy your premium access.</h1>
        <button onClick={handleManageSubscription} className="manage-subscription-button">
          Manage Subscription
        </button>
        </>
      ) : (
        <>
        <h1>Upgrade Your Account to Access More Features</h1>
          <div className="standard-info">
            <h2>Standard Students</h2>
            <p>Free</p>
            <ul>
              <li>Submit one idea per opportunity</li>
              <li>Submit to three submissions per month</li>
              <li>5% fee on successful placements</li>
            </ul>
          </div>
          {renderPricingTables()}
        </>
      )}
    </div>
  );
};

export default SubscriptionComponent;



// import React, { useEffect } from 'react';
// import { loadStripe } from '@stripe/stripe-js';
// import { useDispatch, useSelector } from 'react-redux';
// import { useNavigate } from 'react-router-dom';
// import { fetchUserProfile } from '../../redux/profile';
// import './SubscriptionComponent.css';

// const stripePromise = loadStripe('pk_test_51O1YnuBIxhjYY7P2cloS3EG1c3Bv84hHkvSJz331km8OA1VmhhRH0BzAFNGRb2vSQy6Yyjfy9uQO8XhLDv5FBwmP00Z4t3vSpc');

// const SubscriptionComponent = () => {
//   const dispatch = useDispatch();
//   const user = useSelector((state) => state.session.user);
//   const navigate = useNavigate();

//   useEffect(() => {
//     dispatch(fetchUserProfile());
//   }, [dispatch]);

//   const handleCheckout = async (priceId) => {
//     const stripe = await stripePromise;
//     const response = await fetch('/api/stripe/create-checkout-session', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ price_id: priceId }),
//     });

//     const session = await response.json();
//     await stripe.redirectToCheckout({ sessionId: session.id });
//   };

//   const handleManageSubscription = async () => {
//     const response = await fetch('/api/stripe/create-portal-session', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ customer_id: user.stripe_customer_id }),
//     });

//     const session = await response.json();
//     window.location.href = session.url;  // Redirect to the customer portal URL

//     // After user returns from the customer portal, refresh the user data
//     window.addEventListener('focus', () => {
//       dispatch(fetchUserProfile());
//     }, { once: true });
//   };

//   return (
//     <div className="subscription-buttons">
//       <h1>Welcome, {user.username}</h1>
//       <p>Email: {user.email}</p>
//       <p>Status: {user.status}</p>
//       <button onClick={handleManageSubscription}>Manage Subscription</button>
//       <button onClick={() => handleCheckout('price_1PLVpIBIxhjYY7P2UNEsuWfr')} className="subscribe-button">
//         Subscribe Monthly ($77)
//       </button>
//       <button onClick={() => handleCheckout('price_1PLVpbBIxhjYY7P2e7zv0EU2')} className="subscribe-button">
//         Subscribe Annually ($777)
//       </button>
//     </div>
//   );
// };

// export default SubscriptionComponent;
