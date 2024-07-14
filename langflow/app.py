from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/userid_details', methods=['GET', 'POST'])
def userid_details():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user_id = data.get('userid')
        else:
            user_id = request.form.get('userid')
    else:
        user_id = request.args.get('userid')
    
    if user_id:
        return jsonify({'User ID': user_id})
    else:
        return jsonify({'error': 'No User ID provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
