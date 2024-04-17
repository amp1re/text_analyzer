import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

load_dotenv()

TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")  # URL вашего API

# Определение состояний
USERNAME, EMAIL, PASSWORD = range(3)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /register to sign up or /login to log in.")


def start_registration(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter your username:")
    return USERNAME


def username(update: Update, context: CallbackContext):
    context.user_data["username"] = update.message.text
    update.message.reply_text("Please enter your email:")
    return EMAIL


def email(update: Update, context: CallbackContext):
    context.user_data["email"] = update.message.text
    update.message.reply_text("Please enter your password:")
    return PASSWORD


def password(update: Update, context: CallbackContext):
    context.user_data["password"] = update.message.text
    response = requests.put(f"{BASE_URL}/signup", json=context.user_data)
    if response.status_code == 200:
        update.message.reply_text("Registration successful!")
    else:
        update.message.reply_text(
            "Registration failed: " + response.json().get("detail", "Unknown error")
        )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


def start_login(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter your email for login:")
    return EMAIL


def email_login(update: Update, context: CallbackContext):
    context.user_data["email"] = update.message.text
    update.message.reply_text("Please enter your password:")
    return PASSWORD


def password_login(update: Update, context: CallbackContext):
    context.user_data["password"] = update.message.text
    response = requests.post(
        f"{BASE_URL}/signin",
        json={
            "email": context.user_data["email"],
            "password": context.user_data["password"],
        },
    )
    if response.status_code == 200:
        context.user_data["token"] = response.json()["access_token"]
        update.message.reply_text("Login successful!")
    else:
        update.message.reply_text(
            "Login failed: " + response.json().get("detail", "Unknown error")
        )
    return ConversationHandler.END


def balance(update: Update, context: CallbackContext):
    if "token" in context.user_data:
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
    registration_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("register", start_registration)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, username)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    login_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("login", start_login)],
        states={
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, email_login)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password_login)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(registration_conv_handler)
    dp.add_handler(login_conv_handler)
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("classify", classify_text))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
