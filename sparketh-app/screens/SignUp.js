import React from 'react';
import { View, TextInput, Button, Text, StyleSheet } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';


const SignUp = ({ navigation }) => {

  const { control, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      username: '', // Initialize with an empty string
      email: '', // Initialize with an empty string
      password: '', // Initialize with an empty string
    }
  });

  const onSubmit = async (data) => {
    try {
      const csrfToken = await AsyncStorage.getItem('csrf_token'); // Fetch token from storage or state
  
      const response = await axios.post(
        'http://localhost:8000/api/users/register',
        data,
        {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken, // Include CSRF token here if needed
          },
          withCredentials: true,
        }
      );
  
      if (response.status === 201) {
        navigation.navigate('Login'); // Redirect to Login after successful signup
      }
    } catch (error) {
      console.error('Signup error:', error); // Log the full error
      if (error.response) {
        // Server responded with a status other than 2xx
        console.error('Error data:', error.response.data);
      } else if (error.request) {
        // No response received from server
        console.error('Error request:', error.request);
      } else {
        // Other errors
        console.error('Error message:', error.message);
      }
    }
  };
  

  return (
    <View style={styles.container}>
      <Text>Sign Up</Text>
      <Controller
        control={control}
        rules={{ required: true }}
        name="username"
        render={({ field: { onChange, onBlur, value } }) => (
          <TextInput
            style={styles.input}
            placeholder="Username"
            onBlur={onBlur}
            onChangeText={onChange}
            value={value}
          />
        )}
      />
      {errors.username && <Text>This is required.</Text>}

      <Controller
        control={control}
        rules={{ required: true }}
        name="email"
        render={({ field: { onChange, onBlur, value } }) => (
          <TextInput
            style={styles.input}
            placeholder="Email"
            onBlur={onBlur}
            onChangeText={onChange}
            value={value}
          />
        )}
        />
        {errors.email && <Text>This is required.</Text>}

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

      <Button title="Sign Up" onPress={handleSubmit(onSubmit)} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 16 },
  input: { borderWidth: 1, padding: 8, marginVertical: 8 },
});

export default SignUp;
