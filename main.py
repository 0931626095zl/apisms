from flask import Flask, request, jsonify
import subprocess
import threading
import requests

app = Flask(__name__)

API_KEY_CHECK_URL = "https://dstat.vinaddns.com/getkey/api/key.php?key="

def validate_api_key(key):
    try:
        response = requests.get(API_KEY_CHECK_URL + key)
        if response.status_code == 200 and response.json().get("Status") == "success":
            return True, response.json().get("key")
    except requests.RequestException:
        pass
    return False, None

def authenticate_key(func):
    def wrapper(*args, **kwargs):
        key = request.args.get("key")
        is_valid, key_info = validate_api_key(key)
        if not is_valid:
            return jsonify({"error": "Invalid API key"}), 403
        return func(*args, key_info=key_info, **kwargs)
    return wrapper

@app.route('/api', methods=['GET'])
@authenticate_key
def execute_tool(key_info):
    try:
        methods = request.args.get('methods', 'Methods')
        sdt = request.args.get('sdt', '')
        time = request.args.get('time', '')

        # Kiểm tra xem số điện thoại có trong danh sách cần kiểm tra hay không
        invalid_numbers = ["113", "09876333232", "114", "911", "111", "112", "115"]
        if sdt in invalid_numbers:
            return jsonify({"Status": "error", "Noti": "Playing stupid, kid"}), 400

        if not (methods and sdt and time):
            return jsonify({"Status": "error", "Noti": "Please enter complete information"}), 400

        valid_methods = [
            "sms1", "sms2", "sms3", "sms4"
        ]
        if methods not in valid_methods:
            return jsonify({"Status": "error", "Noti": "Method does not exist or is missing, please re-enter"}), 400

        def execute_command():
            if methods == "sms1":
                command = ['python', 'sms.py', sdt, time]
            elif methods == "sms2":
                command = ['python', 'sms.py', sdt, time]
            elif methods == "sms3":
                command = ['python', 'sms.py', sdt, time]
            elif methods == "sms4":
                command = ['python', 'sms.py', sdt, time]
            else:
                print(f"Undefined method: {methods}")
                return

            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=180)
                print(result.stdout)
                print(result.stderr)
            except subprocess.TimeoutExpired:
                print("The execution command has timed out.")
            except Exception as e:
                print(f"Error while executing command: {e}")

        threading.Thread(target=execute_command).start()

        result = {
            'Status': 'Success',
            'time': time,
            'Spam phone number': sdt,
            'spam mode': methods,
            'Owner': 'trong pro',
            'key': key_info
        }

        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Lỗi máy chủ nội bộ'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=800, debug=True)