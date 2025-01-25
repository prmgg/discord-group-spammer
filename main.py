import aiohttp
import asyncio
import json

async def send_request(session, url, headers, data):
    async with session.post(url, headers=headers, json=data) as response:
        resp_json = await response.json()
        return resp_json

async def main():
    token = input("トークンを入力してください: ")
    num_requests = int(input("何回グループを作成しますか？: "))

    url = "https://discord.com/api/v9/users/@me/channels"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Accept": "*/*",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        "Content-Type": "application/json",
        "Authorization": token,
        "X-Context-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJqYSIsImhhc19jbGllbnRfbW9kcyI6ZmFsc2UsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEzNC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEzNC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTM0LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MzYyMzkyLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
        "X-Discord-Locale": "ja",
        "X-Discord-Timezone": "Asia/Shanghai"
    }
    
    recipients = []
    num_users = int(input("何人のユーザーを追加しますか？: "))
    if num_users < 2:
        print("2人以上のユーザーが必要です。")
        return
    
    for i in range(num_users):
        recipients.append(input(f"{i + 1}人目のユーザーIDを入力してください: "))

    data = {"recipients": recipients}

    async with aiohttp.ClientSession() as session:
        for _ in range(num_requests):
            response = await send_request(session, url, headers, data)
            if 'id' in response:
                with open("id.txt", "a") as file:
                    file.write(response['id'] + "\n")
                print(f"ID: {response['id']}")
            else:
                print("IDが含まれていません。")

if __name__ == "__main__":
    asyncio.run(main())
