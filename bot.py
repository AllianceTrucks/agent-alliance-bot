from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Передать заявку", callback_data='submit')],
        [InlineKeyboardButton("Обучение", callback_data='learn')],
        [InlineKeyboardButton("Доход", callback_data='income')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в бота 'Агент Альянса'! Выберите раздел:",
        reply_markup=reply_markup
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'submit':
        await query.edit_message_text("📨 Здесь вы можете передать заявку. (Форма пока не подключена)")
    elif query.data == 'learn':
        await query.edit_message_text("📚 Добро пожаловать в раздел обучения!")
    elif query.data == 'income':
        await query.edit_message_text("💰 Здесь будет отображаться ваш доход.")
    else:
        await query.edit_message_text("🤖 Неизвестная команда.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
