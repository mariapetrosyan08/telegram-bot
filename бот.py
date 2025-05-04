from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters
)

# Состояния
ASK_NAME, ASK_CLASS, ASK_GOAL, ASK_SCHEDULE = range(4)

TOKEN = "8080321382:AAF7o47tEJHWUhcHnmvymzeKLsIe1XWlcHU"  # ← вставь сюда свой токен

OWNER_ID = 1104953636 # ← сюда вставь свой Telegram ID из @userinfobot

# Приветствие и вопрос 1
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Это Мария, твой репетитор по математике ✨😊\n\n"
        "Со мной ты сможешь изучать математику легко, понятно и без стресса 💡\n"
        "Я буду присылать тебе:\n"
        "• Домашние задания ✅\n"
        "• Ссылки на занятия 🔗\n"
        "• Конспекты 📄\n\n"
        "У тебя также будет личный кабинет с баллами и жизнями 💎❤️\n\n"
        "Ответь на несколько вопросов, чтобы мы могли начать! 👇\n\n"
        "Как тебя зовут?"
    )
    return ASK_NAME

# Вопрос 2 — класс
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Отлично! А в каком ты классе?")
    return ASK_CLASS

# Вопрос 3 — цель
async def get_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["class"] = update.message.text
    await update.message.reply_text(
        "Поняла! А какая твоя цель?\n"
        "Повышение успеваемости, ВПР, ОГЭ или что-то другое?"
    )
    return ASK_GOAL

# Вопрос 4 — правила и расписание
async def get_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["goal"] = update.message.text
    name = context.user_data["name"]

    await update.message.reply_text(
    f"Отлично, {name}! Вот правила:\n\n"
    "1. Если ты присутствуешь на занятии и выполняешь домашку — получаешь баллы 💎\n"
    "2. Если ты не выполнишь домашку или пропустишь занятие без предупреждения за несколько часов — теряешь одну жизнь ❤️\n"
    "   У тебя есть 3 жизни на месяц.\n"
    "3. Накопленные баллы можно обменять на бонусы — например, скидку, подарок или день без домашки 🎁💡\n"
    "4. Первый урок — бесплатный 🎁\n"
    "5. Все последующие занятия должны быть оплачены в течение часа после окончания занятия. 💸\n"
    "   Если оплата не поступает — перевожу тебя на предоплату.\n\n"
    "Теперь напиши, когда тебе удобно заниматься.\n"
    "Укажи дни, время и свой город или часовой пояс (если знаешь) ⏰🌍"
)
    return ASK_SCHEDULE

# Финал — обработка расписания
async def get_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["schedule"] = update.message.text
    await update.message.reply_text(
        "Спасибо! Я всё прочитаю и скоро тебе отвечу. До связи!"
    )
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"Новая заявка:\n\n"
             f"Имя: {context.user_data['name']}\n"
             f"Класс: {context.user_data['class']}\n"
             f"Цель: {context.user_data['goal']}\n"
             f"Удобное время: {context.user_data['schedule']}"
    )
    return ConversationHandler.END

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог прерван.")
    return ConversationHandler.END

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        ASK_CLASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_class)],
        ASK_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_goal)],
        ASK_SCHEDULE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_schedule)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

print("Бот запущен!")
app.run_polling()
