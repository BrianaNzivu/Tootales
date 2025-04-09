import pyrebase

# Replace with your Firebase Web config
firebase_config = {
    "apiKey": "YOUR-API-KEY",
    "authDomain": "your-app.firebaseapp.com",
    "projectId": "your-app",
    "storageBucket": "your-app.appspot.com",
    "messagingSenderId": "SENDER_ID",
    "appId": "APP_ID",
    "measurementId": "MEASUREMENT_ID",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
