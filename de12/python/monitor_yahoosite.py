import requests
from bs4 import BeautifulSoup

url = 'https://example-university.edu/assignments'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
session = requests.Session()
login_url = 'https://example-university.edu/login'
credentials = {
    'username': 'your-username',
    'password': 'your-password'
}
session.post(login_url, data=credentials)

# ログイン後のページへアクセス
response = session.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
# ページ内の最新課題を取得（例えばタイトルやリンク）
latest_assignment = soup.find('div', {'class': 'assignment-title'}).text

# 前回取得した課題と比較する
with open('latest_assignment.txt', 'r') as file:
    previous_assignment = file.read()

if latest_assignment != previous_assignment:
    # 通知を送信（次のステップ参照）
    with open('latest_assignment.txt', 'w') as file:
        file.write(latest_assignment)
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = 'your-email@gmail.com'
    password = 'your-email-password'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

# 更新があった場合にメール送信
send_email("新しい課題が追加されました", "新しい課題: " + latest_assignment, "your-email@gmail.com")
import requests

def send_line_notify(message):
    line_notify_token = 'YOUR_LINE_NOTIFY_TOKEN'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': message}
    requests.post(line_notify_api, headers=headers, data=data)

# LINEで通知
send_line_notify(f"新しい課題: {latest_assignment}")
import requests

def send_line_notify(message):
    line_notify_token = 'YOUR_LINE_NOTIFY_TOKEN'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': message}
    requests.post(line_notify_api, headers=headers, data=data)

# LINEで通知
send_line_notify(f"新しい課題: {latest_assignment}")
crontab -e
0 * * * * /usr/bin/python3 /path/to/your_script.py
