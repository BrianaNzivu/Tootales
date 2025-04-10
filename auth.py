from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from firebase_config import auth  # Pyrebase config (for Email/Password)
import firebase_admin
from firebase_admin import credentials, firestore, auth as admin_auth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Firebase Admin if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Create the authentication blueprint
auth_bp = Blueprint("auth_bp", __name__)

# --------- Email/Password Signup ----------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        try:
            # Create user with Email/Password using Pyrebase
            user = auth.create_user_with_email_and_password(email, password)
            uid = user["localId"]
            # Save additional user info in Firestore
            db.collection("users").document(uid).set({
                "username": username,
                "email": email,
                "provider": "password"
            })
            session["user_id"] = uid
            session["user_name"] = username
            return redirect(url_for("home"))
        except Exception as e:
            print("Signup error:", e)
            error_message = str(e)
            if "EMAIL_EXISTS" in error_message:
                error_message = "Email already in use. Please try logging in."
            elif "WEAK_PASSWORD" in error_message:
                error_message = "Password is too weak. Please use a stronger password."
            else:
                error_message = "Signup failed. Please try again."
            return render_template("signup.html", error=error_message)
    return render_template("signup.html")

# --------- Email/Password Login ----------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            # Sign in with Email/Password using Pyrebase
            user = auth.sign_in_with_email_and_password(email, password)
            uid = user["localId"]
            user_doc = db.collection("users").document(uid).get()
            user_data = user_doc.to_dict() if user_doc.exists else {}
            session["user_id"] = uid
            session["user_name"] = user_data.get("username", "User")
            return redirect(url_for("home"))
        except Exception as e:
            print("Login error:", e)
            error_message = str(e)
            if "INVALID_PASSWORD" in error_message:
                error_message = "Invalid password. Please try again."
            elif "EMAIL_NOT_FOUND" in error_message:
                error_message = "Email not found. Please sign up first."
            else:
                error_message = "Login failed. Please try again."
            return render_template("login.html", error=error_message)
    return render_template("login.html")

# --------- Google Sign-In ----------
@auth_bp.route("/google_sign_in", methods=["POST"])
def google_sign_in():
    """
    Expects a JSON payload with an 'idToken' obtained from the client
    after signing in with Google using Firebase's JavaScript SDK.
    """
    data = request.get_json()
    id_token = data.get("idToken")
    if not id_token:
        return jsonify({"error": "Missing ID token"}), 400
    try:
        # Verify the ID token using Firebase Admin SDK
        decoded_token = admin_auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        
        # Try to get the user's Firestore document; if not found, create one.
        user_ref = db.collection("users").document(uid)
        if not user_ref.get().exists:
            username = decoded_token.get("name", "Google User")
            email = decoded_token.get("email", "")
            user_ref.set({
                "username": username,
                "email": email,
                "provider": "google"
            })
            session["user_name"] = username
        else:
            user_data = user_ref.get().to_dict()
            session["user_name"] = user_data.get("username", decoded_token.get("name", "Google User"))
        
        session["user_id"] = uid
        return jsonify({"success": True})
    except Exception as e:
        print("Google sign-in error:", e)
        return jsonify({"error": "Google sign-in failed"}), 400

# --------- Logout ----------
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_bp.login"))