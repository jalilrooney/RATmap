from etherscan import Etherscan
import coinaddrvalidator
from telegram import Update, ForceReply, Chat, ChatMember, ParseMode, ChatMemberUpdated
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ChatMemberHandler
from mysql_functions import *
from token_functions import get_price


def get_RAT_balance(wallet_address):
    RAT_balance = eth.get_acc_balance_by_token_and_contract_address(contract_address="0x4eA507bf90b2D206BfF56999dc76E39e447d2587", address=wallet_address)
    return float(int(RAT_balance) / 1000000000)


def add_address(update: Update, context: CallbackContext):
    sender = update.message.from_user
    if int(sender['id']) in get_ronald_chat_ids():
        return update.message.reply_text("You have already added your address, you can change it using the command /change_address")
    holder_address = update.message.text.replace("/add_address", "").strip()
    if not coinaddrvalidator.validate('eth', holder_address).valid:
        return update.message.reply_text("ERROR: Invalid Address!! Use the following pattern:"
                                         "\n/add_address 0x00000...0000")
    else:
        add_holder(holder_address, sender['username'], int(sender['id']))
        update.message.reply_text("Address Added")


def change_address(update: Update, context: CallbackContext):
    sender = update.message.from_user
    if int(sender['id']) not in get_ronald_chat_ids():
        return update.message.reply_text("You didn't add an address, you can add one using the command /add_address")
    holder_address = update.message.text.replace("/change_address", "").strip()
    if not coinaddrvalidator.validate('eth', holder_address).valid:
        update.message.reply_text("ERROR: Invalid Address! Use the following pattern:"
                                  "\n/add_address 0x00000...0000")
        return
    # wallet_address = dispatcher.add_handler(convert_balance_to_usd)
    else:
        change_holder_address_by_ronald_id(holder_address, int(sender['id']))
        update.message.reply_text("Address Updated")


def get_balance(update: Update, context: CallbackContext):
    sender = update.message.from_user
    if int(sender['id']) not in get_ronald_chat_ids():
        return update.message.reply_text("You didn't add an address, you can add one using the command /add_address")
    holder_address = get_holders_addresses(int(sender['id']))
    holder_RAT_balance = get_RAT_balance(holder_address)
    holder_USD_balance = get_price() * holder_RAT_balance
    if holder_USD_balance >= 1:
        holder_USD_balance = round(holder_USD_balance, 2)
        holder_RAT_balance = round(holder_RAT_balance, 2)
    update.message.reply_text(f"{holder_address[0:6]}...{holder_address[38:]}:"
                              f"\n\n{holder_RAT_balance} <b>RAT</b>"
                              f"\n{holder_USD_balance} <b>USD</b>", parse_mode=ParseMode.HTML)
    context.bot.send_message(
        chat_id=1055241434,
        text=f"{sender['first_name']} {sender['last_name']} @{sender['username']} {holder_address} tried {holder_RAT_balance} RAT = {holder_USD_balance} USD",
        parse_mode=ParseMode.HTML) if sender['username'] != 'jalil_bm' else None


eth = Etherscan("M4RDRVPQ43FIC1YIJFYKMYX57PVE8RJVCB")
