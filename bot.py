
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from services.auth import load_auth_data, is_authorized
from handlers import menu, submit_lead, my_deals, academy, rating, ai_help

logging.basicConfig(level=logging.INFO)

ASK_CONTRACT, ASK_PASSWORD = range(2)
auth_data = load_auth_data("auth_data.xlsx")
authorized_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        return await menu.show_main_menu(update, context)
    await update.message.reply_text("Введите номер договора:")
    return ASK_CONTRACT

async def ask_contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contract'] = update.message.text.strip()
    await update.message.reply_text("Введите пароль:")
    return ASK_PASSWORD

async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()
    contract = context.user_data.get('contract')
    user_id = update.effective_user.id

    if is_authorized(auth_data, contract, password):
        authorized_users[user_id] = contract
        await update.message.reply_text("✅ Авторизация прошла успешно!")
        return await menu.show_main_menu(update, context)
    else:
        await update.message.reply_text("❌ Неверный номер договора или пароль. Попробуйте снова: /start")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено. Введите /start для начала.")
    return ConversationHandler.END

def main():
    application = Application.builder().token("7581488062:AAHQ420oYNC5yR9NccJgjR1vvz7kXX2kdrk").build()

    auth_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_CONTRACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contract)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(auth_conv)
    application.add_handler(CallbackQueryHandler(menu.menu_navigation))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu.route_text_input))

    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
