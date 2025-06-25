from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)  # Allow React frontend to make requests

@app.route('/run_test', methods=['POST'])
def run_test():
    try:
        test_data = request.get_json()

        # Save the incoming test case to single_test.json for immediate execution
        with open('single_test.json', 'w') as f:
            json.dump(test_data, f, indent=2)

        # Append the same test case to dynamic_test_cases.json (history of dynamic runs)
        dynamic_file = 'dynamic_test_cases.json'
        if os.path.exists(dynamic_file):
            with open(dynamic_file, 'r') as f:
                existing_tests = json.load(f)
        else:
            existing_tests = []

        existing_tests.append(test_data)

        with open(dynamic_file, 'w') as f:
            json.dump(existing_tests, f, indent=2)

        # Run the single test using the test runner
        result = subprocess.run(
            ['python3', 'run_tests.py', '--single-test'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return jsonify({
            'output': result.stdout,
            'error': result.stderr,
            'success': result.returncode == 0
        })

    except Exception as e:
        print(f"Backend error: {e}")  # Logs in terminal
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
