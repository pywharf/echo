import os

from flask import Flask, current_app, request
import waitress
from paste.translogger import TransLogger

app = Flask(__name__)  # pylint: disable=invalid-name


@app.route('/set/<name>', methods=['POST'])
def api_set(name):
    current_app.storage[name] = request.get_data(as_text=True)
    return f'Set {name}', 200


@app.route('/get/<name>', methods=['GET'])
def api_get(name):
    if name not in current_app.storage:
        return 'N/A', 404
    return current_app.storage[name], 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    ECHO_HOST = os.getenv('ECHO_HOST', '0.0.0.0')
    ECHO_PORT = os.getenv('ECHO_PORT', '9999')

    with app.app_context():
        current_app.storage = {}

    waitress.serve(
            TransLogger(app, setup_console_handler=False),
            host=ECHO_HOST,
            port=ECHO_PORT,
    )
