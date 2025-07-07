import os
import requests
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Konfigurasi Token Bot dan Unsplash API Key
TELEGRAM_BOT_TOKEN = "7834641455:AAHZ9zqT1NvV39o6WANeGyR-x6w-Xc698_A"
UNSPLASH_ACCESS_KEY = "oZZeDnCq0lFi5r11Fj22pMFg5FLbqTHpvP7ZbA57pQ8"

# URL API Unsplash
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mengirim pesan selamat datang saat perintah /start diterima."""
    await update.message.reply_text(
        "Halo! 👋 Saya bot pencari foto Unsplash. Kirimkan kata kunci foto yang ingin kamu cari, "
        "misalnya 'kucing lucu' atau 'pemandangan gunung'."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mengirim pesan bantuan saat perintah /help diterima."""
    await update.message.reply_text(
        "Untuk mencari foto, cukup ketikkan kata kunci yang kamu inginkan. "
        "Contoh: 'bunga mawar', 'sunset di pantai'.\n"
        "Saya akan mencoba mencarikan 3 foto terbaik untukmu."
    )

async def search_photos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mencari foto di Unsplash berdasarkan kata kunci dari pengguna."""
    query = update.message.text
    if not query:
        await update.message.reply_text("Mohon masukkan kata kunci untuk mencari foto.")
        return

    params = {
        "query": query,
        "client_id": UNSPLASH_ACCESS_KEY,
        "per_page": 3  # Mengambil 3 foto per pencarian
    }

    try:
        response = requests.get(UNSPLASH_API_URL, params=params)
        response.raise_for_status()  # Angkat HTTPError untuk respons status yang buruk (4xx atau 5xx)
        data = response.json()

        if data and data["results"]:
            photos = data["results"]
            media = []
            for photo in photos:
                if "urls" in photo and "regular" in photo["urls"]:
                    media.append(InputMediaPhoto(media=photo["urls"]["regular"]))
            
            if media:
                await update.message.reply_media_group(media=media)
                await update.message.reply_text(f"Ini dia 3 foto terbaik untuk '{query}' dari Unsplash.")
            else:
                await update.message.reply_text(f"Maaf, tidak ada foto yang ditemukan untuk '{query}'. Coba kata kunci lain.")
        else:
            await update.message.reply_text(f"Maaf, tidak ada foto yang ditemukan untuk '{query}'. Coba kata kunci lain.")

    except requests.exceptions.RequestException as e:
        print(f"Error saat memanggil API Unsplash: {e}")
        await update.message.reply_text(
            "Maaf, terjadi kesalahan saat mencoba mengambil foto. Silakan coba lagi nanti."
        )
    except Exception as e:
        print(f"Error tak terduga: {e}")
        await update.message.reply_text(
            "Terjadi kesalahan yang tidak terduga. Mohon laporkan jika ini sering terjadi."
        )

def main() -> None:
    """Menjalankan bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Menambahkan handler perintah
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Menambahkan handler pesan teks untuk mencari foto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_photos))

    # Jalankan bot
    print("Bot sedang berjalan...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
