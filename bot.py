# -*- coding: utf-8 -*-
import os
import telebot
import requests
import re
import threading
import time
import json
import sys
import io
import sqlite3
import random
import string
from datetime import datetime, timedelta
from flask import Flask
from telebot.types import MessageEntity, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ==================== FLASK ====================
flask_app = Flask(__name__)
BOT_START_TIME = time.time()

@flask_app.route('/')
def home():
    return "🔥 SAIF OSINT BOT is running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    flask_app.run(host='0.0.0.0', port=port)

# ==================== CONFIG ====================
# Token – aap chahe toh environment variable se bhi le sakte ho
BOT_TOKEN = "8664037209:AAEnvAJuyw_wyWqKLmgwN-OroTFn_sXMYhw"   # Isko apne hisaab se badal lo
ADMIN_ID = 7500110150
PARTNER_ID = 6186265634

UNLIMITED_USERS = [ADMIN_ID, PARTNER_ID, 6270244216, 1518639734]

CHANNEL_ID = -1003932190548
GROUP_ID = -1003862483348
CHANNEL_LINK = "https://t.me/techhackingapi_saifali77"
GROUP_LINK = "https://t.me/numtoinfosaifalihff"
BACKUP_CHANNEL_LINK = "https://t.me/techhackingsaifali"
BACKUP_CHANNEL_USERNAME = "techhackingsaifali"

PHONE_KEY = "mysecretkey123"
AADHAR_KEY = "mysecretkey123"
VEHICLE_INFO_KEY = "paid-key-lifetime"
VEHICLE_TO_NUM_KEY = "paid-key-lifetime"
PAN_INFO_KEY = "DRIFT"

PHONE_URL = 'https://movements-invoice-amanda-victoria.trycloudflare.com/search/number'
AADHAR_URL = 'https://bronx-web-api.onrender.com/api/key-bronx/aadhar'
VEHICLE_INFO_URL = 'https://simple-rc-info.vercel.app/rc'
VEHICLE_TO_NUM_URL = 'https://carter-handheld-textbook-fairy.trycloudflare.com/vnum'
IP_INFO_URL = 'https://sudipta-ip-info.vercel.app/api/v1/ip'
GST_INFO_URL = 'https://sudipta-gst.sudipta.workers.dev/'
IFSC_INFO_URL = 'https://ifsc.razorpay.com/'
PAN_INFO_URL = 'https://drift-pan-info.vercel.app/pan-info'
NAME_SEARCH_URL = 'https://aadhar.ek4nsh.in/'

RESULT_VIDEO_URL = "https://www.image2url.com/r2/default/videos/1786259979579-39550222-56a8-4114-b7b5-ea6e8d2790c4.mp4"
WELCOME_VIDEO_URL = "https://www.image2url.com/r2/default/videos/1786201406583-2992920a-9d19-4d6a-a130-118413cdf4f5.mp4"
OWNER_PHOTO_URL = 'https://kommodo.ai/i/flHOWFDne1dEc4czUcSq'

