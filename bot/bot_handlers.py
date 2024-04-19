import os

import requests
from bot_keybords import BotKeyboards
from bot_texts import BotTexts
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler)

load_dotenv()

TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")

USERNAME, EMAIL, PASSWORD, TEXT, AMOUNT = range(5)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(BotTexts.WELCOME, reply_markup=BotKeyboards.main_menu())


def start_registration(update: Update, context: CallbackContext):
    update.message.reply_text(BotTexts.ENTER_USERNAME)
    return USERNAME


def username(update: Update, context: CallbackContext):
    context.user_data["username"] = update.message.text
    update.message.reply_text(BotTexts.ENTER_EMAIL)
    return EMAIL


def email(update: Update, context: CallbackContext):
    context.user_data["email"] = update.message.text
    update.message.reply_text(BotTexts.ENTER_PASSWORD)
    return PASSWORD


def password(update: Update, context: CallbackContext):
    context.user_data["password"] = update.message.text
    response = requests.put(f"{BASE_URL}/signup", json=context.user_data)
    if response.status_code == 200:
        update.message.reply_text(
            BotTexts.REGISTRATION_SUCCESS, reply_markup=BotKeyboards.main_menu()
        )
    else:
        update.message.reply_text(
            BotTexts.registration_failed(
                response.json().get("detail", "Unknown error")
            ),
            reply_markup=BotKeyboards.main_menu(),
        )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        BotTexts.OPERATION_CANCELLED, reply_markup=BotKeyboards.main_menu()
    )
    return ConversationHandler.END


def start_login(update: Update, context: CallbackContext):
    update.message.reply_text(BotTexts.ENTER_EMAIL)
    return EMAIL


def email_login(update: Update, context: CallbackContext):
    context.user_data["email"] = update.message.text
    update.message.reply_text(BotTexts.ENTER_PASSWORD)
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
        update.message.reply_text(
            BotTexts.LOGIN_SUCCESS, reply_markup=BotKeyboards.post_login_menu()
        )
    else:
        update.message.reply_text(
            BotTexts.login_failed(response.json().get("detail", "Unknown error")),
            reply_markup=BotKeyboards.main_menu(),
        )
    return ConversationHandler.END


def start_balance(update: Update, context: CallbackContext):
    update.message.reply_text(BotTexts.ENTER_AMOUNT)
    return AMOUNT


def balance(update: Update, context: CallbackContext):
    context.user_data["amount"] = update.message.text
    if "token" in context.user_data:
        headers = {"Authorization": f"Bearer {context.user_data['token']}"}
        response = requests.put(
            f"{BASE_URL}/update_balance",
            json={"amount": context.user_data["amount"]},
            headers=headers,
        )
        if response.status_code == 200:
            update.message.reply_text(
                BotTexts.UPDATE_BALANCE_SUCCESS,
                reply_markup=BotKeyboards.post_login_menu(),
            )
        else:
            update.message.reply_text(
                BotTexts.UPDATE_BALANCE_FAILED,
                reply_markup=BotKeyboards.post_login_menu(),
            )
    else:
        update.message.reply_text(
            BotTexts.LOGIN_FIRST, reply_markup=BotKeyboards.main_menu()
        )
    return ConversationHandler.END


def start_classify(update: Update, context: CallbackContext):
    update.message.reply_text(BotTexts.TYPE_TEXT_TO_CLASSIFY)
    return TEXT


def classify_text(update: Update, context: CallbackContext):
    context.user_data["text"] = update.message.text
    if "token" in context.user_data:
        headers = {"Authorization": f"Bearer {context.user_data['token']}"}
        response = requests.get(
            f"{BASE_URL}/execute",
            json={"text": context.user_data["text"]},
            headers=headers,
        )
        if response.status_code == 200:
            update.message.reply_text(
                str(response.json()), reply_markup=BotKeyboards.post_login_menu()
            )
        else:
            update.message.reply_text(
                BotTexts.EXECUTE_TASK_FAILED,
                reply_markup=BotKeyboards.post_login_menu(),
            )
    else:
        update.message.reply_text(
            BotTexts.LOGIN_FIRST, reply_markup=BotKeyboards.main_menu()
        )


registration_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("register", start_registration),
        MessageHandler(Filters.regex("^Register$"), start_registration),
    ],
    states={
        USERNAME: [MessageHandler(Filters.text & ~Filters.command, username)],
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
        PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

login_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("login", start_login),
        MessageHandler(Filters.regex("^Login$"), start_login),
    ],
    states={
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, email_login)],
        PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password_login)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

balance_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("balance", start_balance),
        MessageHandler(Filters.regex("^Update balance$"), start_balance),
    ],
    states={AMOUNT: [MessageHandler(Filters.text & ~Filters.command, balance)]},
    fallbacks=[CommandHandler("cancel", cancel)],
)

classify_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("classify", start_classify),
        MessageHandler(Filters.regex("^Classify text$"), start_classify),
    ],
    states={TEXT: [MessageHandler(Filters.text & ~Filters.command, classify_text)]},
    fallbacks=[CommandHandler("cancel", cancel)],
)
