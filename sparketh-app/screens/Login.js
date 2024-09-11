import React from 'react';
import { View, TextInput, Button, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Login = ({ navigation }) => {
  const { control, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      identifier: '',
      password: '',
    }
  });

  const onSubmit = async (data) => {
    try {
      const csrfToken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrf_token='))
        ?.split('=')[1];

      const response = await axios.post('http://localhost:8000/api/auth/login', data, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': csrfToken,
        },
        withCredentials: true,
      });

      if (response.status === 200) {
        console.log('User data from backend:', response.data);
        await AsyncStorage.setItem('user', JSON.stringify(response.data)); // Store user data
        navigation.navigate('Profile', { user: response.data }); // Navigate to Profile
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text>Login</Text>
      <Controller
        control={control}
        rules={{ required: true }}
        name="identifier"
        render={({ field: { onChange, onBlur, value } }) => (
          <TextInput
            style={styles.input}
            placeholder="Username or Email"
            onBlur={onBlur}
            onChangeText={onChange}
            value={value}
          />
        )}
      />
      {errors.identifier && <Text>This is required.</Text>}

      <Controller
        control={control}
        rules={{ required: true }}
        name="password"
        render={({ field: { onChange, onBlur, value } }) => (
          <TextInput
            style={styles.input}
            placeholder="Password"
            onBlur={onBlur}
            onChangeText={onChange}
            value={value}
            secureTextEntry
          />
        )}
      />
      {errors.password && <Text>This is required.</Text>}

      <Button title="Login" onPress={handleSubmit(onSubmit)} />

      {/* Button to navigate to the Sign Up screen */}
      <TouchableOpacity onPress={() => navigation.navigate('SignUp')}>
        <Text style={styles.linkText}>Don't have an account? Sign Up</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 16 },
  input: { borderWidth: 1, padding: 8, marginVertical: 8 },
  linkText: { color: 'blue', marginTop: 16, textAlign: 'center' },
});

export default Login;
