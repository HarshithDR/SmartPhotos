from flask import Flask, request, jsonify
import db
import flow

app = Flask(__name__)


@app.route('/process_images', methods=['POST'])
def process_images():
    req_data = request.get_json()

    # Check if username and password are correct
    username, password = req_data['user_id'], req_data['password']
    user_id = db.check_user(username,password)
    print(user_id)
    if user_id:
        flow.run_image_describe(req_data['user_id'],user_id)
        return jsonify({'message': 'Login successful on backend'}), 200
    else:
        return jsonify({'error': 'Invalid credentials found on backend'}), 401
    
    
@app.route('/chat_query', methods=['POST'])
def chat_query(): #accepts {query,username,password}
    data = request.get_json()
    user_id = db.check_user(data['user_id'],data['password'])
    
    ai_response ,image_id = flow.query_flow(data['user_id'],user_id, data['query'])
    if image_id:
        return jsonify({'message':"success","ai_response":ai_response,"image_id":image_id})
    else:
        return jsonify({'Error':'Error !!'})

if __name__ == '__main__':
    app.run(debug=True)
