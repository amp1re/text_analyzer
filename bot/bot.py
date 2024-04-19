import os

import requests
from bot_handlers import (balance_conv_handler, classify_conv_handler,
                          login_conv_handler, registration_conv_handler, start)
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

load_dotenv()

TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")

# Определение состояний
USERNAME, EMAIL, PASSWORD, TEXT, AMOUNT = range(5)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(registration_conv_handler)
    dp.add_handler(login_conv_handler)
    dp.add_handler(balance_conv_handler)
    dp.add_handler(classify_conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
