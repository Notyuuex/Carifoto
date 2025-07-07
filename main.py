import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Ganti dengan token bot kamu
BOT_TOKEN = "7834641455:AAHZ9zqT1NvV39o6WANeGyR-x6w-Xc698_A"

# Ganti dengan API Key Unsplash kamu
UNSPLASH_ACCESS_KEY = "TpPOIXVKfag9vVxBnR_MzGWH7emyXfm2Dc1C2vkbE9c"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Halo! Kirim kata kunci untuk mencari foto.\nContoh: kucing lucu")

@dp.message_handler()
async def search_photo(message: types.Message):
    query = message.text

    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data["results"]:
                    img_url = data["results"][0]["urls"]["regular"]
                    await message.reply_photo(photo=img_url)
                else:
                    await message.reply("Foto tidak ditemukan.")
            else:
                await message.reply("Terjadi kesalahan saat mencari foto.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
