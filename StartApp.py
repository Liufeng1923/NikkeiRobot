from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_value():
    data = request.json  # 假设发送的数据是 JSON 格式
    value = data.get('value')
    # 根据接收到的值执行操作
    print(f"接收到的值：{value}")
    # 在这里添加代码以根据值执行特定操作
    return jsonify({"status": "success", "received_value": value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
