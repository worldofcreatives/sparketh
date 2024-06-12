import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';

const WithParentGuard = (WrappedComponent) => {
  return (props) => {
    const user = useSelector((state) => state.session.user);

    if (user && user.type === 'Parent') {
      return <WrappedComponent {...props} />;
    } else {
      return <Navigate to="/unauthorized" />;
    }
  };
};

export default WithParentGuard;
