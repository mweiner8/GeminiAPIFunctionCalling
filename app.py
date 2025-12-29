"""
Flask backend for the Speed Camera GUI
Connects the HTML frontend with Gemini function calling
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gemini_functions import chat_with_gemini
import os

# Flask app
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """Serve the index.html file."""
    return send_from_directory('.', 'index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests from the frontend."""
    try:
        data = request.json
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Get response from Gemini (verbose=False for clean logs)
        result = chat_with_gemini(user_message, verbose=False)

        # Check if there was an error
        if "error" in result:
            return jsonify(result), 429 if "rate limit" in result["error"].lower() else 500

        return jsonify(result)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Speed Camera Assistant Backend")
    print("="*60)
    print(f"Server running on http://localhost:5000")
    print(f"Visit http://localhost:5000 in your browser to use the GUI")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)