
from flask import Flask, request, jsonify
from extractor import extract_data_from_pdf

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    print('>>> PING reçue')
    return 'pong'

@app.route('/api/invoice-extract', methods=['POST'])
def extract_invoice():
    print('>>> API appelée')
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    result = extract_data_from_pdf(file)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
