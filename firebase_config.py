import pyrebase

firebase_config = {
    "apiKey": "AIzaSyAHjDQsqvU-OXjpNIzgg8nQrz6m5YWOL6o",
    "authDomain": "tootales.firebaseapp.com",
    "projectId": "tootales",
    "storageBucket": "tootales.appspot.com",
    "messagingSenderId": "167743847585",
    "appId": "1:167743847585:web:dummyappidfornow",
    "measurementId": "G-DUMMYID",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
