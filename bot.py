import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler,
                          Updater, filters)

load_dotenv()

TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")  # URL вашего API

# Определение состояний
USERNAME, EMAIL, PASSWORD = range(3)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /register to sign up or /login to log in.")


def register(update: Update, context: CallbackContext):
    # Должно получать данные для регистрации, например, через conversation handler
    response = requests.put(
        f"{BASE_URL}/signup",
        json={"username": "username", "email": "email", "password": "password"},
    )
    if response.status_code == 200:
        update.message.reply_text("Registration successful!")
    else:
        update.message.reply_text("Registration failed.")


def login(update: Update, context: CallbackContext):
    # Должно получать данные для входа
    response = requests.post(
        f"{BASE_URL}/signin", json={"email": "email", "password": "password"}
    )
    if response.status_code == 200:
        context.user_data["token"] = response.json()["access_token"]
        update.message.reply_text("Login successful!")
    else:
        update.message.reply_text("Login failed.")


def balance(update: Update, context: CallbackContext):
    if "token" in context.user_data:
        # Пример пополнения баланса
        headers = {"Authorization": f"Bearer {context.user_data['token']}"}
        response = requests.put(
            f"{BASE_URL}/update_balance", json={"amount": 100}, headers=headers
        )
        if response.status_code == 200:
            update.message.reply_text("Balance updated.")
        else:
            update.message.reply_text("Failed to update balance.")
    else:
        update.message.reply_text("Please log in first.")


def classify_text(update: Update, context: CallbackContext):
    if "token" in context.user_data:
        # Пример классификации текста
        headers = {"Authorization": f"Bearer {context.user_data['token']}"}
        response = requests.get(
            f"{BASE_URL}/execute", json={"text": "example text"}, headers=headers
        )
        if response.status_code == 200:
            update.message.reply_text(str(response.json()))
        else:
            update.message.reply_text("Failed to execute task.")
    else:
        update.message.reply_text("Please log in first.")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("login", login))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("classify", classify_text))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
