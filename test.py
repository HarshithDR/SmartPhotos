import tempfile
import flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b'Hello, World!')

    # Get the temporary file path
    temp_file_path = temp_file.name

    # print(f'Temporary file path: {temp_file_path}')
    return temp_file_path

if __name__ == '__main__':
    app.run(debug=True)
