from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pytz import timezone  # Импортируем библиотеку для работы с часовыми поясами

# Токен вашего бота
TOKEN = "7609804996:AAFIN97lDD5HAc32rg3DgMGWfeVwbYHCz24"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш Telegram-бот.")

# Основная функция
def main():
    # Создаем приложение с использованием токена и явно указываем московский часовой пояс
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()