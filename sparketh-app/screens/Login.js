import React from 'react';
import { View, TextInput, Button, Text, StyleSheet } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import axios from 'axios';

const Login = ({ navigation }) => {
  const { control, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      identifier: '', // Changed from 'username' to 'identifier'
      password: '', // Initialize with an empty string
    }
  });

  const onSubmit = async (data) => {
    try {
      // Fetch CSRF token from cookies if needed
      const csrfToken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrf_token='))
        ?.split('=')[1];

      const response = await axios.post('http://localhost:8000/api/auth/login', data, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': csrfToken,  // Include the CSRF token in headers
        },
        withCredentials: true,  // Include cookies in requests
      });

      if (response.status === 200) {
        console.log('User data from backend:', response.data); // Debugging line
        navigation.navigate('Profile', { user: response.data }); // Ensure this is correct
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
        name="identifier" // Changed from 'username' to 'identifier'
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
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 16 },
  input: { borderWidth: 1, padding: 8, marginVertical: 8 },
});

export default Login;
