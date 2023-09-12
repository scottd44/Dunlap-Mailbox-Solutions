import pyrebase

def get_firebase_configuration():
    config = {
        "apiKey": "AIzaSyCPIR0bLyq7wrY8Qr3_WE8_6JBx_RVt-u4",
        "authDomain": "atlwildin-1128.firebaseapp.com",
        "projectId": "atlwildin-1128",
        "storageBucket": "atlwildin-1128.appspot.com",
        "messagingSenderId": "226559882335",
        "appId": "1:226559882335:web:8eedc3a07ee5dca14497ea",
        "measurementId": "G-SHGKCJ46VW",
        "databaseURL": ""
    }

    # Initialising database,auth and firebase for further use
    firebase = pyrebase.initialize_app(config)
    authe = firebase.auth()
    database = firebase.database()

    return config, firebase, authe, database