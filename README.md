# Play-Pal Backend Setup and API Documentation

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

### *--Pagination--*

All list endpoints are paginated with 20 items per page. You can specify the page number in the query string, e.g. `http://localhost:8000/events/list/?page=2`.
#### Example Response:
```json
{
    "count": 0,
    "next": null, //url to the next page
    "previous": null, //url to the previous page
    "results": [] //list of items, see the corresponding endpoint for specific results
}
```

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

- **Endpoint**: `POST accounts/token/refresh/`
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
  - sports_data (a list of sports you can play, e.g. `"[\"football\", \"basketball\"]"`)
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
- **Example Response**:
  ```json
   {
      "id": 1,
      "username": "abc",
      "email": "abc@abc.com",
      "name": "andi",
      "gender": "male",
      "sports_you_can_play": [
        {
            "id": 1,
            "name": "football"
        },
        {
            "id": 2,
            "name": "basketball"
        }
    ],
      "phone_no": "1234567890",
      "age": 10,
      "description": "hello_world",
      "avatar": "a url to the avatar image",
      "email_product": false,
      "email_security": false,
      "phone_security": false,
      "create_events": [(See Get Event by ID playload below for event info)],
      "join_events": [(See Get Event by ID playload below for event info)],
      "admin_event": [(See Get Event by ID playload below for event info)],,
   }
  ```

### Events

#### Create Event

- **Endpoint**: `POST events/create/`
- **Description**: Creates events with the following mandatory fields:
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
- Optional field:
  - attachment_data
- **Success Response**: 201 Created with created event info.

#### Get Event by ID

- **Endpoint**: `GET events/<int:id>/`
- **Description**: Retrieves event by ID.
- **Success Response**: 200 OK with event info.
- **Example Response**:
    ```json
     {
      "id": 1,
      "owner": (see Get User Profile playload above for user info),
      "start_time": "2023-01-01T00:00:00Z",
      "end_time": "2024-01-02T00:00:00Z",
      "title": "hii",
      "attachment": "a url to the attachment",
      "description": "description",
      "content": "content",
      "sport": {
          "id": 2,
          "name": ""
      },
      "players": [
          (see Get User Profile playload above for user info),
      ],
      "level": "B",
      "age_group": "C",
      "visibility": "Public",
      "max_players": 10,
      "admins": [
          (see Get User Profile playload above for user info),
      ],
      "location": "location",
      "created_at": "2024-02-26T01:00:35.951944Z",
      "updated_at": "2024-02-26T01:02:03.325007Z"
  }
  ```

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

- **Endpoint**: `GET notifications/list/`
- **Description**: Retrieves all notifications for the current logged-in user.
- **Success Response**: 200 OK with all notifications' info.
- **Example Response**:
  ```json
   [
      {
        "id": 2,
        "event_id": 1,
        "event_title": "23",
        "description": "The following detail has been changed - start_time: 2023-01-01 00:00:00+00:00, title: 23",
        "created_at": "2024-02-27T01:28:40.340365Z",
        "read": false
      }
  ]
  ```
#### Mark Notification as Read
- **Endpoint**: `PATCH notifications/read/`
- **Description**: Marks notification as read with the following mandatory fields:
  - id
- **Success Response**: 200 OK with notification info.
- **Example Response**:
    ```json
     {
        "id": 2,
        "event_id": 1,
        "event_title": "23",
        "description": "The following detail has been changed - start_time: 2023-01-01 00:00:00+00:00, title: 23",
        "created_at": "2024-02-27T01:28:40.340365Z",
        "read": true
    }
    ```
  
#### Delete Notification by ID
- **Endpoint**: `DELETE notifications/delete/`
- **Description**: Deletes notification by ID with the following mandatory fields:
  - id
- **Success Response**: 200 OK with notification info.
  
### Search

- **Endpoint**: `GET search/{events, users}/`
- **Description**: Searches for events or users with the following query parameter:
  - for events:
    - keywords (match title, description, and content)
    - sports (list of sports)
    - levels (list of levels)
    - age_groups (list of age groups)
    - start_time
    - end_time
  - for users:
    - param (match all username, email, and name)
- **Success Response**: 200 OK with search results.
- **Example Request**: 
  - Events:`GET search/events/?keywords=ball&levels=B&levels=I&age_groups=C&sports=football&sports=basketball&start_time=2023-01-01&end_time=2024-01-01`
  - Users: `GET search/users/?param=abc`

### Make Payment
Payment will be done using PayPal. The user will be redirected to the paypal payment page and after successful payment, the user will be redirected back to the website.
The following is a sandbox account for testing on PayPal:
- **Email**: ```sb-32zaq30062667@personal.example.com```
- **Password**: ```4=z*mXly```

#### Get Payment URL
- **Endpoint**: `POST payment/create/`
- **Description**: Creates a PayPal payment link with the following mandatory fields:
  - event_id
  - amount ($ You want to pay for promotion)
  - return_url (URL to redirect after payment success)
  - cancel_url (URL to redirect after payment cancel)
- **Success Response**: 200 OK with payment URL.
- **Example Response**:
    ```json
  {
      "id": "4A885666C2430470A",
      "status": "CREATED",
      "link": "https://www.sandbox.paypal.com/checkoutnow?token=4A885666C2430470A"
  }
    ```
  Redirect the user to the link to make the payment.

#### Payment Success
- **Endpoint**: `GET payment/verify/`
- **Description**: Verifies the payment with the following mandatory fields:
  - token (token will be given at params from PayPal after successful payment)
- **Success Response**: 200 OK with payment info.
- **Example Response**:
    ```json
  {
    "id": "4A885666C2430470A",
    "intent": "CAPTURE",
    "status": "APPROVED",
    "purchase_units": [
        {
          "reference_id": "default",
            "amount": {
              "currency_code": "CAD",
              "value": "1.00"
        },
          "payee": {
            "email_address": "sb-hujrj30059819@business.example.com",
            "merchant_id": "PC8CK5LHWQL94"
          }
        }
    ],
    "create_time": "2024-03-24T18:51:52Z",
    "links": [
        {
            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/4A885666C2430470A",
            "rel": "self",
            "method": "GET"
        },
        {
            "href": "https://www.sandbox.paypal.com/checkoutnow?token=4A885666C2430470A",
            "rel": "approve",
            "method": "GET"
        },
        {
            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/4A885666C2430470A",
            "rel": "update",
            "method": "PATCH"
        },
        {
            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/4A885666C2430470A/capture",
            "rel": "capture",
            "method": "POST"
        }
      ]
  }
    ```
  Note that the payment status should be "APPROVED" is the user paid successfully.

#### Payment Cancel
- **Endpoint**: `GET payment/cancel/`
- **Description**: Redirects the user to the cancel page after payment cancel with the following mandatory fields:
  - token (token will be given at params from PayPal after payment cancel)
- **Success Response**: 200 OK with {"message": "Payment canceled!"}.
