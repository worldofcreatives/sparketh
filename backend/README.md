# Welcome to Sparketh!

Link to live site: https://packtune.onrender.com/

## Tech Stack
### Frameworks and Libraries
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![Redux](https://img.shields.io/badge/redux-%23593d88.svg?style=for-the-badge&logo=redux&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)

 ### Database:
 ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

 ### Hosting:
 ![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)

## API Documentation

### Overview
This API facilitates interactions between students (writers, artists, producers, musicians) and parents (music labels, sync parents, A-list artists, and producers) within the music industry. It enables the sharing of opportunities and submission of music.

### User Login

This loggs the user in.

- **POST** `/api/login`
- **Body:**
  ```json
  {
    "email": "student@example.com",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "token": "<access_token>",
    "user": {
      "userId": 1,
      "email": "student@example.com",
      "type": "Student",
      "name": "Jane Doe",
      "profilePic": "https://example.com/profilepic.jpg"
    }
  }
  ```

### User Registration

This signs a user up.

- **POST** `/api/register`
- **Body:**
  ```json
  {
    "email": "student@example.com",
    "password": "password123",
    "type": "Student",
    "name": "Jane Doe",
    "artistBandName": "Jane's Band",
    "genres": "Rock, Pop",
    "bio": "Aspiring musician from NYC."
  }
  ```
- **Response:**
  ```json
  {
    "userId": 1,
    "email": "student@example.com",
    "type": "Student",
    "profile": {
      "studentId": 1,
      "name": "Jane Doe",
      "artistBandName": "Jane's Band",
      "genres": "Rock, Pop",
      "bio": "Aspiring musician from NYC.",
      "isActive": true
    }
  }
  ```

### Create Opportunity

This allows a user to create a new opportunity.

- **POST** `/api/opportunities`
- **Body:**
  ```json
  {
    "name": "Summer Pop Hit",
    "description": "Looking for an upbeat pop song for our summer campaign.",
    "parentId": 1,
    "genre": "Pop",
    "deadline": "2024-05-30"
  }
  ```
- **Response:**
  ```json
  {
    "oppId": 1,
    "name": "Summer Pop Hit",
    "description": "Looking for an upbeat pop song for our summer campaign.",
    "parentId": 1,
    "genre": "Pop",
    "deadline": "2024-05-30",
    "isActive": true,
    "createdDate": "2024-04-01T12:00:00Z"
  }
  ```

### Submit Music

This allows a user to submit to an opportunity.

- **POST** `/api/submissions`
- **Body:**
  ```json
  {
    "studentId": 1,
    "oppId": 1,
    "media": [
      {
        "name": "My Summer Song",
        "file": "https://example.com/mysummersong.mp3",
        "fileType": "mp3",
        "duration": 180
      }
    ]
  }
  ```
- **Response:**
  ```json
  {
    "subId": 1,
    "studentId": 1,
    "oppId": 1,
    "status": "Pending",
    "isActive": true,
    "createdDate": "2024-04-02T15:00:00Z",
    "media": [
      {
        "mediaId": 1,
        "name": "My Summer Song",
        "file": "https://example.com/mysummersong.mp3",
        "fileType": "mp3",
        "duration": 180,
        "createdDate": "2024-04-02T15:00:00Z"
      }
    ]
  }
  ```

### List Opportunities

This allows a user to list all opportunities.

- **GET** `/api/opportunities`
- **Response:**
  ```json
  {
    "opportunities": [
      {
        "oppId": 1,
        "name": "Summer Pop Hit",
        "description": "Looking for an upbeat pop song for our summer campaign.",
        "parentId": 1,
        "genre": "Pop",
        "deadline": "2024-05-30",
        "isActive": true,
        "createdDate": "2024-04-01T12:00:00Z"
      }
    ]
  }
  ```

### Update Submission Status

This allows a user to update the status of a submission.

- **PUT** `/api/submissions/:subId/status`
- **Body:**
  ```json
  {
    "status": "Accepted"
  }
  ```
- **Response:**
  ```json
  {
    "subId": 1,
    "status": "Accepted",
    "updatedDate": "2024-04-04T09:00:00Z"
  }
  ```

### List Submissions for Opportunity

This allows a user to list all the submissions in an opportunity.

- **GET** `/api/opportunities/:oppId/submissions`
- **Response:**
  ```json
  {
    "submissions": [
      {
        "subId": 1,
        "studentId": 1,
        "oppId": 1,
        "status": "Accepted",
        "createdDate": "2024-04-02T15:00:00Z",
        "media": [
          {
            "mediaId": 1,
            "name": "My Summer Song",
            "file": "https://example.com/mysummersong.mp3",
            "fileType": "mp3",
            "duration": 180,
            "createdDate": "2024-04-02T15:00:00Z"
          }
        ]
      }
    ]
  }
  ```
# sparketh2
