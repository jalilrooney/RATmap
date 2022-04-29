import traceback
import logging
from telegram import Update, ForceReply, Chat, ChatMember, ParseMode, ChatMemberUpdated
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ChatMemberHandler
from token_functions import convert_balance_to_usd, get_price
from chat_functions import track_chats, greet_chat_members
from locator import locate_fraction
from holders_functions import get_RAT_balance, add_address, change_address, get_balance


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def check_message_source(update):
    return update["message"]['chat']['username'] in ('TelethonAccounts', 'RATbits', 'jalil_bm', 'RatGermany', 'raredubai', 'DubaiRAT')
    # return True


def start(update: Update, context: CallbackContext) -> None:
    sender = update.message.from_user
    if sender['is_bot']:
        return
    text = """
        This bot is developed by @RATbits to help members using the following commands:
        
        /balance - Get your RAT balance in both RAT and USD
        /ratmap - Locate your NFT fraction on a selected Art. i.e: /ratmap I_Fought_The_Law-1
        /ratusd - Get the USD value of a RAT amount. i.e: /ratusd 1000000 (/ratusd same as /ratusd 1)
        /add_address - Add your wallet address to my DataBase
        /change_address - Change your saved wallet address
    """
    update.message.reply_text(text, parse_mode=ParseMode.HTML)


def help_command(update: Update, context: CallbackContext) -> None:
    sender = update.message.from_user
    if sender['is_bot']:
        return
    if not check_message_source(update):
        update.message.reply_text('Please message me from https://t.me/RATbits')
        return
    update.message.reply_text('USE: /ratmap FractionName')


def unknown_message(update: Update, context: CallbackContext) -> None:
    CommandHandler("ratmap_help", help_command)


if __name__ == "__main__":
    updater = Updater("5250985047:AAH0dxrf9FIXMZJJPzZtCrRaV1EOHbIXKGc")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("ratmap_help", help_command))
    dispatcher.add_handler(CommandHandler("ratmap", locate_fraction))
    dispatcher.add_handler(CommandHandler("ratusd", convert_balance_to_usd))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("add_address", add_address))
    dispatcher.add_handler(CommandHandler("change_address", change_address))
    dispatcher.add_handler(CommandHandler("balance", get_balance))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown_message))
    dispatcher.add_handler(MessageHandler(Filters.text, unknown_message))
    dispatcher.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    dispatcher.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.start_polling()

# https://console.cloud.google.com/compute/instances?project=telegrambot-342723
# https://programmingforgood.medium.com/deploy-telegram-bot-on-google-cloud-platform-74f1f531f65e
# */1 * * * * cd /home/benharkatdjalil/RATmap; nohup python3 /home/benharkatdjalil/RATmap/fraction_locatore_local.py </dev/null &>/dev/null &
# chat id of djolocatorbo: 1055241434