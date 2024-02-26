# Play-Pal Backend Setup and API Documentation

Here's the updated documentation with all fields represented in list form:

## Backend Setup

To start the Django REST Framework backend, follow these steps:

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
4. Perform database migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
6. The backend should now be running at `http://localhost:8000/`.

## Endpoints

### Accounts

#### Register

- **Endpoint**: `POST accounts/register/`
- **Description**: Creates accounts with the following mandatory fields: 
  - username
  - email
  - password
- **Success Response**: 201 Created with created user info.

#### Login

- **Endpoint**: `POST accounts/login/`
- **Description**: Logs in with the following mandatory fields: 
  - username
  - password
- **Success Response**: 200 OK with JWT refresh and access token.

#### Refresh Token

- **Endpoint**: `accounts/token/refresh/`
- **Description**: Refreshes JWT token with the following mandatory fields:
    - refresh
- **Success Response**: 200 OK with new access token.

#### Edit Profile

- **Endpoint**: `PATCH accounts/editprofile/`
- **Description**: Edits user profile with the following optional fields: 
  - username
  - email
  - password
  - name
  - gender
  - sports_you_can_play
  - phone_no
  - age
  - description
  - email_product
  - email_security
  - phone_security
  - avatar_data
- **Success Response**: 200 OK with updated user info.

#### Get User Profile by ID

- **Endpoint**: `GET accounts/<int:id>/`
- **Description**: Retrieves user profile by ID.
- **Success Response**: 200 OK with user info.

### Events

#### Create Event

- **Endpoint**: `POST events/create/`
- **Description**: Creates events with the following mandatory fields and optional attachment:
  - start_time
  - end_time
  - title
  - description
  - content
  - sport_data
  - level (B, I, A, P)
  - age_group (C, T, A, S)
  - max_players
  - location
- **Success Response**: 201 Created with created event info.

#### Get Event by ID

- **Endpoint**: `GET events/<int:id>/`
- **Description**: Retrieves event by ID.
- **Success Response**: 200 OK with event info.

#### Get All Events

- **Endpoint**: `GET events/list/`
- **Description**: Retrieves all events.
- **Success Response**: 200 OK with all events info.

#### Update Event by ID

- **Endpoint**: `PATCH events/update/`
- **Description**: Updates event by ID with the following optional fields:
  - id
  - start_time
  - end_time
  - title
  - description
  - content
  - sport_data
  - level (B, I, A, P)
  - age_group (C, T, A, S)
  - max_players
  - location
  - attachment_data
- **Success Response**: 200 OK with updated event info.

#### Join Event

- **Endpoint**: `PATCH events/join/`
- **Description**: Joins event by ID with the following mandatory fields:
  - id
- **Success Response**: 200 OK with {"message": "Joined event successfully!"}.

#### Quit Event

- **Endpoint**: `PATCH events/quit/`
- **Description**: Leaves event by ID with the following mandatory fields:
  - id
- **Success Response**: 200 OK with {"message": "Left event successfully!"}.

#### Delete Event by ID

- **Endpoint**: `DELETE events/delete/`
- **Description**: Deletes event by ID with the following mandatory fields:
  - id
- **Success Response**: 200 OK with event info.

### Notifications

#### Get All Notifications

- **Endpoint**: `GET notification/list/`
- **Description**: Retrieves all notifications for the current logged-in user.
- **Success Response**: 200 OK with all notifications' info.
