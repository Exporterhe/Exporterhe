"""
公众号文章下载工具 - Web 界面
启动方式: python web_ui.py
然后在浏览器打开 http://localhost:5000
"""

import os
import sys
import threading
import base64
from flask import Flask, render_template_string, request, jsonify, send_file
from werkzeug.serving import make_server
import io

# 导入下载器
from wechat_downloader import WechatDownloader

app = Flask(__name__)

# 全局变量存储下载状态
download_status = {
    'status': 'idle',  # idle, downloading, completed, error
    'message': '',
    'progress': 0,
    'result': None,
    'error': None
}


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>公众号文章下载器</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            width: 100%;
            max-width: 700px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        input[type="text"] {
            width: 100%;
            padding: 14px 16px;
            border: 2px solid #e1e1e1;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .progress-container {
            margin-top: 30px;
            display: none;
        }
        .progress-bar {
            height: 8px;
            background: #e1e1e1;
            border-radius: 4px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s;
        }
        .progress-text {
            margin-top: 10px;
            color: #666;
            font-size: 14px;
            text-align: center;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }
        .result.success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .result.error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .result h3 {
            margin-bottom: 10px;
        }
        .result p {
            margin: 5px 0;
        }
        .log {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            max-height: 200px;
            overflow-y: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            color: #333;
            display: none;
        }
        .log-line {
            margin: 3px 0;
            padding: 2px 0;
            border-bottom: 1px solid #eee;
        }
        .sample-links {
            margin-top: 20px;
            padding: 15px;
            background: #f0f4ff;
            border-radius: 10px;
            font-size: 13px;
        }
        .sample-links h4 {
            margin-bottom: 10px;
            color: #555;
        }
        .sample-link {
            display: inline-block;
            margin: 5px 5px 5px 0;
            padding: 6px 12px;
            background: white;
            border: 1px solid #d0d7ff;
            border-radius: 20px;
            color: #667eea;
            text-decoration: none;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .sample-link:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            color: #999;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📰 公众号文章下载器</h1>
        <p class="subtitle">输入微信文章链接，一键下载为 Markdown 文件（包含本地图片）</p>

        <div class="input-group">
            <label for="url">文章链接</label>
            <input type="text" id="url" placeholder="https://mp.weixin.qq.com/s/..." />
        </div>

        <button class="btn" id="downloadBtn" onclick="startDownload()">
            开始下载
        </button>

        <div class="sample-links">
            <h4>示例链接（点击填充）：</h4>
            <span class="sample-link" onclick="fillUrl('https://mp.weixin.qq.com/s/SZDs9Koj1yFxNVhT-3vt9w')">
                架构文章
            </span>
            <span class="sample-link" onclick="fillUrl('https://mp.weixin.qq.com/s/xxxxxxxxxx')">
                其他文章
            </span>
        </div>

        <div class="progress-container" id="progressContainer">
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <p class="progress-text" id="progressText">准备下载...</p>
        </div>

        <div class="log" id="logContainer"></div>

        <div class="result" id="resultContainer"></div>

        <div class="footer">
            公众号文章下载器 v2.0 | Python + Flask
        </div>
    </div>

    <script>
        let statusInterval;

        function fillUrl(url) {
            document.getElementById('url').value = url;
        }

        function startDownload() {
            const url = document.getElementById('url').value.trim();
            if (!url) {
                alert('请输入文章链接');
                return;
            }

            const btn = document.getElementById('downloadBtn');
            btn.disabled = true;
            btn.textContent = '下载中...';

            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('resultContainer').style.display = 'none';
            document.getElementById('logContainer').style.display = 'block';
            document.getElementById('logContainer').innerHTML = '';
            document.getElementById('progressFill').style.width = '0%';

            // 启动轮询
            statusInterval = setInterval(checkStatus, 500);

            // 开始下载
            fetch('/download', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            });
        }

        function checkStatus() {
            fetch('/status')
                .then(r => r.json())
                .then(data => {
                    // 更新进度条
                    document.getElementById('progressFill').style.width = data.progress + '%';
                    document.getElementById('progressText').textContent = data.message;

                    // 添加日志
                    if (data.log) {
                        const logContainer = document.getElementById('logContainer');
                        const lines = data.log.split('\\n');
                        lines.forEach(line => {
                            if (line.trim()) {
                                const div = document.createElement('div');
                                div.className = 'log-line';
                                div.textContent = line;
                                logContainer.appendChild(div);
                            }
                        });
                        logContainer.scrollTop = logContainer.scrollHeight;
                    }

                    // 下载完成
                    if (data.status === 'completed' || data.status === 'error') {
                        clearInterval(statusInterval);
                        showResult(data);
                    }
                });
        }

        function showResult(data) {
            const btn = document.getElementById('downloadBtn');
            btn.disabled = false;
            btn.textContent = '开始下载';

            const resultContainer = document.getElementById('resultContainer');
            resultContainer.style.display = 'block';

            if (data.status === 'completed') {
                resultContainer.className = 'result success';
                resultContainer.innerHTML = `
                    <h3>✅ 下载完成！</h3>
                    <p><strong>文章标题：</strong>${data.result.title}</p>
                    <p><strong>下载图片：</strong>${data.result.images_count} 张</p>
                    <p><strong>保存位置：</strong>当前目录</p>
                    <p style="margin-top: 15px; font-size: 13px; color: #666;">
                        Markdown 文件和图片文件夹已保存到运行目录下
                    </p>
                `;
            } else {
                resultContainer.className = 'result error';
                resultContainer.innerHTML = `
                    <h3>❌ 下载失败</h3>
                    <p>${data.error}</p>
                `;
            }

            document.getElementById('progressContainer').style.display = 'none';
        }
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/download', methods=['POST'])
def download():
    global download_status

    data = request.get_json()
    url = data.get('url', '')

    # 重置状态
    download_status = {
        'status': 'downloading',
        'message': '正在获取页面...',
        'progress': 10,
        'result': None,
        'error': None,
        'log': ''
    }

    def run_download():
        global download_status
        downloader = WechatDownloader()
        try:
            download_status['log'] += '正在连接服务器...\n'
            result = downloader.download(url, '.')
            download_status['status'] = 'completed'
            download_status['message'] = '下载完成！'
            download_status['progress'] = 100
            download_status['result'] = result
            download_status['log'] += f"完成！文章: {result['title']}\n"
            download_status['log'] += f"保存图片: {result['images_count']} 张\n"
        except Exception as e:
            download_status['status'] = 'error'
            download_status['error'] = str(e)
            download_status['log'] += f"错误: {e}\n"

    thread = threading.Thread(target=run_download)
    thread.daemon = True
    thread.start()

    return jsonify({'status': 'started'})


@app.route('/status')
def status():
    global download_status
    return jsonify(download_status)


def main():
    print("=" * 50)
    print("🚀 公众号文章下载器 Web 界面已启动")
    print("=" * 50)
    print("📍 请在浏览器打开: http://localhost:5000")
    print("=" * 50)
    print("按 Ctrl+C 停止服务")
    print()

    server = make_server('127.0.0.1', 5000, app, threaded=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
