import React from 'react';
import { View, Text, Button, StyleSheet, FlatList } from 'react-native';

const Profile = ({ route, navigation }) => {
  const { user } = route.params || {}; // Safely access route.params and extract user

  // Debugging line to check if user data is received correctly
  console.log('User data in Profile component:', user);

  // Handle the case where the user object is undefined
  if (!user) {
    return (
      <View style={styles.container}>
        <Text>User data not available.</Text>
        <Button title="Go Back" onPress={() => navigation.navigate('Login')} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, {user.username}!</Text>
      <Text>Email: {user.email}</Text>
      <Text>Status: {user.status}</Text>
      <Text>Type: {user.type}</Text>

      {/* Display list of students */}
      <Text style={styles.subTitle}>Students:</Text>
      <FlatList
        data={user.students}
        keyExtractor={(student) => student.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.studentContainer}>
            <Text>Student Name: {item.user_id}</Text>
            <Text>Bio: {item.bio || "N/A"}</Text>
            <Text>Skill Level: {item.skill_level || "N/A"}</Text>
          </View>
        )}
      />

      <Button title="Logout" onPress={() => navigation.navigate('Login')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
  subTitle: { fontSize: 18, fontWeight: 'bold', marginVertical: 10 },
  studentContainer: { marginBottom: 10, padding: 10, backgroundColor: '#f0f0f0', borderRadius: 5 },
});

export default Profile;
