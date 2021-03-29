from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater
from telegram import Bot
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.utils.request import Request
from functools import wraps
from cli import *

API_KEY = '1202626125:AAEKnmc0g8r4hgtSeiG7k7kcwatVwEd5BUw'

button_help = "Help"


# Decorator
def log_error(f):

    @wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Error occurred: {e}')
            raise e

    return inner


def button_help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="help reply text",
        reply_markup=ReplyKeyboardRemove()
    )


@log_error
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == button_help:
        return button_help_handler(update=update, context=context)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_help)
            ],
        ],
        resize_keyboard=True
    )

    if text.lower() == "logo":
        update.message.reply_text(
            text="Logo:" + str(print_logo()),
            reply_markup=reply_markup
        )

    update.message.reply_text(
        text="This is help",
        reply_markup=reply_markup
    )


def main():
    print("Start")

    req = Request(
        connect_timeout=0.5,  # 5 sec by default
        # con_pool_size=8,
    )

    bot = Bot(
        request=req,
        token=API_KEY,
        # base_url=''                 # Proxy URL server
    )

    updater = Updater(
        bot=bot,
        use_context=True
    )

    print(updater.bot.get_me())
    if not updater.bot.get_me():
        print("Cannot get info about bot (provider issue, etc.)")
        exit(1)

    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
