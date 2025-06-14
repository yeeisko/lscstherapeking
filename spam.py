import asyncio
from telegram import Bot

bot = Bot(token="7531550158:AAHoBNmHr2spJ_PkAAArvBjRyIzSjuRVhYY")

async def spam_user(chat_id, username):
    message = f"@{username}, you have been viol BY THE KING LSCS FOR NO WORK!!"
    sticker_id = "CAACAgEAAyEFAASfA9PJAAII22hNi6t2DEowr7zJ4ciHZzai8Ur_AAJyBAACW0QQR51COmFpIaY8NgQ"  # Example sticker ID

    while True:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            await bot.send_sticker(chat_id=chat_id, sticker=sticker_id)
        except Exception as e:
            print(f"Error sending message: {e}")
        await asyncio.sleep(1)
