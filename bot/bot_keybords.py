from telegram import ReplyKeyboardMarkup


class BotKeyboards:
    @staticmethod
    def main_menu():
        keyboard = [["Register", "Login"], ["Help"]]
        return ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        )

    @staticmethod
    def post_login_menu():
        keyboard = [["Classify text", "Update balance"]]
        return ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        )

    @staticmethod
    def cancel():
        keyboard = [["Cancel"]]
        return ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        )
