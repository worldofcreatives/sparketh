import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { View, TextInput, Button, Text } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const LoginScreen = ({ navigation }) => {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [csrfToken, setCsrfToken] = useState('');

  useEffect(() => {
    // Fetch the CSRF token from the backend
    const fetchCsrfToken = async () => {
      const response = await axios.get('http://localhost:8000/api/auth/csrf-token', { withCredentials: true });
      setCsrfToken(response.data.csrf_token);
    };

    fetchCsrfToken();
  }, []);

  const handleLogin = async () => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/auth/login',
        {
          identifier: usernameOrEmail,
          password: password,
        },
        {
          headers: {
            'X-CSRFToken': csrfToken,
          },
          withCredentials: true,  // Important for cookies to be sent/received
        }
      );

      await AsyncStorage.setItem('token', response.data.token);
      navigation.navigate('Main');
    } catch (error) {
      console.error('Login Error:', error.response.data);
    }
  };

  return (
    <View>
      <TextInput placeholder="Username or Email" onChangeText={setUsernameOrEmail} value={usernameOrEmail} />
      <TextInput placeholder="Password" onChangeText={setPassword} value={password} secureTextEntry />
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
};

export default LoginScreen;
