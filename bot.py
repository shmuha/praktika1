from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
import logging
import asyncio

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота и настройки
TOKEN = "7609804996:AAFIN97lDD5HAc32rg3DgMGWfeVwbYHCz24"  # Замените на токен вашего бота
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"  # Замените на URL вашего Prometheus
QUERY = 'up{job="example_service"}'  # Замените на ваш запрос к Prometheus
CHAT_ID = "938521809"  # Замените на ID вашего чата в Telegram

# Проверка состояния сервисов
def check_service_status():
    try:
        response = requests.get(PROMETHEUS_URL, params={"query": QUERY})
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data["data"]["result"]
    except Exception as e:
        logger.error(f"Ошибка при запросе к Prometheus: {e}")
        return []

# Проверка, есть ли сбои
def is_service_down(data):
    for result in data:
        if result["value"][1] == "0":  # Если сервис недоступен
            return True
    return False

# Отправка уведомлений
async def send_alert(context: ContextTypes.DEFAULT_TYPE):
    try:
        data = check_service_status()
        if is_service_down(data):
            await context.bot.send_message(chat_id=CHAT_ID, text="⚠️ Сервис недоступен!")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления: {e}")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для мониторинга сервисов.")

# Команда /status
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = check_service_status()
    if is_service_down(data):
        await update.message.reply_text("⚠️ Сервис недоступен!")
    else:
        await update.message.reply_text("✅ Все сервисы работают нормально.")

# Основная функция
async def main():
    # Создаем приложение для бота
    application = ApplicationBuilder().token(TOKEN).build()

    # Планировщик для периодической проверки
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_alert, "interval", minutes=5, args=[application])  # Проверка каждые 5 минут

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status_command))

    # Инициализация приложения
    await application.initialize()

    # Запуск планировщика
    scheduler.start()

    # Запуск бота
    await application.updater.start_polling()
    await application.start()

    # Удерживаем выполнение основной функции
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())//ц
    except (KeyboardInterrupt, SystemExit):
        logger.info("Приложение остановлено.")
