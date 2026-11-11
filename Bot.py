import telebot
from telebot import types
math = __import__('math')

TOKEN = '9286457644:AAHJFMLrhOEx5Hz2tTkHK6YVAfriLozhWfI'
bot = telebot.TeleBot(TOKEN)

# Foydalanuvchilar sonini saqlash uchun
users_set = set()

# Asosiy menyu
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_weather = types.KeyboardButton("🌤 Ob-havo")
    btn_fuel = types.KeyboardButton("⛽️ Yoqilg'i narxlari")
    
    # Geolokatsiya so'raydigan tugma
    btn_nav = types.KeyboardButton("📍 Joylashuvni yuborish", request_location=True)
    
    btn_evacuator = types.KeyboardButton("🚗 Evakuator xizmati")
    btn_stats = types.KeyboardButton("👥 Botdagi odamlar soni")
    btn_help = types.KeyboardButton("ℹ️ Yordam")
    
    markup.add(btn_weather, btn_fuel, btn_nav, btn_evacuator, btn_stats, btn_help)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    users_set.add(message.chat.id)
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! Nukus Avto Botiga xush kelibsiz.\n\n"
        "Quyidagi tugmalardan birini tanlang yoki **📍 Joylashuvni yuborish** tugmasini bosib lokatsiyangizni yuboring:",
        reply_markup=main_keyboard()
    )

# Foydalanuvchi lokatsiya yuborganda ishlaydigan qism
@bot.message_handler(content_types=['location'])
def handle_location(message):
    users_set.add(message.chat.id)
    user_lat = message.location.latitude
    user_lon = message.location.longitude
    
    # Nukus shahridagi mashhur zapravka koordinatalari (misol uchun)
    # O'zingizga kerakli nuqtalarni kiritishingiz mumkin
    stations = [
        {"name": "Nukus Oktan (Benzin/Metan)", "lat": 42.4700, "lon": 59.6200},
        {"name": "Inter Gaz (Propan)", "lat": 42.4500, "lon": 59.6100},
        {"name": "Central Zapravka AI-92", "lat": 42.4600, "lon": 59.6300}
    ]
    
    # Eng yaqin zapravkani oddiy formula yordamida topamiz
    closest = min(stations, key=lambda s: math.sqrt((s['lat'] - user_lat)**2 + (s['lon'] - user_lon)**2))
    
    response_text = (
        "📍 **Sizning lokatsiyangiz qabul qilindi!**\n\n"
        f"🔍 Sizga eng yaqin tavsiya etilgan shoxobcha:\n"
        f"🏷 **{closest['name']}**\n\n"
        "Yo'nalish bo'yicha ehtiyot bo'lib harakatlaning!"
    )
    bot.send_message(message.chat.id, response_text, parse_mode="Markdown")
    
    # Xaritada to'g'ridan-to'g'ri lokatsiyani tashlab beramiz
    bot.send_location(message.chat.id, latitude=closest['lat'], longitude=closest['lon'])

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
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
            "⛽️ **Nukus bo'yicha yoqilg'i narxlari:**\n\n"
            "• AI-92 benzin: 9 500 - 10 000 so'm\n"
            "• AI-80 benzin: 7 500 - 8 000 so'm\n"
            "• Metan gaz: 3 800 so'm / m³\n"
            "• Propan gaz: 5 200 so'm / litr"
        )
        bot.send_message(message.chat.id, fuel_text, parse_mode="Markdown")

    elif text == "🚗 Evakuator xizmati":
        evac_text = (
            "🚗 **Nukus Shahri Avto Evakuator Xizmatlari:**\n\n"
            "Agar yo'lda qolib ketsangiz yoki mashinangiz buzilsa, malakali evakuator xizmatiga murojaat qiling:\n\n"
            "📞 Aloqa uchun raqamlar:\n"
            "• +998 93 123-45-67 (24/7)\n"
            "• +998 90 987-65-43\n\n"
            "Manzilni aniqlash uchun **📍 Joylashuvni yuborish** tugmasini bosing."
        )
        bot.send_message(message.chat.id, evac_text, parse_mode="Markdown")

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
            "Ushbu bot orqali ob-havo, yoqilg'i narxlari, evakuator xizmatlari va eng asosiysi **lokatsiyangizga yaqin bo'lgan shoxobchalarni** topishingiz mumkin."
        )
        bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

    else:
        bot.send_message(
            message.chat.id, 
            "Iltimos, pastdagi menyu tugmalaridan foydalaning yoki lokatsiyangizni yuboring.",
            reply_markup=main_keyboard()
        )

if __name__ == '__main__':
    bot.infinity_polling()
