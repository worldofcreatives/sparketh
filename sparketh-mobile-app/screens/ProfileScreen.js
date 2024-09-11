import React, { useEffect, useState } from 'react';
import { View, Text, Button } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const ProfileScreen = ({ navigation }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUserProfile = async () => {
      const token = await AsyncStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/users/profile', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUser(response.data);
    };

    fetchUserProfile();
  }, []);

  const handleLogout = async () => {
    await AsyncStorage.removeItem('token');
    navigation.navigate('Login');
  };

  return (
    <View>
      {user ? (
        <>
          <Text>Username: {user.username}</Text>
          <Text>Email: {user.email}</Text>
          <Button title="Logout" onPress={handleLogout} />
        </>
      ) : (
        <Text>Loading...</Text>
      )}
    </View>
  );
};

export default ProfileScreen;
