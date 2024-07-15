from flask import Flask, request, jsonify
import db
import flow

app = Flask(__name__)


@app.route('/process_images', methods=['POST'])
def process_images():
    req_data = request.get_json()

    # Check if username and password are correct
    username, password = req_data['username'], req_data['password']
    user_id = db.check_user(username,password)
    if user_id:
        flow.run_image_describe(user_id)
        return jsonify({'message': 'Login successful on backend'}), 200
    else:
        return jsonify({'error': 'Invalid credentials found on backend'}), 401

if __name__ == '__main__':
    app.run(debug=True)
