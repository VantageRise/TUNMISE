from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHANNEL_ID = "@your_channel"  # Replace with your channel username
GROUP_ID = "@your_group"      # Replace with your group username
TWITTER_URL = "https://twitter.com/yourpage"
FACEBOOK_URL = "https://facebook.com/yourpage"

# Database to store user data (consider using a real database for production)
user_data = {}

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")],
        [InlineKeyboardButton("Join Group", url=f"https://t.me/{GROUP_ID[1:]}")],
        [InlineKeyboardButton("Follow Twitter", url=TWITTER_URL)],
        [InlineKeyboardButton("Follow Facebook", url=FACEBOOK_URL)],
        [InlineKeyboardButton("Verify Subscriptions", callback_data="verify")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        f"Hello {user.first_name}! To participate in our airdrop:\n\n"
        "1. Join our Telegram channel\n"
        "2. Join our Telegram group\n"
        "3. Follow our Twitter page\n"
        "4. Follow our Facebook page\n"
        "5. Click 'Verify Subscriptions' when done\n\n"
        "After verification, you'll be asked to provide your Solana address.",
        reply_markup=reply_markup
    )

def verify_subscriptions(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    
    # In a real implementation, you would check if user is actually subscribed
    # This requires additional API calls or bot being admin in the channel/group
    
    # For demo purposes, we'll assume verification is successful
    user_data[user_id] = {"verified": True}
    
    query.answer()
    query.edit_message_text(
        "✅ Verification complete!\n\n"
        "Please send your Solana wallet address now."
    )

def handle_sol_address(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    sol_address = update.message.text
    
    # Basic Solana address validation (44 characters)
    if len(sol_address) == 44:
        if user_id in user_data and user_data[user_id].get("verified"):
            user_data[user_id]["sol_address"] = sol_address
            update.message.reply_text(
                "🎉 Thank you for participating!\n\n"
                "Your Solana address has been recorded: " + sol_address + "\n\n"
                "Airdrop distribution will happen on [date]."
            )
        else:
            update.message.reply_text("Please complete verification first!")
    else:
        update.message.reply_text("Invalid Solana address. Please try again.")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(verify_subscriptions, pattern="^verify$"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_sol_address))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
