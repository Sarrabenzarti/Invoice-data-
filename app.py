from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/segmentation', methods=['POST'])
def segmentation():
    # Placeholder: implement segmentation model inference here
    data = request.get_json() or {}
    # result = run_segmentation_model(data)
    result = {'message': 'Segmentation model not implemented yet', 'input': data}
    return jsonify(result)

@app.route('/api/detection', methods=['POST'])
def detection():
    # Placeholder: implement detection model inference here
    data = request.get_json() or {}
    # result = run_detection_model(data)
    result = {'message': 'Detection model not implemented yet', 'input': data}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
