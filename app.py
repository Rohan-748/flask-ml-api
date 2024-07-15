from flask import Flask, request, jsonify, abort
app = Flask(__name__)
# Example WML credentials (replace with your actual credentials)
WML_CREDENTIALS = {
    "url": "https://namespace1-cpd-namespace1.apps.xxxxx.os.fyre.ibm.com",
    "username": "admin",
    "password": "xxxx",
    "instance_id": "wml_local",
    "version": "3.5"
}
# Mock function to generate scoring payload
def get_scoring_payload(no_of_records_to_score):
    payload = {
        "input_data": []
    }
    for i in range(no_of_records_to_score):
        payload["input_data"].append(["Name{}".format(i), 30 + i, "Position{}".format(i % 2)])
    return payload

# Mock function to perform custom ML scoring
def custom_ml_scoring(payload_scoring):
    output_values = []
    for data in payload_scoring["input_data"]:
        prediction = "personal" if data[2] == "Position0" else "camping"
        probability = [0.7, 0.3] if prediction == "personal" else [0.3, 0.7]
        output_values.append(data + [prediction, probability])
    return {
        "fields": ["name", "age", "position", "prediction", "probability"],
        "labels": ["personal", "camping"],
        "values": output_values
    }
@app.route('/spaces/<space_id>/deployments/<deployment_id>/predictions', methods=['POST'])
def wml_scoring(space_id, deployment_id):
    if not request.json:
        abort(400)
    no_of_records_to_score = request.json.get('no_of_records_to_score', 1)
    payload_scoring = get_scoring_payload(no_of_records_to_score)
    scoring_response = custom_ml_scoring(payload_scoring)
    return jsonify(scoring_response)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
