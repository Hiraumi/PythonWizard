from flask import Blueprint, request, jsonify
import subprocess

# 创建一个蓝图
run_code_bp = Blueprint('run_code', __name__)

# 定义 /run_code 路由
@run_code_bp.route('/run_code', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "代码为空"}), 400

    try:
        # 使用 subprocess 执行用户代码
        result = subprocess.run(
            ["python3", "-c", code],
            text=True,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return jsonify({"output": result.stdout}), 200
        else:
            return jsonify({"error": result.stderr}), 400
    except subprocess.TimeoutExpired:
        return jsonify({"error": "代码运行超时"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
