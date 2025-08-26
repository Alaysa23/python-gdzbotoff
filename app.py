import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN

bot = telebot.TeleBot(TOKEN)

registered_users = {}
SECRET_CODE = "orL84OibgD"

@bot.message_handler(commands=['register'])
def register(message):
    try:
        code = message.text.split(" ")[1]
    except IndexError:
        bot.reply_to(message, "❌ Вы не указали код. Используйте: /register <код>")
        return

    if code == SECRET_CODE:
        registered_users[message.from_user.id] = True
        bot.reply_to(message, "✅ Регистрация прошла успешно! Теперь у вас есть доступ к командам.")
    else:
        bot.reply_to(message, "❌ Неверный код! Попробуйте снова.")

def registration_required(func):
    def wrapper(message):
        if registered_users.get(message.from_user.id, False):
            func(message)
        else:
            bot.reply_to(message, "🚫 Вы не зарегистрированы. Используйте /register <код>")
    return wrapper

@bot.message_handler(commands=['start'])
@registration_required
def send_gdz(message):
    bot.reply_to(
        message,
        "Доступные команды:\n"
        "/gdz7 - получить гдз 7 класса по 2025\n"
        "/gdzkr7 - получить гдз контрольной работы 7 класса по 2025"
    )

@bot.message_handler(commands=['gdz7'])
@registration_required
def gdz7(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Алгебра", url="https://gdzister.net/alhebra"),
        InlineKeyboardButton("Геометрия", url="https://gdzister.net/heometriia"),
        InlineKeyboardButton("Украинский язык", url="https://4book.org/uchebniki-ukraina/7-klas/pidruchnik-ukrayinska-mova-7-klas-zabolotniy-2024"),
        InlineKeyboardButton("Физика", url="https://gdzonline.net/473-fizika-7-klas-baryahtar.html"),
        InlineKeyboardButton("Английский язык", url="https://gdzonline.net/886-english-7-klas-kosta.html"),
        InlineKeyboardButton("Зошит Английский язык", url="https://gdzonline.net/891-7-klas-kosta-workbook.html"),
        InlineKeyboardButton("Зошит Географія", url="https://4book.org/gdz-reshebniki-ukraina/7-klas/gdz-zoshit-geografiya-7-klas-gilberg-2024")
    )
    bot.reply_to(message, "📘 ГДЗ 7 класса:", reply_markup=keyboard)

@bot.message_handler(commands=['gdzkr7'])
@registration_required
def gdzkr7(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Алгебра", url="https://gdzister.net/s-ta-dr-z-alhebry"),
        InlineKeyboardButton("Геометрия", url="https://gdzister.net/s-ta-dr-z-heometriji"),
        InlineKeyboardButton("Биология", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
        InlineKeyboardButton("Укр мова", url="https://onegdz.com/7-klas/gdz-ukrayinska-mova-7-klas/605-gdz-zoshyt-dlia-pidsumkovogo-ocinuvannia-navchalnykh-dosiagnen-zabolotnyi-7-klas-ukrainska-mova-vidpovidi.html")
    )
    bot.reply_to(message, "📗 ГДЗ КР 7 класса:", reply_markup=keyboard)

bot.polling(non_stop=True)