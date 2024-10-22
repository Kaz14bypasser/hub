from flask import Flask, request, render_template_string
import subprocess
import time
import requests
import json
import socket

app = Flask(__name__)


valid_api_keys = ["1234", "kaz1234", "key3"]
valid_links = ["https://gateway.platoboost.com/a/", "https://loot-link.com/s?", "https://flux.li/android/external/start.php?"]

error_log_path = './error_reports.txt'
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1298281635023687701/_vP18Zxi6_dhT2C0oageEbeFzZ2aGyvL53_5vps7v9f6VUUy-zkA8jWu-X6Drh-8Qo_Y"

html_template = """
<html>
  <head>
    <title>Web API</title>
  </head>
  <body>
    <h1>Code web bypass key </h1>
    <p>Cách dùng: http://127.0.0.1:5000/?url= (link cần bypass)&apikey= ( key nhập ở đây )</p>
    <p><a href="https://www.facebook.com/kaz2205/">Liên hệ với admin qua Facebook</a></p>
    <p><a href="https://discord.gg/UQjPG97yYV">Liên hệ với admin qua Discord</a></p>
    {% if message %}
      <p style="color: red">{{ message }}</p>
    {% endif %}
    {% if status %}
      <p style="color: green">{{ status }}</p>
    {% endif %}
    {% if key %}
      <p style="color: blue">Key bypass: {{ key }}</p>
    {% endif %}
  </body>
  <script>
    function submitForm() {
      const url = document.querySelector('input[name="url"]').value;
      const apikey = document.querySelector('input[name="apikey"]').value;
      window.location.href = `/?url=${encodeURIComponent(url)}&apikey=${encodeURIComponent(apikey)}`;
    }
  </script>
</html>
"""

@app.route('/')
def index():
    url = request.args.get('url')
    api_key = request.args.get('apikey')
    message = None
    status = None
    key = None

    if url and api_key:
       
        if api_key not in valid_api_keys:
            message = "Thông báo: Khóa API không hợp lệ."
       
        elif not any(url.startswith(link) for link in valid_links):
            message = "Thông báo: Link không hợp lệ."
        else:

            try:
                subprocess.Popen(['C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe', url])
                status = "Link và khóa API đã được xác nhận. Web đã được mở."
            except Exception as e:
                log_error(f"Lỗi khi mở CocCoc: {str(e)}")
                message = "Đã xảy ra lỗi khi cố gắng mở trình duyệt."
    else:
        message = "Vui lòng nhập link và khóa API."

    return render_template_string(html_template, url=url, api_key=api_key, message=message, status=status, key=key)

@app.route('/report_error', methods=['POST'])
def report_error():
    error_message = request.form.get('error_message')
    log_error(error_message)
    return "Cảm ơn bạn đã báo cáo lỗi."


def log_error(error_message):
    with open(error_log_path, 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")
    
    
    requests.post(DISCORD_WEBHOOK_URL, json={"content": error_message})

@app.route('/timeapi')
def timeapi():
    start_time = time.time()
    ip_address = request.remote_addr
    
    duration = time.time() - start_time
    return f"Tốc độ thời gian web đã chạy: {duration:.2f} giây, Vị trí IP: {ip_address}"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
