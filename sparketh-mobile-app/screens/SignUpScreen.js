import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import axios from 'axios';

const SignUpScreen = ({ navigation }) => {
  const { control, handleSubmit } = useForm();

  const onSubmit = async (data) => {
    try {
      await axios.post('http://localhost:8000/api/users/register', {
        username: data.username,
        email: data.email,
        password: data.password,
      });

      navigation.navigate('Login');
    } catch (error) {
      console.error('SignUp Error:', error.response.data);
    }
  };

  return (
    <View>
      <Text>Sign Up</Text>
      <Controller
        control={control}
        name="username"
        render={({ field: { onChange, value } }) => (
          <TextInput
            placeholder="Username"
            onChangeText={onChange}
            value={value}
          />
        )}
      />
      <Controller
        control={control}
        name="email"
        render={({ field: { onChange, value } }) => (
          <TextInput
            placeholder="Email"
            onChangeText={onChange}
            value={value}
          />
        )}
      />
      <Controller
        control={control}
        name="password"
        render={({ field: { onChange, value } }) => (
          <TextInput
            placeholder="Password"
            secureTextEntry
            onChangeText={onChange}
            value={value}
          />
        )}
      />
      <Button title="Sign Up" onPress={handleSubmit(onSubmit)} />
    </View>
  );
};

export default SignUpScreen;
