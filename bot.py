import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import os

# Set your Telegram Bot token here
TOKEN = os.environ['TOKEN']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# States for the conversation handler (optional, if you want a multi-step conversation)
STATE_1, STATE_2 = range(2)

# Command to start the bot (optional)
def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(f"Hello, {user.first_name}! Welcome to your bot.")
    return STATE_1  # If you don't need a multi-step conversation, you can remove this line

# Command to show the custom keyboard
def show_keyboard(update: Update, context: CallbackContext):
    custom_keyboard = [
        ['Button 1', 'Button 2'],
        ['Button 3', 'Button 4'],
        ['Button 5'],
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Here's your custom keyboard:", reply_markup=reply_markup)

# Command to hide the custom keyboard
def hide_keyboard(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text("Keyboard hidden.", reply_markup=reply_markup)

# Command to handle when user clicks on a button in the custom keyboard
def button_click(update: Update, context: CallbackContext):
    button_text = update.message.text
    update.message.reply_text(f"You clicked on '{button_text}'.")

# Command to handle unknown commands or text (optional)
def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry, I don't understand that command.")

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))  # Optional command to start the bot
    dp.add_handler(CommandHandler("show_keyboard", show_keyboard))
    dp.add_handler(CommandHandler("hide_keyboard", hide_keyboard))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, button_click))
    dp.add_handler(MessageHandler(Filters.command, unknown_command))  # Optional unknown command handler

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C
    updater.idle()

if __name__ == "__main__":
    main()
