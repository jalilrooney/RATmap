from telegram import Update, ForceReply, Chat, ChatMember, ParseMode, ChatMemberUpdated
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ChatMemberHandler
import time
import calendar
import requests
from datetime import datetime
from fake_headers import Headers


def get_price():
    pattern = "%Y/%m/%d %H:%M:%S"
    gmt_midnight_timestamp = int(calendar.timegm(time.strptime(datetime.utcnow().strftime("%Y/%m/%d") + " " + "00:00:00", pattern))) * 1000
    candles = requests.get(f"https://www.dextools.io/chain-ethereum/api/Uniswap/history/candles?sym=usd&span=day&pair=0xb5759fcd538824ecc3ae1b1e201f35cad3fc4988&ts={gmt_midnight_timestamp}", headers=Headers(os="mac", headers=True).generate()).json()["data"]["candles"]
    while not candles:
        gmt_midnight_timestamp -= 86400000
        candles = requests.get(f"https://www.dextools.io/chain-ethereum/api/Uniswap/history/candles?sym=usd&span=day&pair=0xb5759fcd538824ecc3ae1b1e201f35cad3fc4988&ts={gmt_midnight_timestamp}", headers=Headers(os="mac", headers=True).generate()).json()["data"]["candles"]
    price = float(candles[-1]["close"])
    return price


def convert_balance_to_usd(update: Update, context: CallbackContext) -> None:
    sender = update.message.from_user
    if sender['is_bot']:
        return
    RAT_balance = update.message.text.lower().replace("/ratusd", "").replace("rat", "").strip()
    if update.message.chat.type != "private":
        update.message.reply_text('For your own privacy, always send me the /ratusd command as a private message here @RolandRATmapBOT')
        return
    try:
        balance = float(RAT_balance or "1")
    except Exception:
        update.message.reply_text('Please enter a correct value')
        return
    usd_balance = balance * get_price()
    formatted_usd_balance = str('{0:.20f}'.format(usd_balance)).rstrip('0')
    if usd_balance >= 1:
        formatted_usd_balance = round(balance * get_price(), 2)
    sender = update.message.from_user
    update.message.reply_text(f"{formatted_usd_balance} <b>USD</b>", parse_mode=ParseMode.HTML)
