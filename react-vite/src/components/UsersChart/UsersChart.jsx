import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchAllUsers } from '../../redux/users'; // You need to implement this action

const UsersChart = () => {
    const dispatch = useDispatch();

    useEffect(() => {
      dispatch(fetchAllUsers());
    }, [dispatch]);

    const users = useSelector((state) => state.users.users);
    console.log("🚀 ~ UsersChart ~ users:", users)

    return (
        <table>
            <thead>
                <tr>
                    <th>Email Address</th>
                    <th>Date Joined</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Stage Name</th>
                    <th>Genres</th>
                    <th>Types</th>
                    <th>Status</th>
                    <th>Profile</th>
                </tr>
            </thead>
            <tbody>
                {users.map((user) => (
                    <tr key={user.id}>
                        <td>{user.email}</td>
                        <td>{new Date(user.created_date).toLocaleDateString()}</td>
                        <td>{user.student?.first_name || "N/A"}</td>
                        <td>{user.student?.last_name || "N/A"}</td>
                        <td>{user.student?.stage_name || "N/A"}</td>
                        <td>{(user.student?.genres?.map(genre => genre.name) || []).join(', ') || 'N/A'}</td>
                        <td>{(user.student?.types?.map(type => type.name) || []).join(', ') || 'N/A'}</td>
                        <td>{user.status}</td>
                        <td><a href={user.profile_link}>View Profile</a></td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default UsersChart;
