from flask import Flask, request
from utils import detect
import time

app = Flask(__name__)

@app.route('/fraud/detection', methods=['POST'])
def detect_fraud():
    data = request.get_json()

    rule_violated = detect(data)
    status = "ALERT"

    if (rule_violated == []):
        status = "OK"  # or "ALERT" based on your logic

    result = {
        "status": status,
        "ruleViolated": rule_violated,
        "timestamp": str(int(time.time()))
    }

    return result

if __name__ == '__main__':
    app.run()