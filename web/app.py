from flask import Flask, request, render_template, jsonify
from utils_tools.api_client import APIClient
import os

app = Flask(__name__, template_folder='../templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        req_type = request.form['req_type']
        req_path = request.form['req_path']
        req_body = request.form.get('req_body', '')

        with APIClient() as client:
            if req_type.upper() == 'GET':
                response = client.get(req_path)
            elif req_type.upper() == 'POST':
                response = client.post(req_path, data=req_body)
            elif req_type.upper() == 'PUT':
                response = client.put(req_path, data=req_body)
            elif req_type.upper() == 'DELETE':
                response = client.delete(req_path)
            else:
                return jsonify({'error': 'Invalid request type'}), 400

        return jsonify(response)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
