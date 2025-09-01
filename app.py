import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN, ALLOWED_IDS, DEVELOPERS


bot = telebot.TeleBot(TOKEN)

ALLOWED_IDS = set(ALLOWED_IDS)
DELEVELOPERS = set(DEVELOPERS)

def restrict_access(func):
    def wrapper(message):
        user_id = message.from_user.id
        if user_id in ALLOWED_IDS:
            return func(message)
        else:
            bot.reply_to(message, "Доступ запрещён.")
    return wrapper

@bot.message_handler(commands=['addid'])
def addid(message):
    @DEVELOPERS
    def inner(message):
        user_id = message.from_user.id
        if user_id in DEVELOPERS:
            bot.reply_to(message, "Введіть ID користувача для додавання:")
            bot.register_next_step_handler(message, process_add_id)
        else:
            bot.reply_to(message, "У вас немає прав для виконання цієї команди.")
    return inner(message)
def process_add_id(message):
    user_id = message.text
    if user_id.isdigit():
        user_id = int(user_id)
        if user_id not in ALLOWED_IDS:
            ALLOWED_IDS.append(user_id)
            bot.reply_to(message, "Користувача успішно додано.")
        else:
            bot.reply_to(message, "Користувач вже є в списку.")
    else:
        bot.reply_to(message, "Будь ласка, введіть коректний ID.")

@bot.message_handler(commands=['myid'])
def my_id(message):
    bot.reply_to(message, f"Ваш ID: {message.from_user.id}")

@bot.message_handler(commands=['start'])
@restrict_access
def send_gdz(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("📘 ГДЗ 7 класу"),
        KeyboardButton("📗 ГДЗ контрольні роботи 7 класу"),
        KeyboardButton("📘 ГДЗ 8 класу"),
        KeyboardButton("📗 ГДЗ контрольні роботи 8 класу")
    )
    bot.reply_to(message, "Оберіть категорію ГДЗ:", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "📘 ГДЗ 7 класу")
@restrict_access
def gdz7_text(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Алгебра", url="https://gdzister.net/alhebra"),
        InlineKeyboardButton("Геометрія", url="https://gdzister.net/heometriia"),
        InlineKeyboardButton("Українська мова", url="https://4book.org/uchebniki-ukraina/7-klas/pidruchnik-ukrayinska-mova-7-klas-zabolotniy-2024"),
        InlineKeyboardButton("Фізика", url="https://gdzonline.net/473-fizika-7-klas-baryahtar.html"),
        InlineKeyboardButton("Хімія", url="https://gdzonline.net/635-himiya-7-klas-grygorovych.html"),
        InlineKeyboardButton("Англійська мова", url="https://gdzonline.net/886-english-7-klas-kosta.html"),
        InlineKeyboardButton("Зошит з англійської", url="https://gdzonline.net/891-7-klas-kosta-workbook.html"),
        InlineKeyboardButton("Зошит з географії", url="https://4book.org/gdz-reshebniki-ukraina/7-klas/gdz-zoshit-geografiya-7-klas-gilberg-2024"),
    )
    bot.reply_to(message, "📘 ГДЗ 7 класу:", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "📗 ГДЗ контрольні роботи 7 класу")
@restrict_access
def gdzkr7_text(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("Алгебра"),
        KeyboardButton("Геометрія"),
        KeyboardButton("Біологія"),
        KeyboardButton("Українська мова"),
        KeyboardButton("⬅ Назад")
    )
    bot.reply_to(message, "📗 ГДЗ контрольні роботи 7 класу", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "📘 ГДЗ 8 класу")
