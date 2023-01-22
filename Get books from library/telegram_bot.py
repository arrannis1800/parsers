import os
from dotenv import load_dotenv
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler, CallbackContext

from get_in_freebook import parce_books, get_text

load_dotenv(dotenv_path='.env')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Выгрузить нужные книги']]
    keyboard = [[InlineKeyboardButton("Выгрузить нужные книги", callback_data='var_books')]]

    await update.message.reply_text(
        text="Привет, Это бот для выгрузки недостающих книг, чтобы их можно было заказать с сайта Лабиринт",

        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, input_field_placeholder="Нажмите на кнопку"
        # ),


        reply_markup = InlineKeyboardMarkup(keyboard)
    )


async def var_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=query.message.text)
    await query.message.reply_text('Какой минимальный остаток книг в библиотеке?', reply_markup = ReplyKeyboardRemove())

    return 'Choose'


async def parse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Подождите пару секунд')
    parce_books(int(update.message.text))
    texts = get_text()

    for text in texts:
        print(text)
        await update.message.reply_text(texts[text], parse_mode='HTML',)

    keyboard = [[InlineKeyboardButton("Выгрузить нужные книги", callback_data='var_books')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Книги собраны', parse_mode='HTML',reply_markup=reply_markup)


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    reply_keyboard = [['Выгрузить нужные книги']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.add_handler(
        ConversationHandler(entry_points=[MessageHandler(filters.Regex("Выгрузить нужные книги"), var_books),CallbackQueryHandler(var_books)],
                            states={
                                'Choose': [
                                    MessageHandler(filters.Regex(r'^\d+$'), parse),
                                    MessageHandler(filters.Regex("Выгрузить нужные книги"), var_books),
                                    CallbackQueryHandler(var_books, pattern='var_books')
                                ]},
                            fallbacks=[CommandHandler("start", start)]))

    application.run_polling()
