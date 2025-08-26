import telebot

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN

bot = telebot.TeleBot(TOKEN)

ALLOWED_IDS = []
ALLOWED_USERNAMES = []

def restrict_access(func):
    def wrapper(message):
        user_id = message.from_user.id
        username = message.from_user.username

        if user_id in ALLOWED_IDS or (username and username.lower() in [u.lower() for u in ALLOWED_USERNAMES]):
            return func(message)
        else:
            bot.reply_to(message, "🚫 У вас немає прав.")
    return wrapper

@bot.message_handler(commands=['start'])
@restrict_access
def send_gdz(message):
    bot.reply_to(
        message,
        "Доступні команди:\n" \
        "Для 7 класа \n"
        "/gdz7 - отримати ГДЗ 7 класу (2025)\n"
        "/gdzkr7 - отримати ГДЗ контрольної роботи 7 класу (2025)\n"
        "Для 8 класа \n"
        "/gdz8 - отримати ГДЗ 8 класу (2025)\n"
        "/gdzkr8 - отримати ГДЗ контрольної роботи 8 класу (2025)"
    )

@bot.message_handler(commands=['gdz7'])
@restrict_access
def gdz7(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Алгебра", url="https://gdzister.net/alhebra"),
        InlineKeyboardButton("Геометрія", url="https://gdzister.net/heometriia"),
        InlineKeyboardButton("Українська мова", url="https://4book.org/uchebniki-ukraina/7-klas/pidruchnik-ukrayinska-mova-7-klas-zabolotniy-2024"),
        InlineKeyboardButton("Фізика", url="https://gdzonline.net/473-fizika-7-klas-baryahtar.html"),
        InlineKeyboardButton("Хімія", url="https://gdzonline.net/635-himiya-7-klas-grygorovych.html"),
        InlineKeyboardButton("Англійська мова", url="https://gdzonline.net/886-english-7-klas-kosta.html"),
        InlineKeyboardButton("Зошит з англійської", url="https://gdzonline.net/891-7-klas-kosta-workbook.html"),
        InlineKeyboardButton("Зошит з географії", url="https://4book.org/gdz-reshebniki-ukraina/7-klas/gdz-zoshit-geografiya-7-klas-gilberg-2024")
    )
    bot.reply_to(message, "📘 ГДЗ 7 класу:", reply_markup=keyboard)

@bot.message_handler(commands=['gdzkr7'])
@restrict_access
def gdzkr7(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Алгебра", url="https://gdzister.net/s-ta-dr-z-alhebry"),
        InlineKeyboardButton("Геометрія", url="https://gdzister.net/s-ta-dr-z-heometriji"),
        InlineKeyboardButton("Біологія", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
        InlineKeyboardButton("Українська мова", url="https://onegdz.com/7-klas/gdz-ukrayinska-mova-7-klas/605-gdz-zoshyt-dlia-pidsumkovogo-ocinuvannia-navchalnykh-dosiagnen-zabolotnyi-7-klas-ukrainska-mova-vidpovidi.html")
    )
    bot.reply_to(message, "📗 ГДЗ контрольні роботи 7 класу:", reply_markup=keyboard)

@bot.message_handler(commands=['gdz8'])
@restrict_access
def gdz8(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Алгебра", url="https://www.gdzister.in.ua/alhebra"),
        InlineKeyboardButton("Геометрія", url="https://www.gdzister.in.ua/heometriia"),
        InlineKeyboardButton("Українська мова", url="https://shkola.in.ua/2414-hdz-ukrainska-mova-8-klas-zabolotnyi-2016.html"),
        InlineKeyboardButton("Фізика", url="https://shkola.in.ua/2415-hdz-fizyka-8-klas-bar-iakhtar-2016.html"),
        InlineKeyboardButton("Англійська мова", url="https://shkola.in.ua/3251-hdz-anhliiska-mova-8-klas-stairih.html"),
        InlineKeyboardButton("Зошит з англійської", url="https://gdzonline.net/902-english-8-jones-workbook.html"),
        InlineKeyboardButton("Зошит з географії", url="https://shkola.in.ua/3350-hdz-heohrafiia-8-klas-hilberh-2025-robochyi-zoshyt.html"),
        InlineKeyboardButton("Хімія", url="https://shkola.in.ua/2417-hdz-khimiia-8-klas-hryhorovych-2016.html")
    )
    bot.reply_to(message, "📘 ГДЗ 8 класу:", reply_markup=keyboard)

@bot.message_handler(commands=['gdzkr8'])
@restrict_access
def gdzkr8(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Алгебра", url="https://www.gdzister.in.ua/s-ta-dr-z-alhebry"),
        InlineKeyboardButton("Геометрія", url="https://www.gdzister.in.ua/s-ta-dr-z-heometriji"),
    )
    bot.reply_to(message, "📗 ГДЗ контрольні роботи 8 класу:", reply_markup=keyboard)

bot.polling(non_stop=True)
