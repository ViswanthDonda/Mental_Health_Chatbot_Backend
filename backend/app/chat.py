from flask import Blueprint, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
import os

chat_blueprint = Blueprint('chat', __name__)

# Dialogflow project ID (replace with your actual project ID)
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
DIALOGFLOW_LANGUAGE_CODE = "en"  # Or your desired language code
SESSION_ID = "user_session"

@chat_blueprint.route('/send-message', methods=['POST'])
def send_message():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Message text is required"}), 400

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    
    text_input = dialogflow.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        return jsonify({"reply": response.query_result.fulfillment_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
