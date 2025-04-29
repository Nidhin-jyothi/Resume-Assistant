from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import uuid
import json

from extract import (
    extract_text_from_pdf,
    extract_resume_details,
    score_candidate_for_ai,
    add_candidate_to_vectorstore
)
from chatbot import chatbot_answer

app = Flask(__name__)
CORS(app)

os.makedirs('temp', exist_ok=True)
app.config['UPLOAD_FOLDER'] = 'temp/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

global_resume_data = []

@app.route('/')
def index():
    return render_template('index.html', resumes=global_resume_data)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"error": "Bad Request", "message": "No files uploaded"}), 400

    files = request.files.getlist('files')
    results = []

    for file in files:
        if not file or file.filename == '':
            continue

        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(filepath)
            text = extract_text_from_pdf([filepath])
            details = extract_resume_details(text)

            try:
                score_obj = json.loads(score_candidate_for_ai(details))
                details['role_tags'] = score_obj.get('role_tags', {})
            except:
                details['role_tags'] = {}

            add_candidate_to_vectorstore(details)
            global_resume_data.append(details)
            results.append(details)

        except Exception as e:
            return jsonify({"error": "Processing Error", "message": str(e)}), 500
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    return jsonify({
        "message": f"Successfully processed {len(results)} resumes",
        "results": results
    })

@app.route('/chat', methods=['POST'])
def handle_chat():
    data = request.get_json(silent=True) or {}
    query = data.get('query')

    if not query:
        return jsonify({"error": "Bad Request", "message": "Missing query parameter"}), 400

    try:
        answer = chatbot_answer(query)
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": "Chat Error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