# ==================== DATABASE ====================
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, 
    tries INTEGER DEFAULT 5,
    banned INTEGER DEFAULT 0,
    gender TEXT DEFAULT 'unknown',
    verified INTEGER DEFAULT 0
)''')
try:
    cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT DEFAULT 'unknown'")
    conn.commit()
except sqlite3.OperationalError:
    pass
try:
    cursor.execute("ALTER TABLE users ADD COLUMN verified INTEGER DEFAULT 0")
    conn.commit()
except sqlite3.OperationalError:
    pass

cursor.execute('''CREATE TABLE IF NOT EXISTS promo_codes (
    code TEXT PRIMARY KEY, 
    reward_tries INTEGER, 
    max_users INTEGER, 
    used_count INTEGER DEFAULT 0, 
    used_by TEXT DEFAULT '', 
    generated_by INTEGER
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS offer_used (user_id INTEGER PRIMARY KEY)''')
conn.commit()

bot = telebot.TeleBot(BOT_TOKEN)
user_history = {}
user_states = {}
user_lang = {}
temp_data = {}
promo_data = {}
user_page = {}

# ==================== PREMIUM EMOJI MAP ====================
PREMIUM_EMOJI_MAP = {
    '👑': '6089349454823952869',
    '😈': '5260553279321944543',
    '⚡': '6192989708620928755',
    '🎯': '6161480398313362346',
    '😋': '6089003761496232797',
    '🤩': '6253440243735730251',
    '🚀': '6282739376757674628',
    '🔎': '5206473031110631274',
    '❌': '5273914604752216432',
    '📷': '5204150591969830562',
    '☠️': '6276304167128536423',
    '⚠️': '6280762184267994079',
    '❤️‍🔥': '6192987101575780123',
    '📱': '5330237710655306682',
    '🔑': '6176966310920983412',
    '🛡': '6028551194861899805',
    '💙': '5319213852456402176',
    '🔐': '5350619413533958825',
    '💀': '6087162775304409688',
    '🥃': '6192635880625150393',
    '✔️': '5206607081334906820',
    '🛸': '6253440243735730251',
    '🚬': '6192959334612211755',
    '🧀': '6192858776542910960',
    '😎': '6280749428215124956',
    '🏪': '5208573502046610594',
    '😉': '6269298139165889540',
    '😌': '6269144224717870116',
    '😍': '6269464775307038921',
    '🥰': '6269520996428943568',
    '🃏': '6192851170155829005',
    '🪶': '6276154599187421142',
    '💖': '6278022132572101696',
    '🌎': '6114021507908767611',
    '📣': '6053275839821257175',
    '👥': '5989800724312101453',
    '🪩': '6028306016653807599',
    '💐': '6028195661764103744'
}

# ==================== MENU ====================
ITEMS_PER_PAGE = 6
MENU_ITEMS = [
    "👑 BOT OWNER",
    "🔑 Redeem Promo Code",
    "💀 My Account",
    "📱 Num Info",
    "🆔 Aadhar Info",
    "🚗 Vehicle Info",
    "🚗 Vehicle to Number",
    "🛡 IP Info",
    "💙 GST Info",
    "🔐 IFSC Info",
    "🆔 PAN Info",
    "🔍 Name Search"
]

# ==================== REQUEST SESSION ====================
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

# ==================== TEXTS ====================
LANGUAGES = {'en': {'flag': '🇬🇧', 'name': 'English'}, 'hi': {'flag': '🇮🇳', 'name': 'हिंदी'}}
TEXTS = {
    'en': {
        'welcome': "👑 Welcome to SAIF OSINT BOT 👑\n\n                         😉😌😍🥰\n\n😈 Your Ultimate OSINT Tool\n\n⚡ Features:\n• Phone Number Search\n• Aadhar Card Search\n• Vehicle Info Search\n• IP, GST, IFSC Info\n• PAN Info\n• Name Search\n• And More!\n\n😈 Type /help to see all commands\n\n🎯 Owner: @SAIFALI883883",
        'help': "📚 SAIF OSINT BOT - COMMANDS\n\n⚡ BASIC:\n/start - Start Bot\n/help - Show Commands\n/owner - Bot Owner\n/account - My Account\n\n📞 PHONE SEARCH:\n/num 9876543210 - Phone Search\n/aadhar 962397300673 - Aadhar Search\n\n🚗 VEHICLE SEARCH:\n/vehicle MH02FZ0555 - Vehicle Info\n/veh2num MH02FZ0555 - Vehicle to Number\n\n🌐 NETWORK:\n/ip 8.8.8.8 - IP Info\n/gst 22AAAAA0000A1Z5 - GST Info\n/ifsc SBIN0012455 - IFSC Info\n\n🆔 PAN INFO:\n/pan XYZAB1234C - PAN Card Details\n\n🔍 NAME SEARCH:\n/name Rahul - Search by Name",
        'ask_num': '⚠️ Send 10-digit mobile number ⚠️:',
        'ask_aadhar': '⚠️ Send 12-digit Aadhar number ⚠️:',
        'ask_vehicle': '⚠️ Send vehicle number (e.g. MH02FZ0555) ⚠️:',
        'ask_veh2num': '⚠️ Send vehicle number for details ⚠️:',
        'ask_ip': '⚠️ Send IP address ⚠️:',
        'ask_gst': '⚠️ Send GST number (15 chars) ⚠️:',
        'ask_ifsc': '⚠️ Send IFSC code ⚠️:',
        'ask_pan': '⚠️ Send PAN number (e.g. XYZAB1234C) ⚠️:',
        'ask_namesearch': '⚠️ Send name to search ⚠️:',
        'err_num': '❌ Mobile number must be 10 digits.',
        'err_aadhar': '❌ Aadhar must be 12 digits.',
        'err_vehicle': '❌ Invalid vehicle number format!',
        'err_ip': '❌ Invalid IP format!',
        'err_gst': '❌ Invalid GST format!',
        'err_ifsc': '❌ Invalid IFSC format!',
        'err_pan': '❌ Invalid PAN format! (e.g. XYZAB1234C)',
        'err_namesearch': '❌ Please send a valid name.',
        'no_history': '📭 No search history found.',
        'history_cleared': '🗑️ History cleared!',
        'no_tries': '❌ No searches left! 💡 Please redeem a promo code using the "🔑 Redeem Promo Code" button or contact admin.',
        'choose_lang': '🌐 Choose your language:',
    },
    'hi': {
        'welcome': "👑 सैफ OSINT बॉट में आपका स्वागत है 👑\n\n                         😉😌😍🥰\n\n😈 आपका Ultimate OSINT टूल\n\n⚡ फीचर्स:\n• मोबाइल नंबर सर्च\n• आधार कार्ड सर्च\n• वाहन इंफो सर्च\n• IP, GST, IFSC इंफो\n• PAN इंफो\n• Name Search\n• और भी बहुत कुछ!\n\n😈 सभी कमांड्स के लिए /help टाइप करें\n\n🎯 मालिक: @SAIFALI883883",
        'help': "📚 सैफ OSINT बॉट - कमांड्स\n\n⚡ बेसिक:\n/start - बॉट शुरू करें\n/help - कमांड्स देखें\n/owner - मालिक की जानकारी\n/account - मेरा अकाउंट\n\n📞 फोन सर्च:\n/num 9876543210 - फोन सर्च\n/aadhar 962397300673 - आधार सर्च\n\n🚗 वाहन सर्च:\n/vehicle MH02FZ0555 - वाहन इंफो\n/veh2num MH02FZ0555 - वाहन से नंबर\n\n🌐 नेटवर्क:\n/ip 8.8.8.8 - IP इंफो\n/gst 22AAAAA0000A1Z5 - GST इंफो\n/ifsc SBIN0012455 - IFSC इंफो\n\n🆔 PAN इंफो:\n/pan XYZAB1234C - PAN कार्ड डिटेल्स\n\n🔍 NAME SEARCH:\n/name Rahul - नाम से सर्च",
        'ask_num': '⚠️ 10 अंकीय मोबाइल नंबर भेजें ⚠️:',
        'ask_aadhar': '⚠️ 12 अंकीय आधार नंबर भेजें ⚠️:',
        'ask_vehicle': '⚠️ वाहन नंबर भेजें (जैसे MH02FZ0555) ⚠️:',
        'ask_veh2num': '⚠️ वाहन नंबर से डिटेल्स पाने के लिए भेजें ⚠️:',
        'ask_ip': '⚠️ IP address भेजें ⚠️:',
        'ask_gst': '⚠️ GST नंबर (15 अक्षर) भेजें ⚠️:',
        'ask_ifsc': '⚠️ IFSC code भेजें ⚠️:',
        'ask_pan': '⚠️ PAN नंबर भेजें (जैसे XYZAB1234C) ⚠️:',
        'ask_namesearch': '⚠️ सर्च करने के लिए नाम भेजें ⚠️:',
        'err_num': '❌ मोबाइल नंबर 10 अंकों का होना चाहिए।',
        'err_aadhar': '❌ आधार 12 अंकों का होना चाहिए।',
        'err_vehicle': '❌ गलत वाहन नंबर फॉर्मेट!',
        'err_ip': '❌ गलत IP फॉर्मेट!',
        'err_gst': '❌ गलत GST फॉर्मेट!',
        'err_ifsc': '❌ गलत IFSC फॉर्मेट!',
        'err_pan': '❌ गलत PAN फॉर्मेट! (जैसे XYZAB1234C)',
        'err_namesearch': '❌ कृपया एक वैध नाम भेजें।',
        'no_history': '📭 कोई सर्च इतिहास नहीं मिला।',
        'history_cleared': '🗑️ इतिहास साफ कर दिया गया!',
        'no_tries': '❌ कोई सर्च बचा नहीं! 💡 कृपया "🔑 Redeem Promo Code" बटन का उपयोग करें या एडमिन से संपर्क करें।',
        'choose_lang': '🌐 अपनी भाषा चुनें:',
    }
}

# ==================== CORE HELPERS ====================
def get_user_tries(user_id):
    c = conn.cursor()
    c.execute("SELECT tries, banned, verified FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    c.close()
    return (result[0], result[1], result[2]) if result else (0, 0, 0)

def add_tries(user_id, amount):
    c = conn.cursor()
    c.execute("SELECT tries FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        c.execute("UPDATE users SET tries = tries + ? WHERE user_id = ?", (amount, user_id))
    else:
        c.execute("INSERT INTO users (user_id, tries) VALUES (?, ?)", (user_id, amount))
    conn.commit()
    c.close()
    return True

def use_try(user_id):
    if user_id in UNLIMITED_USERS:
        return True
    c = conn.cursor()
    c.execute("SELECT tries FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result and result[0] > 0:
        c.execute("UPDATE users SET tries = tries - 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        c.close()
        return True
    c.close()
    return False

def get_remaining_tries(user_id):
    if user_id in UNLIMITED_USERS:
        return 999999
    c = conn.cursor()
    c.execute("SELECT tries FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    c.close()
    return result[0] if result else 0

def is_user_banned(user_id):
    c = conn.cursor()
    c.execute("SELECT banned FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    c.close()
    return result[0] == 1 if result else False

def is_user_verified(user_id):
    c = conn.cursor()
    c.execute("SELECT verified FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    c.close()
    return result[0] == 1 if result else False

def set_user_verified(user_id):
    c = conn.cursor()
    c.execute("UPDATE users SET verified = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    c.close()

def register_user(user_id):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, tries, banned, gender, verified) VALUES (?, 5, 0, 'unknown', 0)", (user_id,))
    conn.commit()
    c.close()
    return True

def get_lang(user_id):
    return user_lang.get(user_id, 'en')

def save_to_history(user_id, query_type, query_value):
    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].append(f"{query_type}: {query_value}")
    if len(user_history[user_id]) > 20:
        user_history[user_id].pop(0)

def get_random_emoji():
    return random.choice(["🔥","🚀","💎","✨","🌟","⚡","🎯","💪","🤖","🛸","🌈","⭐","🎉","💥","🔮","🦅","🚨","🎇","🧿"])

def sanitize_raw_data(data):
    if not isinstance(data, dict):
        return data
    cleaned = data.copy()
    unwanted = ['powered_by', 'api_info', 'credit', 'sources', 'bronx', 'ultra', 'by', 'developer', 'api_credit', 'source', '_proxy', 'response_time', 'timestamp', 'response_time_seconds']
    for key in unwanted:
        cleaned.pop(key, None)
    if 'api_1_car_info' in cleaned and isinstance(cleaned['api_1_car_info'], dict):
        for key in unwanted:
            cleaned['api_1_car_info'].pop(key, None)
    if 'api_2_ummym' in cleaned:
        cleaned.pop('api_2_ummym', None)
    if 'credit' in cleaned:
        cleaned.pop('credit', None)
    if 'response_time_seconds' in cleaned:
        cleaned.pop('response_time_seconds', None)
    if 'timestamp' in cleaned:
        cleaned.pop('timestamp', None)
    return cleaned

def safe_delete_message(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass

def get_footer(user_id=None):
    footer_text = ""
    if user_id and (user_id not in UNLIMITED_USERS):
        remaining = get_remaining_tries(user_id)
        footer_text += f"\n🔍 Remaining Searches: {remaining}"
    footer_text += "\n🛡️ POWERED BY @SAIFALI883883"
    footer_text += "\n👑 PARTNERSHIP @HACKK4FUN"
    footer_text += "\n🤖 Bot: @Osint_saifali_V7_bot"
    return footer_text

def generate_promo_code():
    prefixes = ["SAIFALI", "ALISAIF", "SAIF"]
    prefix = random.choice(prefixes)
    if prefix == "SAIF":
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    else:
        length = random.randint(4, 6)
        suffix = ''.join(random.choices(string.digits, k=length))
    code = prefix + suffix
    c = conn.cursor()
    c.execute("SELECT code FROM promo_codes WHERE code = ?", (code,))
    if c.fetchone():
        c.close()
        return generate_promo_code()
    c.close()
    return code

# ==================== ENTITY HELPERS ====================
def utf16_len(s):
    return len(s.encode('utf-16-le')) // 2

def get_entities_for_premium_emojis(text, extra_map=None):
    entities = []
    all_emojis = PREMIUM_EMOJI_MAP.copy()
    if extra_map:
        all_emojis.update(extra_map)
    for emoji, emoji_id in all_emojis.items():
        start = 0
        while True:
            pos = text.find(emoji, start)
            if pos == -1:
                break
            offset_utf16 = utf16_len(text[:pos])
            length_utf16 = utf16_len(emoji)
            entities.append(MessageEntity(
                type="custom_emoji",
                offset=offset_utf16,
                length=length_utf16,
                custom_emoji_id=emoji_id
            ))
            start = pos + 1
    return entities

def send_prompt(chat_id, prompt_text):
    entities = get_entities_for_premium_emojis(prompt_text)
    bot.send_message(chat_id, prompt_text, entities=entities)

# ==================== SEND RESULT ====================
def send_result_with_buttons(chat_id, loading_msg, formatted_text, raw_data, user_id=None, response_time=None):
    safe_delete_message(chat_id, loading_msg.message_id)
    final_text = formatted_text
    if user_id and (user_id not in UNLIMITED_USERS):
        remaining = get_remaining_tries(user_id)
        final_text += f"\n\n🔍 Remaining Searches: {remaining}"
    if response_time is not None:
        final_text += f"\n⏱ Response Time: {response_time:.2f} sec"
    footer_text = get_footer(user_id)
    final_text += footer_text

    emoji = get_random_emoji()
    caption_text = f"{emoji} SAIF OSINT RESULT {emoji}\n🤖 @Osint_saifali_V7_bot"
    bot.send_video(
        chat_id,
        video=RESULT_VIDEO_URL,
        caption=caption_text,
        parse_mode='HTML',
        supports_streaming=True
    )

    if len(final_text) > 4096:
        for i in range(0, len(final_text), 4000):
            chunk = final_text[i:i+4000]
            bot.send_message(chat_id, chunk, parse_mode='HTML')
    else:
        bot.send_message(chat_id, final_text, parse_mode='HTML')

    keyboard = InlineKeyboardMarkup(row_width=2)
    token = str(time.time()) + "_" + str(chat_id)
    clean_data = sanitize_raw_data(raw_data)
    temp_data[token] = {'formatted': formatted_text, 'raw': clean_data}
    keyboard.add(
        InlineKeyboardButton("📋 COPY", callback_data=f"copy_{token}", style="success"),
        InlineKeyboardButton("📄 JSON", callback_data=f"json_{token}", style="success")
    )
    bot.send_message(chat_id, f"{get_random_emoji()} Options:", reply_markup=keyboard)

# ==================== MEMBERSHIP ====================
def check_membership(user_id):
    try:
        channel_member = bot.get_chat_member(CHANNEL_ID, user_id)
        if channel_member.status not in ['member', 'administrator', 'creator']:
            return False, "Channel"
        group_member = bot.get_chat_member(GROUP_ID, user_id)
        if group_member.status not in ['member', 'administrator', 'creator']:
            return False, "Group"
        backup_chat = bot.get_chat(f"@{BACKUP_CHANNEL_USERNAME}")
        backup_member = bot.get_chat_member(backup_chat.id, user_id)
        if backup_member.status not in ['member', 'administrator', 'creator']:
            return False, "Backup Channel"
        return True, None
    except:
        return False, "Unknown"

def enforce_membership(chat_id, user_id, message_obj=None, call_obj=None):
    if not is_user_verified(user_id):
        return True
    is_member, _ = check_membership(user_id)
    if is_member:
        return True

    c = conn.cursor()
    c.execute("UPDATE users SET verified = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    c.close()

    text = (
        "💐 Welcome to SAIF OSINT BOT\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🛡 Please join our official channels to continue:\n\n"
        "📣 Main Channel\n"
        "👥 Main Group\n"
        "🪩 Backup Channel\n\n"
        "✨ After joining all three, click the ✔️ Joined button below.\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    all_entities = get_entities_for_premium_emojis(text)

    links = [
        ("Main Channel", CHANNEL_LINK),
        ("Main Group", GROUP_LINK),
        ("Backup Channel", BACKUP_CHANNEL_LINK)
    ]
    for name, url in links:
        pos = text.find(name)
        if pos != -1:
            offset = utf16_len(text[:pos])
            length = utf16_len(name)
            all_entities.append(MessageEntity(
                type="text_link",
                offset=offset,
                length=length,
                url=url
            ))

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("✔️ Joined", callback_data="verify_me", style="success"))

    if message_obj:
        try: bot.delete_message(chat_id, message_obj.message_id)
        except: pass
    if call_obj:
        try: bot.edit_message_reply_markup(chat_id, call_obj.message.message_id, reply_markup=None)
        except: pass

    bot.send_message(chat_id, text, entities=all_entities, reply_markup=keyboard)
    return False

# ==================== UI FUNCTIONS ====================
def show_menu_page(chat_id, user_id, page=0, lang='en'):
    total_items = len(MENU_ITEMS)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    start_idx = page * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, total_items)
    page_items = MENU_ITEMS[start_idx:end_idx]

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for item in page_items:
        keyboard.add(KeyboardButton(item))
    if user_id == ADMIN_ID:
        keyboard.add(KeyboardButton("⚙️ Admin Panel"))

    nav_row = []
    if page > 0:
        nav_row.append("⬅️ PREVIOUS PAGE")
    if page < total_pages - 1:
        nav_row.append("NEXT PAGE ➡️")
    if nav_row:
        keyboard.add(*[KeyboardButton(btn) for btn in nav_row])

    header = f"🃏 PAGE {page + 1} – Menu Options\n\n😋 Choose an option:\n\n<b>🤖 Bot: @Osint_saifali_V7_bot</b>"
    footer = "\n\n🪶 BOT MADE BY 💖 : @SAIFALI883883"
    full_text = header + footer

    user_page[user_id] = page
    entities = get_entities_for_premium_emojis(full_text)
    bot_start = full_text.find('🤖 Bot: @Osint_saifali_V7_bot')
    if bot_start != -1:
        offset_utf16 = utf16_len(full_text[:bot_start])
        length_utf16 = utf16_len('🤖 Bot: @Osint_saifali_V7_bot')
        entities.append(MessageEntity(type="bold", offset=offset_utf16, length=length_utf16))
    bot.send_message(chat_id, full_text, reply_markup=keyboard, entities=entities)

def send_main_menu(chat_id, user_id, lang='en'):
    show_menu_page(chat_id, user_id, 0, lang)

# ==================== WELCOME ====================
def send_welcome_message(chat_id, user_id, lang='en', gender='unknown'):
    text = TEXTS[lang]['welcome']
    entities = get_entities_for_premium_emojis(text)
    bot.send_video(
        chat_id,
        video=WELCOME_VIDEO_URL,
        caption=text,
        caption_entities=entities,
        supports_streaming=True
    )
    send_main_menu(chat_id, user_id, lang)

def show_owner_details(chat_id, user_id, lang):
    text = """🎯 BOT OWNER

🔹 🥃 Name : SAIF ALI (Bihari ❤️‍🔥)
🔹 ✔️ Username : @SAIFALI883883
🔹 🛸 Age : 18+ (Young & Energetic 🚀)
🔹 🚬 Lover : Bhojpuri Music 🎵, RCB LOVER, Gold Flake Lover
🔹 🧀 Motto : "Bihari hoon, code bhi likhta hoon, aur dil bhi jeet leta hoon!" ✨
🔹 Fun Fact : I can hack your heart with my code! ❤️‍🔥
🔹 Bot      : @Osint_saifali_V7_bot 🤖
🔹 Contact  : 📷 Instagram: @nxt_level_saif

🔹 🏪 DM for collaboration or just to say hi! 😄"""
    entities = get_entities_for_premium_emojis(text)
    bot.send_photo(
        chat_id,
        photo=OWNER_PHOTO_URL,
        caption=text,
        caption_entities=entities
    )
    send_main_menu(chat_id, user_id, lang)

def send_language_selection(chat_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en", style="success"),
        InlineKeyboardButton("🇮🇳 हिंदी", callback_data="lang_hi", style="success")
    )
    bot.send_message(chat_id, TEXTS['en']['choose_lang'], reply_markup=keyboard)

# ==================== NAVIGATION ====================
@bot.message_handler(func=lambda m: m.text == "⬅️ PREVIOUS PAGE")
def prev_page(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    page = user_page.get(uid, 0)
    if page > 0:
        show_menu_page(m.chat.id, uid, page-1)
    else:
        bot.reply_to(m, "❌ Already on first page!")

@bot.message_handler(func=lambda m: m.text == "NEXT PAGE ➡️")
def next_page(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    page = user_page.get(uid, 0)
    total = (len(MENU_ITEMS) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    if page < total - 1:
        show_menu_page(m.chat.id, uid, page+1)
    else:
        bot.reply_to(m, "❌ Already on last page!")

# ==================== MENU BUTTON HANDLERS ====================
@bot.message_handler(func=lambda m: m.text == "👑 BOT OWNER")
def btn_owner(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    show_owner_details(m.chat.id, uid, get_lang(uid))
    send_main_menu(m.chat.id, uid, get_lang(uid))

@bot.message_handler(func=lambda m: m.text == "🔑 Redeem Promo Code")
def btn_redeem(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    user_states[uid] = "waiting_promo_code"
    bot.reply_to(m, "🎁 Send promo code:")

@bot.message_handler(func=lambda m: m.text == "💀 My Account")
def btn_account(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    tries = get_remaining_tries(uid)
    text = f"💀 MY ACCOUNT\n👤 ID: {uid}\n🔍 Remaining: {tries}"
    bot.send_message(m.chat.id, text, parse_mode='HTML')
    send_main_menu(m.chat.id, uid, get_lang(uid))

@bot.message_handler(func=lambda m: m.text == "📱 Num Info")
def btn_num(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    if not can_search(uid):
        bot.reply_to(m, TEXTS[get_lang(uid)]['no_tries'])
        return
    user_states[uid] = "waiting_num"
    send_prompt(m.chat.id, TEXTS[get_lang(uid)]['ask_num'])

@bot.message_handler(func=lambda m: m.text == "🆔 Aadhar Info")
def btn_aadhar(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    if not can_search(uid):
        bot.reply_to(m, TEXTS[get_lang(uid)]['no_tries'])
        return
    user_states[uid] = "waiting_aadhar"
    send_prompt(m.chat.id, TEXTS[get_lang(uid)]['ask_aadhar'])

@bot.message_handler(func=lambda m: m.text == "🚗 Vehicle Info")
def btn_vehicle(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    if not can_search(uid):
        bot.reply_to(m, TEXTS[get_lang(uid)]['no_tries'])
        return
    user_states[uid] = "waiting_vehicle"
    send_prompt(m.chat.id, TEXTS[get_lang(uid)]['ask_vehicle'])

@bot.message_handler(func=lambda m: m.text == "🚗 Vehicle to Number")
def btn_veh2num(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    if not can_search(uid):
        bot.reply_to(m, TEXTS[get_lang(uid)]['no_tries'])
        return
    user_states[uid] = "waiting_veh2num"
    send_prompt(m.chat.id, TEXTS[get_lang(uid)]['ask_veh2num'])

@bot.message_handler(func=lambda m: m.text == "🛡 IP Info")
def btn_ip(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    if not can_search(uid):
        bot.reply_to(m, TEXTS[get_lang(uid)]['no_tries'])
        return
    user_states[uid] = "waiting_ip"
    send_prompt(m.chat.id, TEXTS[get_lang(uid)]['ask_ip'])

@bot.message_handler(func=lambda m: m.text == "💙 GST Info")
def btn_gst(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    if not can_search(uid):
        bot.reply_to(m, TEXTS[get_lang(uid)]['no_tries'])
        return
    user_states[uid] = "waiting_gst"
    send_prompt(m.chat.id, TEXTS[get_lang(uid)]['ask_gst'])

@bot.message_handler(func=lambda m: m.text == "🔐 IFSC Info")
def btn_ifsc(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    if not can_search(uid):
        bot.reply_to(m, TEXTS[get_lang(uid)]['no_tries'])
        return
    user_states[uid] = "waiting_ifsc"
    send_prompt(m.chat.id, TEXTS[get_lang(uid)]['ask_ifsc'])

@bot.message_handler(func=lambda m: m.text == "🆔 PAN Info")
def btn_pan(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    if not can_search(uid):
        bot.reply_to(m, TEXTS[get_lang(uid)]['no_tries'])
        return
    user_states[uid] = "waiting_pan"
    send_prompt(m.chat.id, TEXTS[get_lang(uid)]['ask_pan'])

@bot.message_handler(func=lambda m: m.text == "🔍 Name Search")
def btn_namesearch(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    if not can_search(uid):
        bot.reply_to(m, TEXTS[get_lang(uid)]['no_tries'])
        return
    user_states[uid] = "waiting_namesearch"
    send_prompt(m.chat.id, TEXTS[get_lang(uid)]['ask_namesearch'])

# ==================== ADMIN PANEL ====================
@bot.message_handler(func=lambda m: m.text == "⚙️ Admin Panel" and m.from_user.id == ADMIN_ID)
def admin_panel(m):
    if not enforce_membership(m.chat.id, m.from_user.id, message_obj=m):
        return
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton("📊 Bot Status"))
    keyboard.add(KeyboardButton("📦 Generate Promo Code"))
    keyboard.add(KeyboardButton("🚫 Ban User"))
    keyboard.add(KeyboardButton("✅ Unban User"))
    keyboard.add(KeyboardButton("📢 Broadcast Message"))
    keyboard.add(KeyboardButton("🔙 Back to Menu"))
    bot.send_message(m.chat.id, "⚙️ ADMIN PANEL", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "📊 Bot Status" and m.from_user.id == ADMIN_ID)
def admin_status(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE banned=1")
    banned = c.fetchone()[0]
    c.execute("SELECT SUM(used_count) FROM promo_codes")
    total_redemptions = c.fetchone()[0] or 0
    c.close()

    uptime_seconds = int(time.time() - BOT_START_TIME)
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    uptime_str = f"{days}d {hours}h {minutes}m"

    text = f"""📊 BOT STATUS
═══════════════════════
👥 Total Users: {total}
🚫 Banned Users: {banned}
🎁 Total Promo Redemptions: {total_redemptions}
⏱️ Bot Uptime: {uptime_str}
═══════════════════════"""
    bot.send_message(m.chat.id, text, parse_mode='HTML')
    admin_panel(m)

@bot.message_handler(func=lambda m: m.text == "📦 Generate Promo Code" and m.from_user.id == ADMIN_ID)
def admin_gen_promo(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    user_states[uid] = "admin_gen_promo_step1"
    send_prompt(m.chat.id, "⚠️ Kitne search ka code banana hai? ⚠️\n(e.g., 20)")

@bot.message_handler(func=lambda m: m.text == "🚫 Ban User" and m.from_user.id == ADMIN_ID)
def admin_ban_user(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    user_states[uid] = "admin_ban"
    send_prompt(m.chat.id, "⚠️ Enter User ID to ban ⚠️:")

@bot.message_handler(func=lambda m: m.text == "✅ Unban User" and m.from_user.id == ADMIN_ID)
def admin_unban_user(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    user_states[uid] = "admin_unban"
    send_prompt(m.chat.id, "⚠️ Enter User ID to unban ⚠️:")

@bot.message_handler(func=lambda m: m.text == "📢 Broadcast Message" and m.from_user.id == ADMIN_ID)
def admin_broadcast(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    user_states[uid] = "admin_broadcast"
    send_prompt(m.chat.id, "⚠️ Send broadcast message (text/photo/video) ⚠️:")

@bot.message_handler(func=lambda m: m.text == "🔙 Back to Menu" and m.from_user.id == ADMIN_ID)
def admin_back(m):
    uid = m.from_user.id
    if not enforce_membership(m.chat.id, uid, message_obj=m):
        return
    send_main_menu(m.chat.id, uid, get_lang(uid))

# ==================== ADMIN STATE HANDLERS ====================
@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) in ["admin_gen_promo_step1", "admin_gen_promo_step2", "admin_ban", "admin_unban"] and m.from_user.id == ADMIN_ID)
def admin_state_handler(m):
    uid = m.from_user.id
    state = user_states.get(uid)
    chat_id = m.chat.id

    if state == "admin_gen_promo_step1":
        if m.text.isdigit():
            search_count = int(m.text)
            promo_data[uid] = {'search_count': search_count}
            user_states[uid] = "admin_gen_promo_step2"
            send_prompt(chat_id, f"⚠️ Kitne users ke liye? ⚠️\nSearch: {search_count}")
        else:
            bot.send_message(chat_id, "❌ Send a number!")

    elif state == "admin_gen_promo_step2":
        if m.text.isdigit():
            max_users = int(m.text)
            search_count = promo_data.get(uid, {}).get('search_count', 0)
            if search_count:
                code = generate_promo_code()
                c = conn.cursor()
                c.execute("INSERT INTO promo_codes (code, reward_tries, max_users, used_count, generated_by) VALUES (?, ?, ?, 0, ?)",
                          (code, search_count, max_users, uid))
                conn.commit()
                c.close()
                bot.send_message(chat_id, f"🎁 Code: <code>{code}</code>\n🔍 {search_count} searches\n👥 {max_users} users max", parse_mode='HTML')
                user_states[uid] = None
                promo_data.pop(uid, None)
                admin_panel(m)
            else:
                bot.send_message(chat_id, "❌ Session expired!")
        else:
            bot.send_message(chat_id, "❌ Send a number!")

    elif state == "admin_ban":
        if m.text.isdigit():
            user_id = int(m.text)
            c = conn.cursor()
            c.execute("UPDATE users SET banned = 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            c.close()
            bot.send_message(chat_id, f"✅ User {user_id} banned.")
            user_states[uid] = None
            admin_panel(m)
        else:
            bot.send_message(chat_id, "❌ Send numeric ID.")

    elif state == "admin_unban":
        if m.text.isdigit():
            user_id = int(m.text)
            c = conn.cursor()
            c.execute("UPDATE users SET banned = 0 WHERE user_id = ?", (user_id,))
            conn.commit()
            c.close()
            bot.send_message(chat_id, f"✅ User {user_id} unbanned.")
            user_states[uid] = None
            admin_panel(m)
        else:
            bot.send_message(chat_id, "❌ Send numeric ID.")

# ==================== BROADCAST (FULLY UPDATED – Premium Emoji Conversion) ====================
@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "admin_broadcast" and m.from_user.id == ADMIN_ID, content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'animation'])
def broadcast_send(m):
    uid = m.from_user.id
    chat_id = m.chat.id

    header = "📢 BROADCAST\n\n"
    footer = f"\n\n🛡️ POWERED BY @SAIFALI883883\n👑 PARTNERSHIP @HACKK4FUN\n🤖 Bot: @Osint_saifali_V7_bot"

    broadcast_data = {}
    if m.text:
        broadcast_data['type'] = 'text'
        broadcast_data['text'] = m.text
    elif m.photo:
        broadcast_data['type'] = 'photo'
        broadcast_data['photo'] = m.photo[-1].file_id
        broadcast_data['caption'] = m.caption or ''
    elif m.video:
        broadcast_data['type'] = 'video'
        broadcast_data['video'] = m.video.file_id
        broadcast_data['caption'] = m.caption or ''
    elif m.document:
        broadcast_data['type'] = 'document'
        broadcast_data['document'] = m.document.file_id
        broadcast_data['caption'] = m.caption or ''
    elif m.audio:
        broadcast_data['type'] = 'audio'
        broadcast_data['audio'] = m.audio.file_id
        broadcast_data['caption'] = m.caption or ''
    elif m.voice:
        broadcast_data['type'] = 'voice'
        broadcast_data['voice'] = m.voice.file_id
        broadcast_data['caption'] = m.caption or ''
    elif m.animation:
        broadcast_data['type'] = 'animation'
        broadcast_data['animation'] = m.animation.file_id
        broadcast_data['caption'] = m.caption or ''
    else:
        bot.send_message(chat_id, "❌ Unsupported media type.")
        user_states[uid] = None
        return

    c = conn.cursor()
    c.execute("SELECT user_id FROM users")
    users = c.fetchall()
    c.close()

    sent = 0
    failed = 0

    # ---- For text broadcast ----
    if broadcast_data['type'] == 'text':
        full_text = header + broadcast_data['text'] + footer
        # Convert all emojis (from our map) to custom emoji entities
        entities = get_entities_for_premium_emojis(full_text)

    # ---- For media with caption ----
    elif broadcast_data['type'] in ['photo', 'video', 'document', 'audio', 'voice', 'animation']:
        caption = header + broadcast_data['caption'] + footer
        caption_entities = get_entities_for_premium_emojis(caption)
        broadcast_data['caption'] = caption
        broadcast_data['caption_entities'] = caption_entities

    # ---- Send to each user ----
    for u in users:
        try:
            if broadcast_data['type'] == 'text':
                bot.send_message(u[0], full_text, entities=entities)
                sent += 1
            elif broadcast_data['type'] == 'photo':
                bot.send_photo(u[0], broadcast_data['photo'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
                sent += 1
            elif broadcast_data['type'] == 'video':
                bot.send_video(u[0], broadcast_data['video'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'], supports_streaming=True)
                sent += 1
            elif broadcast_data['type'] == 'document':
                bot.send_document(u[0], broadcast_data['document'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
                sent += 1
            elif broadcast_data['type'] == 'audio':
                bot.send_audio(u[0], broadcast_data['audio'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
                sent += 1
            elif broadcast_data['type'] == 'voice':
                bot.send_voice(u[0], broadcast_data['voice'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
                sent += 1
            elif broadcast_data['type'] == 'animation':
                bot.send_animation(u[0], broadcast_data['animation'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
                sent += 1
        except Exception:
            failed += 1
        time.sleep(0.05)

    # ---- Send to Main Channel ----
    try:
        if broadcast_data['type'] == 'text':
            bot.send_message(CHANNEL_ID, full_text, entities=entities)
        elif broadcast_data['type'] == 'photo':
            bot.send_photo(CHANNEL_ID, broadcast_data['photo'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'video':
            bot.send_video(CHANNEL_ID, broadcast_data['video'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'], supports_streaming=True)
        elif broadcast_data['type'] == 'document':
            bot.send_document(CHANNEL_ID, broadcast_data['document'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'audio':
            bot.send_audio(CHANNEL_ID, broadcast_data['audio'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'voice':
            bot.send_voice(CHANNEL_ID, broadcast_data['voice'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'animation':
            bot.send_animation(CHANNEL_ID, broadcast_data['animation'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        channel_status = "✅ Sent to channel"
    except Exception as e:
        channel_status = f"❌ Channel error: {e}"

    # ---- Send to Main Group ----
    try:
        if broadcast_data['type'] == 'text':
            bot.send_message(GROUP_ID, full_text, entities=entities)
        elif broadcast_data['type'] == 'photo':
            bot.send_photo(GROUP_ID, broadcast_data['photo'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'video':
            bot.send_video(GROUP_ID, broadcast_data['video'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'], supports_streaming=True)
        elif broadcast_data['type'] == 'document':
            bot.send_document(GROUP_ID, broadcast_data['document'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'audio':
            bot.send_audio(GROUP_ID, broadcast_data['audio'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'voice':
            bot.send_voice(GROUP_ID, broadcast_data['voice'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'animation':
            bot.send_animation(GROUP_ID, broadcast_data['animation'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        group_status = "✅ Sent to group"
    except Exception as e:
        group_status = f"❌ Group error: {e}"

    # ---- Send to Backup Channel ----
    try:
        backup_chat_id = f"@{BACKUP_CHANNEL_USERNAME}"
        if broadcast_data['type'] == 'text':
            bot.send_message(backup_chat_id, full_text, entities=entities)
        elif broadcast_data['type'] == 'photo':
            bot.send_photo(backup_chat_id, broadcast_data['photo'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'video':
            bot.send_video(backup_chat_id, broadcast_data['video'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'], supports_streaming=True)
        elif broadcast_data['type'] == 'document':
            bot.send_document(backup_chat_id, broadcast_data['document'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'audio':
            bot.send_audio(backup_chat_id, broadcast_data['audio'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'voice':
            bot.send_voice(backup_chat_id, broadcast_data['voice'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        elif broadcast_data['type'] == 'animation':
            bot.send_animation(backup_chat_id, broadcast_data['animation'], caption=broadcast_data['caption'], caption_entities=broadcast_data['caption_entities'])
        backup_status = "✅ Sent to backup channel"
    except Exception as e:
        backup_status = f"❌ Backup error: {e}"

    user_states[uid] = None
    bot.send_message(chat_id, f"✅ Broadcast sent!\n👥 Users: {sent} sent, {failed} failed\n📢 {channel_status}\n👥 {group_status}\n🔔 {backup_status}", parse_mode='HTML')
    admin_panel(m)

# ==================== CALLBACKS ====================
@bot.callback_query_handler(func=lambda call: call.data.startswith('copy_') or call.data.startswith('json_'))
def handle_copy_json(call):
    uid = call.from_user.id
    if not enforce_membership(call.message.chat.id, uid, call_obj=call):
        return
    token = call.data.split('_', 1)[1]
    data = temp_data.get(token)
    if not data:
        bot.answer_callback_query(call.id, text="❌ Data expired", show_alert=True)
        return
    if call.data.startswith('copy_'):
        bot.send_message(call.message.chat.id, data['formatted'], parse_mode='HTML')
        bot.answer_callback_query(call.id, text="✅ Copied!", show_alert=False)
    else:
        json_text = json.dumps(data['raw'], indent=2, ensure_ascii=False)
        if len(json_text) > 4096:
            file = io.BytesIO(json_text.encode('utf-8'))
            file.name = 'result.json'
            bot.send_document(call.message.chat.id, file, caption="📄 Raw JSON")
        else:
            bot.send_message(call.message.chat.id, f"```json\n{json_text}\n```", parse_mode='Markdown')
        bot.answer_callback_query(call.id, text="✅ JSON sent!", show_alert=False)
    temp_data.pop(token, None)

@bot.callback_query_handler(func=lambda call: call.data in [item[1] for item in MENU_ITEMS] or call.data == "admin_panel")
def menu_callback(call):
    uid = call.from_user.id
    chat_id = call.message.chat.id
    if not enforce_membership(chat_id, uid, call_obj=call):
        return
    lang = get_lang(uid)
    action = call.data

    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

    if action == "owner":
        show_owner_details(chat_id, uid, lang)
        send_main_menu(chat_id, uid, lang)
    elif action == "redeem":
        user_states[uid] = "waiting_promo_code"
        bot.send_message(chat_id, "🎁 Send promo code:")
    elif action == "account":
        tries = get_remaining_tries(uid)
        text = f"💀 MY ACCOUNT\n👤 ID: {uid}\n🔍 Remaining: {tries}"
        bot.send_message(chat_id, text, parse_mode='HTML')
        send_main_menu(chat_id, uid, lang)
    elif action in ["num", "aadhar", "vehicle", "veh2num", "ip", "gst", "ifsc", "pan", "namesearch"]:
        if not can_search(uid):
            bot.send_message(chat_id, TEXTS[lang]['no_tries'])
            return
        state_map = {
            "num": "waiting_num",
            "aadhar": "waiting_aadhar",
            "vehicle": "waiting_vehicle",
            "veh2num": "waiting_veh2num",
            "ip": "waiting_ip",
            "gst": "waiting_gst",
            "ifsc": "waiting_ifsc",
            "pan": "waiting_pan",
            "namesearch": "waiting_namesearch"
        }
        state = state_map[action]
        user_states[uid] = state
        ask_key = state.replace("waiting_", "ask_")
        prompt = TEXTS[lang][ask_key]
        send_prompt(chat_id, prompt)
    elif action == "admin_panel":
        if uid == ADMIN_ID:
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                InlineKeyboardButton("📊 Bot Status", callback_data="admin_status", style="success"),
                InlineKeyboardButton("📦 Generate Promo Code", callback_data="admin_gen_promo", style="success"),
                InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban", style="danger"),
                InlineKeyboardButton("✅ Unban User", callback_data="admin_unban", style="success"),
                InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast", style="success"),
                InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu", style="primary")
            )
            bot.send_message(chat_id, "⚙️ ADMIN PANEL", reply_markup=keyboard)
        else:
            bot.answer_callback_query(call.id, text="❌ Only admin!", show_alert=True)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_menu")
def back_menu_callback(call):
    uid = call.from_user.id
    chat_id = call.message.chat.id
    if not enforce_membership(chat_id, uid, call_obj=call):
        return
    send_main_menu(chat_id, uid, user_page.get(uid, 0), get_lang(uid))
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def admin_callback(call):
    uid = call.from_user.id
    if uid != ADMIN_ID:
        bot.answer_callback_query(call.id, text="❌ Only admin!", show_alert=True)
        return
    chat_id = call.message.chat.id
    if not enforce_membership(chat_id, uid, call_obj=call):
        return
    action = call.data
    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

    if action == "admin_status":
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM users WHERE banned=1")
        banned = c.fetchone()[0]
        c.execute("SELECT SUM(used_count) FROM promo_codes")
        total_redemptions = c.fetchone()[0] or 0
        c.close()

        uptime_seconds = int(time.time() - BOT_START_TIME)
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        uptime_str = f"{days}d {hours}h {minutes}m"

        text = f"""📊 BOT STATUS
═══════════════════════
👥 Total Users: {total}
🚫 Banned Users: {banned}
🎁 Total Promo Redemptions: {total_redemptions}
⏱️ Bot Uptime: {uptime_str}
═══════════════════════"""
        bot.send_message(chat_id, text, parse_mode='HTML')
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("📊 Bot Status", callback_data="admin_status", style="success"),
            InlineKeyboardButton("📦 Generate Promo Code", callback_data="admin_gen_promo", style="success"),
            InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban", style="danger"),
            InlineKeyboardButton("✅ Unban User", callback_data="admin_unban", style="success"),
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast", style="success"),
            InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu", style="primary")
        )
        bot.send_message(chat_id, "⚙️ ADMIN PANEL", reply_markup=keyboard)

    elif action == "admin_gen_promo":
        user_states[uid] = "admin_gen_promo_step1"
        send_prompt(chat_id, "⚠️ Kitne search ka code banana hai? ⚠️\n(e.g., 20)")

    elif action == "admin_ban":
        user_states[uid] = "admin_ban"
        send_prompt(chat_id, "⚠️ Enter User ID to ban ⚠️:")

    elif action == "admin_unban":
        user_states[uid] = "admin_unban"
        send_prompt(chat_id, "⚠️ Enter User ID to unban ⚠️:")

    elif action == "admin_broadcast":
        user_states[uid] = "admin_broadcast"
        send_prompt(chat_id, "⚠️ Send broadcast message (text/photo/video) ⚠️:")

    bot.answer_callback_query(call.id)

# ==================== START ====================
@bot.message_handler(commands=['start'])
def start_command(message):
    uid = message.from_user.id
    register_user(uid)

    if is_user_verified(uid):
        is_member, _ = check_membership(uid)
        if not is_member:
            c = conn.cursor()
            c.execute("UPDATE users SET verified = 0 WHERE user_id = ?", (uid,))
            conn.commit()
            c.close()
        else:
            lang = get_lang(uid)
            send_welcome_message(message.chat.id, uid, lang)
            return

    text = (
        "💐 Welcome to SAIF OSINT BOT\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🛡 Please join our official channels to continue:\n\n"
        "📣 Main Channel\n"
        "👥 Main Group\n"
        "🪩 Backup Channel\n\n"
        "✨ After joining all three, click the ✔️ Joined button below.\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    all_entities = get_entities_for_premium_emojis(text)

    links = [
        ("Main Channel", CHANNEL_LINK),
        ("Main Group", GROUP_LINK),
        ("Backup Channel", BACKUP_CHANNEL_LINK)
    ]
    for name, url in links:
        pos = text.find(name)
        if pos != -1:
            offset = utf16_len(text[:pos])
            length = utf16_len(name)
            all_entities.append(MessageEntity(
                type="text_link",
                offset=offset,
                length=length,
                url=url
            ))

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("✔️ Joined", callback_data="verify_me", style="success"))

    bot.send_message(
        message.chat.id,
        text,
        entities=all_entities,
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data == "verify_me")
def verify_me_callback(call):
    uid = call.from_user.id
    chat_id = call.message.chat.id

    is_member, missing = check_membership(uid)
    if not is_member:
        bot.answer_callback_query(call.id, text=f"❌ Please join our {missing} first! (Channel, Group & Backup Channel)", show_alert=True)
        return

    set_user_verified(uid)
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass

    success_text = "✔️ Verified! Please select your language."
    bot.send_message(chat_id, success_text, entities=get_entities_for_premium_emojis(success_text))
    send_language_selection(chat_id)
    bot.answer_callback_query(call.id, text="✅ Verified!", show_alert=False)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def language_selected(call):
    uid = call.from_user.id
    lang_code = call.data.split('_')[1]
    user_lang[uid] = lang_code
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    send_welcome_message(call.message.chat.id, uid, lang_code)
    bot.answer_callback_query(call.id)

def can_search(user_id):
    if user_id in UNLIMITED_USERS:
        return True
    return get_remaining_tries(user_id) > 0

# ==================== FORMATTERS ====================
def format_phone(data):
    lines = []
    lines.append("📱 PHONE INFORMATION")
    lines.append("═" * 40)

    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            data = data[0]
        else:
            return "❌ No data found."

    result = data.get('result', {})
    if not result:
        return "❌ No data found."

    if isinstance(result, list):
        records = result
    elif isinstance(result, dict):
        records = [result]
    else:
        return "❌ No data found."

    total = len(records)
    lines.append(f"\n📊 SUMMARY: {total} RECORD(s) FOUND.\n")

    for idx, rec in enumerate(records, 1):
        lines.append(f"━━━ RECORD {idx} ━━━")
        for key, value in rec.items():
            if value:
                clean_key = key.replace('_', ' ').title()
                lines.append(f"🔹 {clean_key}: {value}")
        lines.append("")

    lines.append("═" * 40)
    return "\n".join(lines)

def format_aadhar(data):
    lines = []
    lines.append("🆔 AADHAR INFORMATION")
    lines.append("═" * 40)
    results = data.get('results', {})
    if not results:
        return "❌ No data found."
    for key, value in results.items():
        if value:
            lines.append(f"🔹 {key.replace('_', ' ').title()}: {value}")
    lines.append("═" * 40)
    return "\n".join(lines)

def format_vehicle_info_new(data):
    lines = []
    lines.append("🚗 VEHICLE INFORMATION")
    lines.append("═" * 40)

    reg = data.get('registration', {})
    lines.append(f"🔢 Registration Number: {data.get('registration_number', 'N/A')}")
    lines.append(f"📅 Registration Date: {reg.get('date', 'N/A')}")
    lines.append(f"🏛️ RTO: {reg.get('rto', 'N/A')}")
    lines.append(f"📍 Authority: {reg.get('authority', 'N/A')}")

    owner = data.get('owner', {})
    lines.append(f"\n👤 Owner Name: {owner.get('name', 'N/A')}")
    lines.append(f"👤 Father's Name: {owner.get('father_name', 'N/A')}")
    lines.append(f"📌 Owner Serial: {owner.get('serial_no', 'N/A')}")

    vehicle = data.get('vehicle', {})
    lines.append(f"\n🚘 Vehicle Class: {vehicle.get('class', 'N/A')}")
    lines.append(f"🏭 Manufacturer: {vehicle.get('manufacturer', 'N/A')}")
    lines.append(f"📐 Model: {vehicle.get('model', 'N/A')}")
    lines.append(f"🔧 Maker Model: {vehicle.get('maker_model', 'N/A')}")
    lines.append(f"⚙️ Variant: {vehicle.get('variant', 'N/A')}")
    lines.append(f"📏 CC: {vehicle.get('cc', 'N/A')}")
    lines.append(f"⛽ Fuel: {vehicle.get('fuel', 'N/A')}")
    lines.append(f"📊 Fuel Norms: {vehicle.get('fuel_norms', 'N/A')}")
    lines.append(f"💺 Seating: {vehicle.get('seating', 'N/A')}")
    lines.append(f"📋 Type: {vehicle.get('type', 'N/A')}")
    lines.append(f"🏪 Commercial: {'Yes' if vehicle.get('commercial') else 'No'}")

    addr = data.get('address', {})
    lines.append(f"\n📍 Present Address: {addr.get('present', 'N/A')}")
    lines.append(f"🏙️ City: {addr.get('city', 'N/A')}")
    lines.append(f"📮 Pincode: {addr.get('pincode', 'N/A')}")

    insurance = data.get('insurance', {})
    lines.append(f"\n🏢 Insurance Company: {insurance.get('company', 'N/A')}")
    lines.append(f"📅 Insurance Valid Upto: {insurance.get('valid_upto', 'N/A')}")
    lines.append(f"📄 Policy No: {insurance.get('policy_no', 'N/A')}")
    lines.append(f"✅ Expired: {'Yes' if insurance.get('expired') else 'No'}")

    fitness = data.get('fitness', {})
    lines.append(f"\n📋 Fitness Upto: {fitness.get('fitness_upto', 'N/A')}")
    lines.append(f"💰 Tax Upto: {fitness.get('tax_upto', 'N/A')}")

    puc = data.get('puc', {})
    lines.append(f"\n🔬 PUC No: {puc.get('no', 'N/A')}")
    lines.append(f"📅 PUC Valid Upto: {puc.get('valid_upto', 'N/A')}")

    ident = data.get('identification', {})
    lines.append(f"\n🔧 Chassis Number: {ident.get('chassis', 'N/A')}")
    lines.append(f"⚙️ Engine Number: {ident.get('engine', 'N/A')}")

    fin = data.get('financier', {})
    lines.append(f"\n🏦 Financier: {fin.get('name', 'N/A')}")

    rto_contact = data.get('rto_contact', {})
    lines.append(f"\n📞 RTO Phone: {rto_contact.get('phone', 'N/A')}")

    lines.append("═" * 40)
    return "\n".join(lines)

def format_name_search(data):
    lines = []
    lines.append("🔍 NAME SEARCH RESULTS")
    lines.append("═" * 40)
    count = data.get('count', 0)
    lines.append(f"📊 Total Results: {count}")
    if count > 0:
        for idx, item in enumerate(data.get('data', []), 1):
            lines.append(f"\n{idx}. {item.get('name', 'N/A')}")
            if item.get('aadhar'):
                lines.append(f"   Aadhar: {item.get('aadhar')}")
            if item.get('phone'):
                lines.append(f"   Phone: {item.get('phone')}")
    lines.append("═" * 40)
    return "\n".join(lines)

# ==================== OTHER COMMANDS ====================
@bot.message_handler(commands=['help'])
def help_command(message):
    uid = message.from_user.id
    if not enforce_membership(message.chat.id, uid, message_obj=message):
        return
    text = TEXTS[get_lang(uid)]['help']
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['owner'])
def owner_command(message):
    uid = message.from_user.id
    if not enforce_membership(message.chat.id, uid, message_obj=message):
        return
    show_owner_details(message.chat.id, uid, get_lang(uid))

@bot.message_handler(commands=['account'])
def account_command(message):
    uid = message.from_user.id
    if not enforce_membership(message.chat.id, uid, message_obj=message):
        return
    tries = get_remaining_tries(uid)
    text = f"💀 MY ACCOUNT\n👤 ID: {uid}\n🔍 Remaining: {tries}"
    bot.send_message(message.chat.id, text, parse_mode='HTML')
    send_main_menu(message.chat.id, uid, get_lang(uid))

@bot.message_handler(commands=['name'])
def name_command(message):
    uid = message.from_user.id
    if not enforce_membership(message.chat.id, uid, message_obj=message):
        return
    if not can_search(uid):
        bot.reply_to(message, TEXTS[get_lang(uid)]['no_tries'])
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "❌ Usage: /name <name>\nExample: /name Rahul")
        return
    query = args[1].strip()
    user_states[uid] = "waiting_namesearch"
    start_time = time.time()
    loading = bot.send_message(message.chat.id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
    try:
        resp = session.get(NAME_SEARCH_URL, params={'name': query}, timeout=30)
        end_time = time.time()
        if resp.status_code == 200:
            data = resp.json()
            if data.get('count', 0) > 0 and data.get('data'):
                result_text = format_name_search(data)
                save_to_history(uid, "NameSearch", query)
                if uid not in UNLIMITED_USERS:
                    use_try(uid)
                send_result_with_buttons(message.chat.id, loading, result_text, data, uid, response_time=end_time-start_time)
            else:
                safe_delete_message(message.chat.id, loading.message_id)
                bot.reply_to(message, "❌ No data found for this name.")
        else:
            safe_delete_message(message.chat.id, loading.message_id)
            bot.reply_to(message, f"❌ API error (HTTP {resp.status_code})")
    except Exception as e:
        safe_delete_message(message.chat.id, loading.message_id)
        bot.reply_to(message, f"❌ Error: {e}")
    user_states[uid] = None

# ==================== MAIN HANDLE_ALL ====================
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    uid = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip() if message.text else ""
    state = user_states.get(uid)
    lang = get_lang(uid)

    if not enforce_membership(chat_id, uid, message_obj=message):
        return

    if state in ["admin_gen_promo_step1", "admin_gen_promo_step2", "admin_ban", "admin_unban", "admin_broadcast"]:
        return

    # Promo code
    if state == "waiting_promo_code":
        code = text.upper()
        c = conn.cursor()
        c.execute("SELECT reward_tries, max_users, used_count FROM promo_codes WHERE code = ?", (code,))
        row = c.fetchone()
        if row:
            reward, max_users, used = row
            if used < max_users:
                add_tries(uid, reward)
                c.execute("UPDATE promo_codes SET used_count = used_count + 1 WHERE code = ?", (code,))
                conn.commit()
                c.close()
                bot.reply_to(message, f"✅ Promo code applied! You got {reward} searches.")
            else:
                bot.reply_to(message, "❌ This promo code has already reached its maximum usage.")
        else:
            bot.reply_to(message, "❌ Invalid promo code.")
        user_states[uid] = None
        send_main_menu(chat_id, uid, lang)
        return

    # Phone
    if state == "waiting_num":
        if not can_search(uid):
            bot.reply_to(message, TEXTS[lang]['no_tries'])
            user_states[uid] = None
            return
        if text.isdigit() and len(text) == 10:
            start_time = time.time()
            loading = bot.send_message(chat_id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
            try:
                resp = session.get(PHONE_URL, params={'number': text, 'key': PHONE_KEY}, timeout=30)
                end_time = time.time()
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('status') == 'success' and data.get('result'):
                        result_text = format_phone(data)
                        save_to_history(uid, "Num", text)
                        if uid not in UNLIMITED_USERS:
                            use_try(uid)
                        send_result_with_buttons(chat_id, loading, result_text, data, uid, response_time=end_time-start_time)
                    else:
                        safe_delete_message(chat_id, loading.message_id)
                        bot.reply_to(message, "❌ No data found.")
                else:
                    safe_delete_message(chat_id, loading.message_id)
                    bot.reply_to(message, f"❌ API error (HTTP {resp.status_code})")
            except Exception as e:
                safe_delete_message(chat_id, loading.message_id)
                bot.reply_to(message, f"❌ Error: {e}")
        else:
            bot.reply_to(message, TEXTS[lang]['err_num'])
        user_states[uid] = None
        return

    # Aadhar
    if state == "waiting_aadhar":
        if not can_search(uid):
            bot.reply_to(message, TEXTS[lang]['no_tries'])
            user_states[uid] = None
            return
        if text.isdigit() and len(text) == 12:
            start_time = time.time()
            loading = bot.send_message(chat_id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
            try:
                resp = session.get(AADHAR_URL, params={'key': AADHAR_KEY, 'num': text}, timeout=30)
                end_time = time.time()
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('success') and data.get('results'):
                        clean_data = {k: v for k, v in data.items() if k not in ['powered_by', 'api_info']}
                        result_text = format_aadhar(clean_data)
                        save_to_history(uid, "Aadhar", text)
                        if uid not in UNLIMITED_USERS:
                            use_try(uid)
                        send_result_with_buttons(chat_id, loading, result_text, clean_data, uid, response_time=end_time-start_time)
                    else:
                        safe_delete_message(chat_id, loading.message_id)
                        bot.reply_to(message, "❌ No data found.")
                else:
                    safe_delete_message(chat_id, loading.message_id)
                    bot.reply_to(message, f"❌ API error (HTTP {resp.status_code})")
            except Exception as e:
                safe_delete_message(chat_id, loading.message_id)
                bot.reply_to(message, f"❌ Error: {e}")
        else:
            bot.reply_to(message, TEXTS[lang]['err_aadhar'])
        user_states[uid] = None
        return

    # Vehicle
    if state == "waiting_vehicle":
        if not can_search(uid):
            bot.reply_to(message, TEXTS[lang]['no_tries'])
            user_states[uid] = None
            return
        if len(text) >= 6:
            start_time = time.time()
            loading = bot.send_message(chat_id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
            vehicle_number = text.upper().strip()
            raw_data = {}
            result_text = None

            try:
                resp = session.get(VEHICLE_INFO_URL, params={'num': vehicle_number}, timeout=90)
                end_time = time.time()
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('status') == 'success' and data.get('api_1_car_info'):
                        car_info = data['api_1_car_info']
                        raw_data = car_info
                        result_text = format_vehicle_info_new(car_info)
            except Exception as e:
                print(f"Vehicle API Error: {e}")
                end_time = time.time()

            if result_text:
                save_to_history(uid, "Vehicle", vehicle_number)
                if uid not in UNLIMITED_USERS:
                    use_try(uid)
                send_result_with_buttons(chat_id, loading, result_text, raw_data, uid, response_time=end_time-start_time)
            else:
                safe_delete_message(chat_id, loading.message_id)
                bot.reply_to(message, "❌ No vehicle data found. Please check the number and try again.")
        else:
            bot.reply_to(message, TEXTS[lang]['err_vehicle'])
        user_states[uid] = None
        return

    # Vehicle to Number
    if state == "waiting_veh2num":
        if not can_search(uid):
            bot.reply_to(message, TEXTS[lang]['no_tries'])
            user_states[uid] = None
            return
        if len(text) >= 6:
            start_time = time.time()
            loading = bot.send_message(chat_id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
            vehicle_number = text.upper().strip()
            result_text = None
            raw_data = {}

            for attempt in range(3):
                try:
                    resp = session.get(VEHICLE_TO_NUM_URL, params={'reg': vehicle_number}, timeout=30)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data and data.get('status') == 'success':
                            raw_data = data
                            result_text = f"🚗 VEHICLE TO NUMBER\n═" * 40
                            for key, value in data.items():
                                if value and key not in ['status', 'timestamp']:
                                    result_text += f"\n🔹 {key.replace('_', ' ').title()}: {value}"
                            result_text += "\n═" * 40
                            break
                    elif resp.status_code == 504:
                        print(f"Gateway Timeout (attempt {attempt+1})")
                        continue
                    else:
                        break
                except requests.exceptions.Timeout:
                    print(f"Timeout (attempt {attempt+1})")
                    continue
                except Exception as e:
                    print(f"Error: {e}")
                    break
                time.sleep(2)

            end_time = time.time()

            if result_text:
                save_to_history(uid, "Veh2Num", vehicle_number)
                if uid not in UNLIMITED_USERS:
                    use_try(uid)
                send_result_with_buttons(chat_id, loading, result_text, raw_data, uid, response_time=end_time-start_time)
            else:
                safe_delete_message(chat_id, loading.message_id)
                bot.reply_to(message, "❌ Vehicle to Number lookup failed. Please try again later.")
        else:
            bot.reply_to(message, TEXTS[lang]['err_vehicle'])
        user_states[uid] = None
        return

    # IP
    if state == "waiting_ip":
        if not can_search(uid):
            bot.reply_to(message, TEXTS[lang]['no_tries'])
            user_states[uid] = None
            return
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', text):
            start_time = time.time()
            loading = bot.send_message(chat_id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
            try:
                resp = session.get(IP_INFO_URL, params={'ip': text}, timeout=30)
                end_time = time.time()
                if resp.status_code == 200:
                    data = resp.json()
                    result_text = f"🛡 IP INFORMATION\n═" * 40 + f"\n{json.dumps(data, indent=2)}"
                    save_to_history(uid, "IP", text)
                    if uid not in UNLIMITED_USERS:
                        use_try(uid)
                    send_result_with_buttons(chat_id, loading, result_text, data, uid, response_time=end_time-start_time)
                else:
                    safe_delete_message(chat_id, loading.message_id)
                    bot.reply_to(message, "❌ IP lookup failed.")
            except Exception as e:
                safe_delete_message(chat_id, loading.message_id)
                bot.reply_to(message, f"❌ Error: {e}")
        else:
            bot.reply_to(message, TEXTS[lang]['err_ip'])
        user_states[uid] = None
        return

    # GST
    if state == "waiting_gst":
        if not can_search(uid):
            bot.reply_to(message, TEXTS[lang]['no_tries'])
            user_states[uid] = None
            return
        if len(text) == 15:
            start_time = time.time()
            loading = bot.send_message(chat_id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
            try:
                resp = session.get(GST_INFO_URL, params={'gst': text.upper()}, timeout=30)
                end_time = time.time()
                if resp.status_code == 200:
                    data = resp.json()
                    result_text = f"💙 GST INFORMATION\n═" * 40 + f"\n{json.dumps(data, indent=2)}"
                    save_to_history(uid, "GST", text)
                    if uid not in UNLIMITED_USERS:
                        use_try(uid)
                    send_result_with_buttons(chat_id, loading, result_text, data, uid, response_time=end_time-start_time)
                else:
                    safe_delete_message(chat_id, loading.message_id)
                    bot.reply_to(message, "❌ GST lookup failed.")
            except Exception as e:
                safe_delete_message(chat_id, loading.message_id)
                bot.reply_to(message, f"❌ Error: {e}")
        else:
            bot.reply_to(message, TEXTS[lang]['err_gst'])
        user_states[uid] = None
        return

    # IFSC
    if state == "waiting_ifsc":
        if not can_search(uid):
            bot.reply_to(message, TEXTS[lang]['no_tries'])
            user_states[uid] = None
            return
        if len(text) >= 4:
            start_time = time.time()
            loading = bot.send_message(chat_id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
            try:
                resp = session.get(IFSC_INFO_URL + text.upper(), timeout=30)
                end_time = time.time()
                if resp.status_code == 200:
                    data = resp.json()
                    result_text = f"🔐 IFSC INFORMATION\n═" * 40 + f"\n{json.dumps(data, indent=2)}"
                    save_to_history(uid, "IFSC", text)
                    if uid not in UNLIMITED_USERS:
                        use_try(uid)
                    send_result_with_buttons(chat_id, loading, result_text, data, uid, response_time=end_time-start_time)
                else:
                    safe_delete_message(chat_id, loading.message_id)
                    bot.reply_to(message, "❌ IFSC lookup failed.")
            except Exception as e:
                safe_delete_message(chat_id, loading.message_id)
                bot.reply_to(message, f"❌ Error: {e}")
        else:
            bot.reply_to(message, TEXTS[lang]['err_ifsc'])
        user_states[uid] = None
        return

    # PAN
    if state == "waiting_pan":
        if not can_search(uid):
            bot.reply_to(message, TEXTS[lang]['no_tries'])
            user_states[uid] = None
            return
        if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', text.upper()):
            start_time = time.time()
            loading = bot.send_message(chat_id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
            try:
                resp = session.get(PAN_INFO_URL, params={'key': PAN_INFO_KEY, 'pan': text.upper()}, timeout=30)
                end_time = time.time()
                if resp.status_code == 200:
                    data = resp.json()
                    result_text = f"🆔 PAN INFORMATION\n═" * 40 + f"\n{json.dumps(data, indent=2)}"
                    save_to_history(uid, "PAN", text)
                    if uid not in UNLIMITED_USERS:
                        use_try(uid)
                    send_result_with_buttons(chat_id, loading, result_text, data, uid, response_time=end_time-start_time)
                else:
                    safe_delete_message(chat_id, loading.message_id)
                    bot.reply_to(message, "❌ PAN lookup failed.")
            except Exception as e:
                safe_delete_message(chat_id, loading.message_id)
                bot.reply_to(message, f"❌ Error: {e}")
        else:
            bot.reply_to(message, TEXTS[lang]['err_pan'])
        user_states[uid] = None
        return

    # Name Search
    if state == "waiting_namesearch":
        if not can_search(uid):
            bot.reply_to(message, TEXTS[lang]['no_tries'])
            user_states[uid] = None
            return
        if len(text) >= 2:
            start_time = time.time()
            loading = bot.send_message(chat_id, "🌎 Processing...", entities=get_entities_for_premium_emojis("🌎 Processing..."))
            try:
                resp = session.get(NAME_SEARCH_URL, params={'name': text}, timeout=30)
                end_time = time.time()
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('count', 0) > 0 and data.get('data'):
                        result_text = format_name_search(data)
                        save_to_history(uid, "NameSearch", text)
                        if uid not in UNLIMITED_USERS:
                            use_try(uid)
                        send_result_with_buttons(chat_id, loading, result_text, data, uid, response_time=end_time-start_time)
                    else:
                        safe_delete_message(chat_id, loading.message_id)
                        bot.reply_to(message, "❌ No data found for this name.")
                else:
                    safe_delete_message(chat_id, loading.message_id)
                    bot.reply_to(message, f"❌ API error (HTTP {resp.status_code})")
            except Exception as e:
                safe_delete_message(chat_id, loading.message_id)
                bot.reply_to(message, f"❌ Error: {e}")
        else:
            bot.reply_to(message, TEXTS[lang]['err_namesearch'])
        user_states[uid] = None
        return

    bot.reply_to(message, "❌ Unknown command or state.")

# ==================== MAIN ====================
if __name__ == '__main__':
    print("🔥 SAIF OSINT BOT STARTED!")
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    try:
        bot.remove_webhook()
    except:
        pass
    while True:
        try:
            bot.infinity_polling(timeout=30)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(5)
