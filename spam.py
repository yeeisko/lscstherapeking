from aiohttp import web
import aiohttp
import os

BOT_TOKEN = os.getenv('7531550158:AAHoBNmHr2spJ_PkAAArvBjRyIzSjuRVhYY')  # Set your bot token as environment variable
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

sticker_id = 'CAACAgEAAyEFAASfA9PJAAII22hNi6t2DEowr7zJ4ciHZzai8Ur_AAJyBAACW0QQR51COmFpIaY8NgQ'  # Replace with your sticker file_id

async def send_message(chat_id, text):
    url = f'{API_URL}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            return await resp.json()

async def send_sticker(chat_id, sticker):
    url = f'{API_URL}/sendSticker'
    payload = {'chat_id': chat_id, 'sticker': sticker}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            return await resp.json()

async def handle_viol(request):
    data = await request.json()
    chat_id = data.get('chat_id')
    if not chat_id:
        return web.json_response({'status': 'chat_id not provided'}, status=400)

    message_text = "you have been viol BY THE KING LSCS FOR NO WORK!!"
    await send_message(chat_id, message_text)
    await send_sticker(chat_id, sticker_id)

    return web.json_response({'status': 'Message and sticker sent!'})

app = web.Application()
app.router.add_post('/send_viol', handle_viol)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    web.run_app(app, port=port)
