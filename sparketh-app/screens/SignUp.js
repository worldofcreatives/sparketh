import React from 'react';
import { View, TextInput, Button, Text, StyleSheet } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import axios from 'axios';

const SignUp = ({ navigation }) => {

  const { control, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      username: '', // Initialize with an empty string
      password: '', // Initialize with an empty string
    }
  });

  const onSubmit = async (data) => {
    try {
      const response = await axios.post('http://localhost:8000/api/auth/signup', data);
      if (response.status === 200) {
        navigation.navigate('Login'); // Redirect to Login after successful signup
      }
    } catch (error) {
      console.error(error);
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
