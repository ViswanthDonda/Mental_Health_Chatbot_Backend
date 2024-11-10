from flask import Blueprint, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

auth_blueprint = Blueprint('auth', __name__)

# GCP Client ID (replace with your actual client ID)
GCP_CLIENT_ID = os.getenv("GCP_CLIENT_ID")

@auth_blueprint.route('/login', methods=['POST'])
def login():
    token = request.json.get("id_token")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GCP_CLIENT_ID)
        return jsonify({"status": "success", "user_id": idinfo["sub"]}), 200
    except ValueError:
        return jsonify({"error": "Invalid token"}), 403

@auth_blueprint.route('/check-token', methods=['POST'])
def check_token():
    token = request.json.get("id_token")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GCP_CLIENT_ID)
        return jsonify({"status": "valid", "user_id": idinfo["sub"]}), 200
    except ValueError:
        return jsonify({"status": "invalid"}), 403
