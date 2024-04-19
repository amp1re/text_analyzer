class BotTexts:
    WELCOME = "Welcome! Use /register to sign up or /login to log in."
    ENTER_USERNAME = "Please enter your username:"
    ENTER_EMAIL = "Please enter your email:"
    ENTER_PASSWORD = "Please enter your password:"
    REGISTRATION_SUCCESS = "Registration successful!"
    REGISTRATION_FAILED = "Registration failed: {}"
    LOGIN_SUCCESS = "Login successful!"
    LOGIN_FAILED = "Login failed: {}"
    ENTER_AMOUNT = "Please enter amount:"
    UPDATE_BALANCE_SUCCESS = "Balance updated."
    UPDATE_BALANCE_FAILED = "Failed to update balance."
    LOGIN_FIRST = "Please log in first."
    OPERATION_CANCELLED = "Operation cancelled."
    TYPE_TEXT_TO_CLASSIFY = "Please, type text to classify:"
    EXECUTE_TASK_FAILED = "Failed to execute task."

    @staticmethod
    def registration_failed(detail):
        return BotTexts.REGISTRATION_FAILED.format(detail)

    @staticmethod
    def login_failed(detail):
        return BotTexts.LOGIN_FAILED.format(detail)