@restrict_access
def gdz8(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Алгебра", url="https://www.gdzister.in.ua/alhebra"),
        InlineKeyboardButton("Геометрія", url="https://www.gdzister.in.ua/heometriia"),
        InlineKeyboardButton("Українська мова", url="https://shkola.in.ua/2414-hdz-ukrainska-mova-8-klas-zabolotnyi-2016.html"),
        InlineKeyboardButton("Фізика", url="https://shkola.in.ua/2415-hdz-fizyka-8-klas-bar-iakhtar-2016.html"),
        InlineKeyboardButton("Англійська мова", url="https://shkola.in.ua/3251-hdz-anhliiska-mova-8-klas-stairih.html"),
        InlineKeyboardButton("Зошит з англійської", url="https://gdzonline.net/902-english-8-jones-workbook.html"),
        InlineKeyboardButton("Зошит з географії", url="https://shkola.in.ua/3350-hdz-heohrafiia-8-klas-hilberh-2025-robochyi-zoshyt.html"),
        InlineKeyboardButton("Хімія", url="https://shkola.in.ua/2417-hdz-khimiia-8-klas-hryhorovych-2016.html"),
    )
    bot.reply_to(message, "📘 ГДЗ 8 класу:", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "📗 ГДЗ контрольні роботи 8 класу")
