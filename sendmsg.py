import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

token = input("トークンを入力してください: ")

async def send():
    group_ids = []
    with open("id.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                group_ids.append(line)
    logging.info(f"{len(group_ids)} 個のグループIDが読み込まれました。")

    common_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Accept": "*/*",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        "Content-Type": "application/json",
        "Authorization": token,
        "X-Super-Properties": (
            "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsI"
            "nN5c3RlbV9sb2NhbGUiOiJqYSIsImhhc19jbGllbnRfbW9kcyI6ZmFsc2UsImJyb3dz"
            "ZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0"
            "OyB4NjQ7IHJ2OjEzNC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEzNC4wIiwiYnJvd"
            "3Nlcl92ZXJzaW9uIjoiMTM0LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6Ii"
            "IsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJ"
            "yaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwi"
            "Y2xpZW50X2J1aWxkX251bWJlciI6MzYyMzkyLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxs"
        ),
        "X-Discord-Locale": "ja",
        "X-Discord-Timezone": "Asia/Tokyo",  
        "X-Debug-Options": "bugReporterEnabled",
    }

    async with aiohttp.ClientSession() as session:
        for idx, group_id in enumerate(group_ids, start=1):
            logging.info(f"{idx} / {len(group_ids)}: グループID = {group_id} の処理を開始します。")

            patch_url = f"https://discord.com/api/v9/channels/{group_id}"
            rename_json = {"name": "あう!!!"}

            try:
                async with session.patch(patch_url, headers=common_headers, json=rename_json) as patch_response:
                    if patch_response.status == 200:
                        logging.info(f"グループ {group_id} の名前を 'あう' に変更しました。")
                    else:
                        logging.warning(
                            f"グループ {group_id} の名前変更に失敗しました。"
                            f"ステータスコード: {patch_response.status}"
                        )
                        error_text = await patch_response.text()
                        logging.warning(f"レスポンス: {error_text}")

            except Exception as e:
                logging.error(f"グループ {group_id} の名前変更時にエラー発生: {e}")

            msg_url = f"https://discord.com/api/v9/channels/{group_id}/messages"
            message_json = {
                "mobile_network_type": "unknown",
                "content": "@everyone",
                "tts": False,
                "flags": 0
            }

            try:
                async with session.post(msg_url, headers=common_headers, json=message_json) as msg_response:
                    if 200 <= msg_response.status < 300:
                        logging.info(f"グループ {group_id} にメッセージを送信しました。")
                    else:
                        logging.warning(
                            f"グループ {group_id} へのメッセージ送信に失敗しました。"
                            f"ステータスコード: {msg_response.status}"
                        )
                        error_text = await msg_response.text()
                        logging.warning(f"レスポンス: {error_text}")

            except Exception as e:
                logging.error(f"グループ {group_id} へのメッセージ送信中にエラー発生: {e}")


        logging.info("全てのグループへの処理が完了しました。")

asyncio.run(send())
