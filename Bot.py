import telebot
from telebot import types

TOKEN = '9286457644:AAHJFMLrhOEx5Hz2tTkHK6YVAfriLozhWfI'
bot = telebot.TeleBot(TOKEN)

# Foydalanuvchilar ID'larini saqlab turish uchun to'plam (Set)
users_set = set()

# Asosiy menyu klaviaturasi
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_weather = types.KeyboardButton("🌤 Ob-havo")
    btn_fuel = types.KeyboardButton("⛽️ Yoqilg'i narxlari")
    btn_nav = types.KeyboardButton("📍 Navigatsiya / Joylashuv")
    btn_stats = types.KeyboardButton("👥 Botdagi odamlar soni")
    btn_help = types.KeyboardButton("ℹ️ Yordam")
    markup.add(btn_weather, btn_fuel, btn_nav, btn_stats, btn_help)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Har bir /start bosgan odamni ro'yxatga qo'shamiz
    users_set.add(message.chat.id)
    
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! Nukus Avto Botiga xush kelibsiz.\n\n"
        "Kerakli bo'limni tanlang:",
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # Kelgan har qanday xabar egasini ham ro'yxatga qo'shib ketamiz
    users_set.add(message.chat.id)
    text = message.text

    if text == "🌤 Ob-havo":
        weather_text = (
            "🌤 **Nukus shahri bo'yicha ob-havo:**\n\n"
            "• Harorat: +18°C\n"
            "• Holat: Ochiq, quyoshli\n"
            "• Shamol: 5 m/s, shimoli-g'arbiy\n"
            "• Namlik: 45%"
        )
        bot.send_message(message.chat.id, weather_text, parse_mode="Markdown")

    elif text == "⛽️ Yoqilg'i narxlari":
        fuel_text = (
            "⛽️ **Nukus bo'yicha yoqilg'i narxlari (tahminiy):**\n\n"
            "• AI-92 benzin: 9 500 - 10 000 so'm\n"
            "• AI-80 benzin: 7 500 - 8 000 so'm\n"
            "• Metan gaz: 3 800 so'm / m³\n"
            "• Propan gaz: 5 200 so'm / litr"
        )
        bot.send_message(message.chat.id, fuel_text, parse_mode="Markdown")

    elif text == "📍 Navigatsiya / Joylashuv":
        nav_text = (
            "📍 **Nukus Avto Xizmatlar Navigatsiyasi:**\n\n"
            "1. Eng yaqin zapravkalar va servis markazlarini xaritadan topishingiz mumkin.\n"
            "2. Nukus markazi: 42.4619° N, 59.6166° E\n\n"
            "Mo'ljal: Nukus avtovokzal / Markaziy bozor."
        )
        bot.send_message(message.chat.id, nav_text, parse_mode="Markdown")

    elif text == "👥 Botdagi odamlar soni":
        total_users = len(users_set)
        bot.send_message(
            message.chat.id,
            f"👥 **Botimizga a'zo bo'lgan jami foydalanuvchilar soni:** {total_users} ta",
            parse_mode="Markdown"
        )

    elif text == "ℹ️ Yordam":
        help_text = (
            "🤖 **Nukus Avto Bot yordamchisi**\n\n"
            "Ushbu bot orqali Nukus shahridagi avtomobil egalari uchun kerakli bo'lgan ob-havo, yoqilg'i narxlari va navigatsiya ma'lumotlarini olishingiz mumkin."
        )
        bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

    else:
        bot.send_message(
            message.chat.id, 
            "Iltimos, pastdagi menyu tugmalaridan birini tanlang.",
            reply_markup=main_keyboard()
        )

if __name__ == '__main__':
    bot.infinity_polling()
