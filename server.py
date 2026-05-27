import json
import os
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
# 导入原有功能模块
from catch import get_cct_and_contentkey
from decryption import aes_cbc_decrypt
from download import download_images

app = Flask(__name__)
# 允许跨域（插件请求本地服务需要）
CORS(app, resources={r"/download": {"origins": "*"}})

def download_manga(url):
    """封装原有下载逻辑"""
    try:
        # 提取参数 + 漫画名、章节名
        cct, content_key, comic_title, chapter_name = get_cct_and_contentkey(url)
        
        if not cct or not content_key:
            raise ValueError("提取cct/content_key失败")
        
        # 拼接两级文件夹路径
        save_path = os.path.join(comic_title, chapter_name)

        # 解密图片URL
        decrypt_raw = aes_cbc_decrypt(cct, content_key)
        image_urls = json.loads(decrypt_raw)

        # 下载图片
        download_images(image_urls, save_path)
        return True, "下载成功"
    except Exception as e:
        return False, str(e)

@app.route('/download', methods=['POST'])
def handle_download():
    """接收插件的下载请求"""
    try:
        # 获取请求中的URL
        data = request.get_json()
        if not data or not data.get('url'):
            return jsonify({
                "code": 400,
                "msg": "URL不能为空"
            })
        
        url = data.get('url')
        # 异步执行下载（避免阻塞HTTP响应）
        threading.Thread(
            target=lambda: download_manga(url),
            daemon=True
        ).start()

        return jsonify({
            "code": 200,
            "msg": "下载任务已启动"
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"服务端错误：{str(e)}"
        })

if __name__ == "__main__":
    print("="*60)
    print("🚀 漫画下载服务已启动 | 地址：http://localhost:5000")
    print("="*60)
    # 启动Flask服务（允许外部访问，端口5000）
    app.run(host='127.0.0.1', port=5000, debug=False)