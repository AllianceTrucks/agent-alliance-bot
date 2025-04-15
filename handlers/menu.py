from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Передать клиента", callback_data='submit_lead')],
        [InlineKeyboardButton("Мои сделки", callback_data='my_deals')],
        [InlineKeyboardButton("Академия Альянса", callback_data='academy')],
        [InlineKeyboardButton("Рейтинг героев", callback_data='rating')],
        [InlineKeyboardButton("Помощь", callback_data='ai_help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Главное меню:", reply_markup=reply_markup)

async def menu_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    data = update.callback_query.data
    await update.callback_query.edit_message_text(f"Вы нажали: {data}")

async def route_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, используйте кнопки меню.")