@restrict_access
def gdzkr8(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Алгебра", url="https://www.gdzister.in.ua/s-ta-dr-z-alhebry"),
        InlineKeyboardButton("Геометрія", url="https://www.gdzister.in.ua/s-ta-dr-z-heometriji"),
    )
    bot.reply_to(message, "📗 ГДЗ контрольні роботи 8 класу:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["Алгебра", "Геометрія", "Біологія", "Українська мова"])
@restrict_access
def choose_category(message):
    subject = message.text
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton(f"{subject} — Самостійні"),
        KeyboardButton(f"{subject} — Контрольні"),
        KeyboardButton("⬅ Назад")
    )
    bot.reply_to(message, f"Оберіть категорію для {subject}:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: "Самостійні" in message.text)
@restrict_access
def show_self_work(message):
    subject = message.text.split(" — ")[0]
    keyboard = InlineKeyboardMarkup(row_width=1)

    if subject == "Алгебра":
        keyboard.add(
            InlineKeyboardButton("С-1 [1М]. Узагальнення та систематизація знань", url="https://gdzister.net/s-ta-dr-z-alhebry/s-1-1m"),
            InlineKeyboardButton("С-2 [2М]. Лінійні рівняння з однією змінною", url="https://gdzister.net/s-ta-dr-z-alhebry/s-2-2m"),
            InlineKeyboardButton("С-3 [5М]. Вирази зі змінними", url="https://gdzister.net/s-ta-dr-z-alhebry/s-3-5m"),
            InlineKeyboardButton("С-4 [6М]. Одночлен", url="https://gdzister.net/s-ta-dr-z-alhebry/s-4-6m"),
            InlineKeyboardButton("С-5 [9М]. Многочлен", url="https://gdzister.net/s-ta-dr-z-alhebry/s-5-9m"),
            InlineKeyboardButton("С-6 [10М]. Множення многочлена", url="https://gdzister.net/s-ta-dr-z-alhebry/s-6-10m"),
            InlineKeyboardButton("С-7 [13М]. Квадрат суми і квадрат різниці", url="https://gdzister.net/s-ta-dr-z-alhebry/s-7-13m"),
            InlineKeyboardButton("С-8 [14М]. Розкладання на множники різниці квадратів", url="https://gdzister.net/s-ta-dr-z-alhebry/s-8-14m"),
            InlineKeyboardButton("С-9 [17М]. Функції", url="https://gdzister.net/s-ta-dr-z-alhebry/s-9-17m"),
            InlineKeyboardButton("С-10 [20М]. Лінійне рівняння з двома змінними", url="https://gdzister.net/s-ta-dr-z-alhebry/s-10-20m"),
            InlineKeyboardButton("С-11 [21М]. Розв'язування систем лінійних рівнянь", url="https://gdzister.net/s-ta-dr-z-alhebry/s-11-21m"),
        )   

    elif subject == "Геометрія":
        keyboard.add(
            InlineKeyboardButton("С-1 [3М]. Елементарні геометричні фігури", url="https://gdzister.net/s-ta-dr-z-heometriji/s-1-3m"),
            InlineKeyboardButton("С-2 [4М]. Суміжні та вертикальні кути", url="https://gdzister.net/s-ta-dr-z-heometriji/s-2-4m"),
            InlineKeyboardButton("С-4 [8М]. Ознаки та властивості паралельних прямих", url="https://gdzister.net/s-ta-dr-z-heometriji/s-4-8m"),
            InlineKeyboardButton("С-5 [11М]. Трикутник та його елементи", url="https://gdzister.net/s-ta-dr-z-heometriji/s-5-11m"),
            InlineKeyboardButton("С-6 [12М]. Рівнобедрений трикутник", url="https://gdzister.net/s-ta-dr-z-heometriji/s-6-12m"),
            InlineKeyboardButton("С-7 [15М]. Сума кутів трикутника", url="https://gdzister.net/s-ta-dr-z-heometriji/s-7-15m"),
            InlineKeyboardButton("С-8 [16М]. Прямокутні трикутники", url="https://gdzister.net/s-ta-dr-z-heometriji/s-8-16m"),
            InlineKeyboardButton("С-9 [18М]. Коло. Круг", url="https://gdzister.net/s-ta-dr-z-heometriji/s-9-18m"),
            InlineKeyboardButton("С-10 [19М]. Коло, описане навколо трикутника", url="https://gdzister.net/s-ta-dr-z-heometriji/s-10-19m"),
        )

    else:
        bot.send_message(message.chat.id, f"Для {subject} немає самостійних робіт.")
        return

    bot.send_message(message.chat.id, f"{subject} — Самостійні:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: "Контрольні" in message.text)
@restrict_access
def show_control_work(message):
    subject = message.text.split(" — ")[0]
    keyboard = InlineKeyboardMarkup(row_width=1)

    if subject == "Алгебра":
        keyboard.add(
            InlineKeyboardButton("ДР-1 [1М]. Лінійні рівняння", url="https://gdzister.net/s-ta-dr-z-alhebry/dr-1-1m"),
            InlineKeyboardButton("ДР-2 [3М]. Вирази зі змінними", url="https://gdzister.net/s-ta-dr-z-alhebry/dr-2-3m"),    
            InlineKeyboardButton("ДР-3 [5М]. Многочлен", url="https://gdzister.net/s-ta-dr-z-alhebry/dr-3-5m/dr-3-var1"),
            InlineKeyboardButton("ДР-4 [7М]. Формули скороченого множення. Розкладання многочленів на множники за допомогою формул скороченого множення", url="https://gdzister.net/s-ta-dr-z-alhebry/dr-4-7m"),
            InlineKeyboardButton("ДР-5 [9М]. Функції", url="https://gdzister.net/s-ta-dr-z-alhebry/dr-5-9m"),
            InlineKeyboardButton("ДР-6 [11М]. Система лінійне рівняння з двома змінними", url="https://gdzister.net/s-ta-dr-z-alhebry/dr-6-11m"),
            InlineKeyboardButton("Контрольна робота за Ⅰ семестр", url="https://gdzister.net/s-ta-dr-z-alhebry/kr-1"),
            InlineKeyboardButton("Контрольна робота за Ⅱ семестр", url="https://gdzister.net/s-ta-dr-z-alhebry/kr-2"),
            InlineKeyboardButton("Річна контрольна робота за 7 клас", url="https://gdzister.net/s-ta-dr-z-alhebry/rkr-za-7-klas"),
        )

    elif subject == "Геометрія":
        keyboard.add(
            InlineKeyboardButton("ДР-1 [2М]. Елементарні геометричні фігури", url="https://gdzister.net/s-ta-dr-z-heometriji/dr-1-2m"),
            InlineKeyboardButton("ДР-2 [4М]. Паралельні та перпендикулярні прямі", url="https://gdzister.net/s-ta-dr-z-heometriji/dr-2-4m"),
            InlineKeyboardButton("ДР-3 [6М]. Паралельні та перпендикулярні прямі 2", url="https://gdzister.net/s-ta-dr-z-heometriji/dr-3-6m"),
            InlineKeyboardButton("ДР-4 [8М]. Трикутник та його елементи", url="https://gdzister.net/s-ta-dr-z-heometriji/dr-4-8m"),
            InlineKeyboardButton("Контрольна робота за Ⅰ семестр", url="https://gdzister.net/s-ta-dr-z-heometriji/kr-1"),
            InlineKeyboardButton("Контрольна робота за Ⅱ семестр", url="https://gdzister.net/s-ta-dr-z-heometriji/kr-2"),
            InlineKeyboardButton("Річна контрольна робота за 7 клас", url="https://gdzister.net/s-ta-dr-z-heometriji/rkr-za-7-klas"),
            InlineKeyboardButton("Річна контрольна робота з математики", url="https://gdzister.net/s-ta-dr-z-heometriji/rkr-za-7-klas-z-matematyky"),
        )

    elif subject == "Біологія":
        keyboard.add(
            InlineKeyboardButton("Вступ, клітина, прокаріоти", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/page,2,608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
            InlineKeyboardButton("Одноклітинні евкаріоти, водорості", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/page,3,608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
            InlineKeyboardButton("Характерні риси та будова вищих рослин", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/page,4,608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
            InlineKeyboardButton("Різноманітність вищих рослин", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/page,5,608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
            InlineKeyboardButton("Характерні риси та будова тварин", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/page,6,608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
            InlineKeyboardButton("Різноманітність тварин (Безхребетні)", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/page,7,608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
            InlineKeyboardButton("Різноманітність тварин (Хребетні)", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/page,8,608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
            InlineKeyboardButton("Гриби — гетеротрофні організми", url="https://onegdz.com/7-klas/gdz-biologiia-7-klas/page,9,608-gdz-biologiia-pidsumkove-tematychne-ocinuvannia-kozlenko-kulinich-urchenko.html"),
        )

    elif subject == "Українська мова":
        keyboard.add(
            InlineKeyboardButton("Повторення вивченого", url="https://onegdz.com/7-klas/gdz-ukrayinska-mova-7-klas/page,2,605-gdz-zoshyt-dlia-pidsumkovogo-ocinuvannia-navchalnykh-dosiagnen-zabolotnyi-7-klas-ukrainska-mova-vidpovidi.html"),
            InlineKeyboardButton("Сприймання тексту «Веснянки» на слух", url="https://onegdz.com/7-klas/gdz-ukrayinska-mova-7-klas/page,3,605-gdz-zoshyt-dlia-pidsumkovogo-ocinuvannia-navchalnykh-dosiagnen-zabolotnyi-7-klas-ukrainska-mova-vidpovidi.html"),
            InlineKeyboardButton("Дієслово", url="https://onegdz.com/7-klas/gdz-ukrayinska-mova-7-klas/page,4,605-gdz-zoshyt-dlia-pidsumkovogo-ocinuvannia-navchalnykh-dosiagnen-zabolotnyi-7-klas-ukrainska-mova-vidpovidi.html"),
            InlineKeyboardButton("Дієприкметник, дієслівні форми на -но, -то, дієприслівник", url="https://onegdz.com/7-klas/gdz-ukrayinska-mova-7-klas/page,5,605-gdz-zoshyt-dlia-pidsumkovogo-ocinuvannia-navchalnykh-dosiagnen-zabolotnyi-7-klas-ukrainska-mova-vidpovidi.html"),
            InlineKeyboardButton("Сприймання письмового тексту «Ягода, фрукт чи плід?», «Розвіюємо міфи» (читання) ", url="https://onegdz.com/7-klas/gdz-ukrayinska-mova-7-klas/page,6,605-gdz-zoshyt-dlia-pidsumkovogo-ocinuvannia-navchalnykh-dosiagnen-zabolotnyi-7-klas-ukrainska-mova-vidpovidi.html"),
            InlineKeyboardButton("Прислівник", url="https://onegdz.com/7-klas/gdz-ukrayinska-mova-7-klas/page,7,605-gdz-zoshyt-dlia-pidsumkovogo-ocinuvannia-navchalnykh-dosiagnen-zabolotnyi-7-klas-ukrainska-mova-vidpovidi.html"),
            InlineKeyboardButton("Службові частини мови, вигук", url="https://onegdz.com/7-klas/gdz-ukrayinska-mova-7-klas/page,8,605-gdz-zoshyt-dlia-pidsumkovogo-ocinuvannia-navchalnykh-dosiagnen-zabolotnyi-7-klas-ukrainska-mova-vidpovidi.html"),
        )

    bot.send_message(message.chat.id, f"{subject} — Контрольні:", reply_markup=keyboard)


@restrict_access
@bot.message_handler(func=lambda message: message.text == "⬅ Назад")
def go_back(message):
    send_gdz(message)

bot.polling(non_stop=True)
