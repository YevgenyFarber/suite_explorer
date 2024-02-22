from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
import threading
import main  # Import your main module

app = Flask(__name__)
# app.secret_key = 'your_very_secret_key'  # Replace with a strong secret key

# Global variable to store the progress
task_progress = 0


class Args:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path


def run_main_task(json_file_path):
    global task_progress
    # Call your main function and update task_progress
    main.main(json_file_path)  # Call your main function here
    task_progress = 100  # Set progress to 100% once done


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/start-task', methods=['POST'])
def start_task():
    global task_progress
    task_progress = 0
    json_file_path = ''
    if not request.form.get('json_path'):
        print("The target directory doesn't exist")
        json_file_path = Args('owners.json')
    else:
        target_dir = Path(request.form.get('json_path'))
        if not target_dir.is_file():
            print("The target directory doesn't exist")
            json_file_path = Args('owners.json')
    threading.Thread(target=run_main_task, args=(json_file_path,)).start()
    return jsonify({'status': 'started'})


@app.route('/progress')
def progress():
    return jsonify({'progress': task_progress})


# Example route to clear the session
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return 'Logged out successfully'


if __name__ == '__main__':
    app.run(debug=True)
