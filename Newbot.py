import os
import telebot
import requests
import json
import re
import threading
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==================== TOKEN FROM ENVIRONMENT (SECURE) ====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable not set!")

bot = telebot.TeleBot(BOT_TOKEN)

# API Configuration
BASE_URL = "https://movements-invoice-amanda-victoria.trycloudflare.com/search"
API_KEY = "mysecretkey123"
FAMILY_API_URL = "https://atof.onrender.com/full-search"

# Admin Configuration
ADMIN_USERNAME_1 = "saifali2123"
ADMIN_USERNAME_2 = "saifali883883"

# ==================== AUTO-DELETE FUNCTION ====================
def auto_delete_message(chat_id, message_id, delay=30):
    def delete():
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
    threading.Timer(delay, delete).start()

# ==================== NO RESULT FUNCTION ====================
def send_no_result(chat_id, custom_text=None):
    try:
        if custom_text:
            text = custom_text
        else:
            text = "❌ 𝑲𝒖𝒄𝒉 𝒏𝒂𝒉𝒊 𝒎𝒊𝒍𝒂!\n\n𝑲𝒓𝒑𝒚𝒂 𝒔𝒂𝒉𝒊 𝒊𝒏𝒑𝒖𝒕 𝒅𝒂𝒍𝒆𝒏 𝒂𝒖𝒓 𝒅𝒖𝒃𝒂𝒓𝒂 𝒕𝒓𝒚 𝒌𝒓𝒆𝒏."
        
        footer = f"\n\n┌─⊱ ✦ 𝑨𝒅𝒎𝒊𝒏 ✦ ⊰─┐\n│ 👑 @{ADMIN_USERNAME_1}\n│ 💬 𝑲𝒐𝒊 𝒑𝒓𝒐𝒃𝒍𝒆𝒎 𝒉𝒐 𝒕𝒐 𝒎𝒆𝒔𝒔𝒂𝒈𝒆 𝒌𝒓𝒐 𝒅𝒎 𝒎𝒂𝒊\n└─────────────┘"
        
        bot.send_message(chat_id, f"{text}{footer}", parse_mode='Markdown')
    except Exception as e:
        bot.send_message(chat_id, f"{text}{footer}", parse_mode='Markdown')

# ==================== STYLES ====================
LINE_SEPARATOR = "─" * 38
DOUBLE_LINE = "═" * 40

HEADER_NUM = "📱 ──⊱ 𝑵𝒖𝒎𝒃𝒆𝒓 𝑺𝒆𝒂𝒓𝒄𝒉 ⊰──"
HEADER_AADHAR = "🆔 ──⊱ 𝑨𝒂𝒅𝒉𝒂𝒓 𝑺𝒆𝒂𝒓𝒄𝒉 ⊰──"
HEADER_FAMILY = "👨‍👩‍👧‍👦 ──⊱ 𝑭𝒂𝒎𝒊𝒍𝒚 𝑫𝒆𝒕𝒂𝒊𝒍𝒔 ⊰──"

ENTRY_BOX_TOP = "╭" + "─" * 38 + "╮"
ENTRY_BOX_BOTTOM = "╰" + "─" * 38 + "╯"
ENTRY_SEPARATOR = "├" + "─" * 38 + "┤"

ADMIN_BOX_TOP = "┌─⊱ ✦ 𝑨𝒅𝒎𝒊𝒏 ✦ ⊰─┐"
ADMIN_BOX_BOTTOM = "└─────────────┘"
POWERED_BOX_TOP = "┌─⊱ ✦ 𝑷𝒐𝒘𝒆𝒓𝒆𝒅 𝑩𝒚 ✦ ⊰─┐"
POWERED_BOX_BOTTOM = "└─────────────┘"
SUPPORT_BOX_TOP = "┌─⊱ ✦ 𝑺𝒖𝒑𝒑𝒐𝒓𝒕 ✦ ⊰─┐"
SUPPORT_BOX_BOTTOM = "└─────────────┘"

ADMIN_LINE = f"\n\n{ADMIN_BOX_TOP}\n│ 👑 @{ADMIN_USERNAME_1}\n│ 💬 𝑲𝒐𝒊 𝒑𝒓𝒐𝒃𝒍𝒆𝒎 𝒉𝒐 𝒕𝒐 𝒎𝒆𝒔𝒔𝒂𝒈𝒆 𝒌𝒓𝒐 𝒅𝒎 𝒎𝒂𝒊\n{ADMIN_BOX_BOTTOM}"
POWERED_BY = f"\n{POWERED_BOX_TOP}\n│ 🔰 @{ADMIN_USERNAME_2}\n{POWERED_BOX_BOTTOM}"
SUPPORT_LINE = f"\n{SUPPORT_BOX_TOP}\n│ 📢 @techhackingsaifali\n{SUPPORT_BOX_BOTTOM}"
FOOTER = f"{ADMIN_LINE}{POWERED_BY}{SUPPORT_LINE}"

# ==================== FUNCTIONS ====================
user_history = {}

def fetch_data(endpoint, param, value):
    try:
        url = f"{BASE_URL}/{endpoint}?{param}={value}&key={API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

def fetch_family_data(aadhar):
    try:
        url = f"{FAMILY_API_URL}?aadhaar={aadhar}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

def format_number_results(data):
    if "error" in data:
        return f"❌ Error: {data['error']}"
    if data.get("status") != "success" or not data.get("result"):
        return None

    results = data["result"]
    formatted = [HEADER_NUM, f"🔍 𝑻𝒐𝒕𝒂𝒍: {len(results)} 𝒆𝒏𝒕𝒓𝒊𝒆𝒔", DOUBLE_LINE]

    for idx, entry in enumerate(results, 1):
        name = entry.get("name", "N/A").strip()
        fname = entry.get("fname", "N/A").strip()
        aadhar = entry.get("aadhar", "N/A")
        num = entry.get("num", "N/A")
        address = entry.get("address", "N/A").strip()
        circle = entry.get("circle", "N/A")
        email = entry.get("email", "N/A") or "Not available"

        formatted.append(ENTRY_BOX_TOP)
        formatted.append(f"│ 📌 𝑬𝒏𝒕𝒓𝒚 #{idx}")
        formatted.append(ENTRY_SEPARATOR)
        formatted.append(f"│ 👤 𝑵𝒂𝒎𝒆: `{name}`")
        formatted.append(f"│ 👨 𝑭𝒂𝒕𝒉𝒆𝒓: `{fname}`")
        formatted.append(f"│ 🆔 𝑨𝒂𝒅𝒉𝒂𝒓: `{aadhar}`")
        formatted.append(f"│ 📱 𝑵𝒖𝒎𝒃𝒆𝒓: `{num}`")
        formatted.append(f"│ 📍 𝑨𝒅𝒅𝒓𝒆𝒔𝒔: `{address[:70]}{'...' if len(address) > 70 else ''}`")
        formatted.append(f"│ 📡 𝑪𝒊𝒓𝒄𝒍𝒆: `{circle}`")
        formatted.append(f"│ 📧 𝑬𝒎𝒂𝒊𝒍: `{email}`")
        formatted.append(ENTRY_BOX_BOTTOM)
        if idx < len(results):
            formatted.append("")

    formatted.append(f"\n{FOOTER}")
    return "\n".join(formatted)

def format_aadhar_results(data):
    if "error" in data:
        return f"❌ Error: {data['error']}"
    if data.get("status") != "success" or not data.get("result"):
        return None

    results = data["result"]
    formatted = [HEADER_AADHAR, f"🔍 𝑻𝒐𝒕𝒂𝒍: {len(results)} 𝒆𝒏𝒕𝒓𝒊𝒆𝒔", DOUBLE_LINE]

    for idx, entry in enumerate(results, 1):
        name = entry.get("name", "N/A").strip()
        fname = entry.get("fname", "N/A").strip()
        aadhar = entry.get("aadhar", "N/A")
        num = entry.get("num", "N/A")
        address = entry.get("address", "N/A").strip()
        circle = entry.get("circle", "N/A")
        email = entry.get("email", "N/A") or "Not available"

        formatted.append(ENTRY_BOX_TOP)
        formatted.append(f"│ 📌 𝑬𝒏𝒕𝒓𝒚 #{idx}")
        formatted.append(ENTRY_SEPARATOR)
        formatted.append(f"│ 👤 𝑵𝒂𝒎𝒆: `{name}`")
        formatted.append(f"│ 👨 𝑭𝒂𝒕𝒉𝒆𝒓: `{fname}`")
        formatted.append(f"│ 📱 𝑵𝒖𝒎𝒃𝒆𝒓: `{num}`")
        formatted.append(f"│ 📍 𝑨𝒅𝒅𝒓𝒆𝒔𝒔: `{address[:70]}{'...' if len(address) > 70 else ''}`")
        formatted.append(f"│ 📡 𝑪𝒊𝒓𝒄𝒍𝒆: `{circle}`")
        formatted.append(f"│ 📧 𝑬𝒎𝒂𝒊𝒍: `{email}`")
        formatted.append(ENTRY_BOX_BOTTOM)
        if idx < len(results):
            formatted.append("")

    formatted.append(f"\n{FOOTER}")
    return "\n".join(formatted)

def format_family_results(data):
    if "error" in data:
        return f"❌ Error: {data['error']}"
    if not data.get("success") or not data.get("details"):
        return None

    details = data["details"]
    card_info = details.get("card_info", {})
    members = details.get("members", [])
    monthly_summary = details.get("monthly_summary", [])
    ration_card_id = data.get("ration_card_id", "N/A")

    formatted = [HEADER_FAMILY, DOUBLE_LINE, ENTRY_BOX_TOP, "│ 📋 𝑪𝒂𝒓𝒅 𝑰𝒏𝒇𝒐𝒓𝒎𝒂𝒕𝒊𝒐𝒏", ENTRY_SEPARATOR,
                 f"│ 🆔 𝑹𝒂𝒕𝒊𝒐𝒏 𝑪𝒂𝒓𝒅 𝑰𝑫: `{ration_card_id}`",
                 f"│ 🏷️ 𝑪𝒂𝒓𝒅 𝑻𝒚𝒑𝒆: `{card_info.get('Card Type', 'N/A')}`",
                 f"│ 📋 𝑺𝒄𝒉𝒆𝒎𝒆: `{card_info.get('Scheme', 'N/A')}`",
                 f"│ 🏠 𝑯𝒐𝒎𝒆 𝑭𝑷𝑺: `{card_info.get('Home FPS', 'N/A')}`",
                 f"│ 📍 𝑫𝒊𝒔𝒕𝒓𝒊𝒄𝒕: `{card_info.get('District', 'N/A')}`",
                 f"│ 🏛️ 𝑺𝒕𝒂𝒕𝒆: `{card_info.get('State', 'N/A')}`",
                 f"│ 📅 𝑰𝒔𝒔𝒖𝒆 𝑫𝒂𝒕𝒆: `{card_info.get('Issue Date', 'N/A')}`",
                 f"│ 📍 𝑨𝒅𝒅𝒓𝒆𝒔𝒔: `{card_info.get('Address', 'N/A')}`",
                 ENTRY_BOX_BOTTOM, ""]

    if members:
        formatted.append(ENTRY_BOX_TOP)
        formatted.append(f"│ 👥 𝑭𝒂𝒎𝒊𝒍𝒚 𝑴𝒆𝒎𝒃𝒆𝒓𝒔 ({len(members)})")
        formatted.append(ENTRY_SEPARATOR)
        
        for idx, member in enumerate(members, 1):
            formatted.append(f"│ 👤 𝑴𝒆𝒎𝒃𝒆𝒓 #{idx}")
            formatted.append(f"│   📛 𝑵𝒂𝒎𝒆: `{member.get('member_name', 'N/A')}`")
            formatted.append(f"│   🔄 𝑹𝒆𝒍𝒂𝒕𝒊𝒐𝒏: `{member.get('relationship', 'N/A')}`")
            formatted.append(f"│   ⚥ 𝑮𝒆𝒏𝒅𝒆𝒓: `{member.get('gender', 'N/A')}`")
            formatted.append(f"│   🆔 𝑼𝑰𝑫: `{member.get('uid_masked', 'N/A')}`")
            formatted.append(f"│   ✅ 𝑬-𝑲𝒀𝑪: `{member.get('ekyc_status', 'N/A')}`")
            formatted.append(f"│   📅 𝑳𝒂𝒔𝒕 𝑼𝒑𝒅𝒂𝒕𝒆𝒅: `{member.get('cr_last_updated', 'N/A')}`")
            if idx < len(members):
                formatted.append("│   " + "•" * 20)
        
        formatted.append(ENTRY_BOX_BOTTOM)
        formatted.append("")

    if monthly_summary:
        formatted.append(ENTRY_BOX_TOP)
        formatted.append("│ 📊 𝑴𝒐𝒏𝒕𝒉𝒍𝒚 𝑺𝒖𝒎𝒎𝒂𝒓𝒚")
        formatted.append(ENTRY_SEPARATOR)
        
        for summary in monthly_summary:
            formatted.append(f"│   📆 {summary.get('month', 'N/A')}")
            formatted.append(f"│   👥 𝑴𝒆𝒎𝒃𝒆𝒓𝒔: `{summary.get('member_count', 'N/A')}`")
            formatted.append(f"│   📅 𝑪𝒂𝒑𝒕𝒖𝒓𝒆𝒅: `{summary.get('captured_on', 'N/A')}`")
            formatted.append("│   " + "•" * 15)
        
        formatted.append(ENTRY_BOX_BOTTOM)

    formatted.append(f"\n{FOOTER}")
    return "\n".join(formatted)

# ==================== WELCOME MESSAGE ====================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        user_first_name = message.from_user.first_name or "User"
        user_username = message.from_user.username or "No Username"
        user_id = message.from_user.id
        
        welcome_text = (
            "╔═══════════════════════════════════════════╗\n"
            "║   ✦ 𝑾𝑬𝑳𝑪𝑶𝑴𝑬 𝑻𝑶 𝑰𝑵𝑭𝑶 𝑮𝑹𝑶𝑼𝑷 𝑩𝒀 𝑺𝑨𝑰𝑭 𝑨𝑳𝑰 ✦   ║\n"
            "╚═══════════════════════════════════════════╝\n\n"
            f"👋 *𝑯𝒆𝒍𝒍𝒐* `{user_first_name}` !\n"
            f"🆔 *𝑼𝒔𝒆𝒓𝒏𝒂𝒎𝒆:* @{user_username}\n"
            f"🔢 *𝑼𝒔𝒆𝒓 𝑰𝑫:* `{user_id}`\n\n"
            "┌─⊱ 🔍 𝑨𝒃𝒐𝒖𝒕 𝑩𝒐𝒕 ⊰─┐\n"
            "│ 📌 𝑨𝒂𝒑𝒌𝒂 𝒐𝒏𝒍𝒊𝒏𝒆 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒕𝒊𝒐𝒏\n"
            "│    𝒔𝒆𝒂𝒓𝒄𝒉 𝒑𝒂𝒓𝒕𝒏𝒆𝒓!\n"
            "│ 💡 𝑺𝒊𝒎𝒑𝒍𝒆, 𝑭𝒂𝒔𝒕 & 𝑹𝒆𝒍𝒊𝒂𝒃𝒍𝒆\n"
            "└─────────────────────────┘\n\n"
            "┌─⊱ 📋 𝑨𝒗𝒂𝒊𝒍𝒂𝒃𝒍𝒆 𝑪𝒐𝒎𝒎𝒂𝒏𝒅𝒔 ⊰─┐\n"
            "│ 🔹 `/num <𝒑𝒉𝒐𝒏𝒆_𝒏𝒖𝒎𝒃𝒆𝒓>`\n"
            "│    ➜ 10 𝒅𝒊𝒈𝒊𝒕 𝒏𝒖𝒎𝒃𝒆𝒓 𝒔𝒆𝒂𝒓𝒄𝒉\n"
            "│ 🔹 `/aadhar <𝒂𝒂𝒅𝒉𝒂𝒓_𝒏𝒖𝒎𝒃𝒆𝒓>`\n"
            "│    ➜ 12 𝒅𝒊𝒈𝒊𝒕 𝑨𝒂𝒅𝒉𝒂𝒓 𝒔𝒆𝒂𝒓𝒄𝒉\n"
            "│ 🔹 `/family <𝒂𝒂𝒅𝒉𝒂𝒓_𝒏𝒖𝒎𝒃𝒆𝒓>`\n"
            "│    ➜ 𝑭𝒂𝒎𝒊𝒍𝒚/𝑹𝒂𝒕𝒊𝒐𝒏 𝒅𝒆𝒕𝒂𝒊𝒍𝒔\n"
            "│ 🔹 `/history`\n"
            "│    ➜ 𝑺𝒆𝒂𝒓𝒄𝒉 𝒉𝒊𝒔𝒕𝒐𝒓𝒚\n"
            "│ 🔹 `/clearhistory`\n"
            "│    ➜ 𝑪𝒍𝒆𝒂𝒓 𝒉𝒊𝒔𝒕𝒐𝒓𝒚\n"
            "└─────────────────────────┘\n\n"
            "┌─⊱ 📌 𝑬𝒙𝒂𝒎𝒑𝒍𝒆𝒔 ⊰─┐\n"
            "│ `/num 9661756498`\n"
            "│ `/aadhar 962397300673`\n"
            "│ `/family 202372727238`\n"
            "└─────────────────────────┘\n\n"
            "┌─⊱ ⏰ 𝑨𝒖𝒕𝒐-𝑫𝒆𝒍𝒆𝒕𝒆 ⊰─┐\n"
            "│ ✅ 𝑴𝒆𝒔𝒔𝒂𝒈𝒆𝒔 𝒂𝒖𝒕𝒐-𝒅𝒆𝒍𝒆𝒕𝒆\n"
            "│    𝒉𝒐𝒏𝒈𝒆 30 𝒔𝒆𝒄𝒐𝒏𝒅𝒔 𝒎𝒆𝒊𝒏\n"
            "└─────────────────────────┘\n"
            f"{ADMIN_LINE}{POWERED_BY}{SUPPORT_LINE}"
        )
        
        msg = bot.reply_to(message, welcome_text, parse_mode='Markdown')
        auto_delete_message(message.chat.id, msg.message_id, 60)
        auto_delete_message(message.chat.id, message.message_id, 60)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# ==================== COMMANDS ====================
@bot.message_handler(commands=['num'])
def handle_number(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            send_no_result(message.chat.id, "❌ 𝑷𝒍𝒆𝒂𝒔𝒆 𝒑𝒓𝒐𝒗𝒊𝒅𝒆 𝒂 𝒑𝒉𝒐𝒏𝒆 𝒏𝒖𝒎𝒃𝒆𝒓.\n𝑬𝒙𝒂𝒎𝒑𝒍𝒆: `/num 9661756498`")
            return

        number = parts[1].strip()
        if not number.isdigit() or len(number) != 10:
            send_no_result(message.chat.id, "❌ 𝑰𝒏𝒗𝒂𝒍𝒊𝒅 𝒏𝒖𝒎𝒃𝒆𝒓. 𝑷𝒍𝒆𝒂𝒔𝒆 10 𝒅𝒊𝒈𝒊𝒕 𝒏𝒖𝒎𝒃𝒆𝒓 𝒅𝒂𝒍𝒆.")
            return

        user_id = message.from_user.id
        if user_id not in user_history:
            user_history[user_id] = []
        user_history[user_id].append({
            "command": "/num",
            "input": number,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        processing_msg = bot.reply_to(message, "⏳ 𝑺𝒆𝒂𝒓𝒄𝒉𝒊𝒏𝒈... 𝑷𝒍𝒆𝒂𝒔𝒆 𝒘𝒂𝒊𝒕...")
        data = fetch_data("number", "number", number)
        formatted_result = format_number_results(data)
        
        if formatted_result is None:
            auto_delete_message(message.chat.id, processing_msg.message_id, 5)
            send_no_result(message.chat.id)
            return
        
        result_msg = bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            text=formatted_result,
            parse_mode='Markdown'
        )
        
        auto_delete_message(message.chat.id, result_msg.message_id, 30)
        auto_delete_message(message.chat.id, message.message_id, 30)

    except Exception as e:
        send_no_result(message.chat.id, f"❌ 𝑬𝒓𝒓𝒐𝒓: {str(e)}")

@bot.message_handler(commands=['aadhar'])
def handle_aadhar(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            send_no_result(message.chat.id, "❌ 𝑷𝒍𝒆𝒂𝒔𝒆 𝒑𝒓𝒐𝒗𝒊𝒅𝒆 𝒂𝒏 𝑨𝒂𝒅𝒉𝒂𝒓 𝒏𝒖𝒎𝒃𝒆𝒓.\n𝑬𝒙𝒂𝒎𝒑𝒍𝒆: `/aadhar 962397300673`")
            return

        aadhar = parts[1].strip()
        if not aadhar.isdigit() or len(aadhar) != 12:
            send_no_result(message.chat.id, "❌ 𝑰𝒏𝒗𝒂𝒍𝒊𝒅 𝑨𝒂𝒅𝒉𝒂𝒓. 𝑷𝒍𝒆𝒂𝒔𝒆 12 𝒅𝒊𝒈𝒊𝒕 𝑨𝒂𝒅𝒉𝒂𝒓 𝒅𝒂𝒍𝒆.")
            return

        user_id = message.from_user.id
        if user_id not in user_history:
            user_history[user_id] = []
        user_history[user_id].append({
            "command": "/aadhar",
            "input": aadhar,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        processing_msg = bot.reply_to(message, "⏳ 𝑺𝒆𝒂𝒓𝒄𝒉𝒊𝒏𝒈... 𝑷𝒍𝒆𝒂𝒔𝒆 𝒘𝒂𝒊𝒕...")
        data = fetch_data("aadhar", "aadhar", aadhar)
        formatted_result = format_aadhar_results(data)
        
        if formatted_result is None:
            auto_delete_message(message.chat.id, processing_msg.message_id, 5)
            send_no_result(message.chat.id)
            return
        
        result_msg = bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            text=formatted_result,
            parse_mode='Markdown'
        )
        
        auto_delete_message(message.chat.id, result_msg.message_id, 30)
        auto_delete_message(message.chat.id, message.message_id, 30)

    except Exception as e:
        send_no_result(message.chat.id, f"❌ 𝑬𝒓𝒓𝒐𝒓: {str(e)}")

@bot.message_handler(commands=['family'])
def handle_family(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            send_no_result(message.chat.id, "❌ 𝑷𝒍𝒆𝒂𝒔𝒆 𝒑𝒓𝒐𝒗𝒊𝒅𝒆 𝒂𝒏 𝑨𝒂𝒅𝒉𝒂𝒓 𝒏𝒖𝒎𝒃𝒆𝒓.\n𝑬𝒙𝒂𝒎𝒑𝒍𝒆: `/family 202372727238`")
            return

        aadhar = parts[1].strip()
        if not aadhar.isdigit() or len(aadhar) != 12:
            send_no_result(message.chat.id, "❌ 𝑰𝒏𝒗𝒂𝒍𝒊𝒅 𝑨𝒂𝒅𝒉𝒂𝒓. 𝑷𝒍𝒆𝒂𝒔𝒆 12 𝒅𝒊𝒈𝒊𝒕 𝑨𝒂𝒅𝒉𝒂𝒓 𝒅𝒂𝒍𝒆.")
            return

        user_id = message.from_user.id
        if user_id not in user_history:
            user_history[user_id] = []
        user_history[user_id].append({
            "command": "/family",
            "input": aadhar,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        processing_msg = bot.reply_to(message, "⏳ 𝑭𝒆𝒕𝒄𝒉𝒊𝒏𝒈 𝒅𝒆𝒕𝒂𝒊𝒍𝒔... 𝑷𝒍𝒆𝒂𝒔𝒆 𝒘𝒂𝒊𝒕...")
        data = fetch_family_data(aadhar)
        formatted_result = format_family_results(data)
        
        if formatted_result is None:
            auto_delete_message(message.chat.id, processing_msg.message_id, 5)
            send_no_result(message.chat.id)
            return
        
        result_msg = bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            text=formatted_result,
            parse_mode='Markdown'
        )
        
        auto_delete_message(message.chat.id, result_msg.message_id, 30)
        auto_delete_message(message.chat.id, message.message_id, 30)

    except Exception as e:
        send_no_result(message.chat.id, f"❌ 𝑬𝒓𝒓𝒐𝒓: {str(e)}")

@bot.message_handler(commands=['history'])
def show_history(message):
    user_id = message.from_user.id
    if user_id not in user_history or not user_history[user_id]:
        send_no_result(message.chat.id, "📭 𝑵𝒐 𝒔𝒆𝒂𝒓𝒄𝒉 𝒉𝒊𝒔𝒕𝒐𝒓𝒚.")
        return

    history = user_history[user_id][-10:]
    formatted = ["📜 *𝑺𝒆𝒂𝒓𝒄𝒉 𝑯𝒊𝒔𝒕𝒐𝒓𝒚*", DOUBLE_LINE]
    
    for entry in reversed(history):
        formatted.append(f"⏰ `{entry['timestamp']}`")
        formatted.append(f"📌 *{entry['command']}* `{entry['input']}`")
        formatted.append(LINE_SEPARATOR)
    
    msg = bot.reply_to(message, "\n".join(formatted), parse_mode='Markdown')
    auto_delete_message(message.chat.id, msg.message_id, 30)
    auto_delete_message(message.chat.id, message.message_id, 30)

@bot.message_handler(commands=['clearhistory'])
def clear_history(message):
    user_id = message.from_user.id
    if user_id in user_history:
        user_history[user_id] = []
        msg = bot.reply_to(message, "🗑️ 𝑯𝒊𝒔𝒕𝒐𝒓𝒚 𝒄𝒍𝒆𝒂𝒓𝒆𝒅.", parse_mode='Markdown')
    else:
        msg = bot.reply_to(message, "📭 𝑵𝒐 𝒉𝒊𝒔𝒕𝒐𝒓𝒚 𝒕𝒐 𝒄𝒍𝒆𝒂𝒓.", parse_mode='Markdown')
    
    auto_delete_message(message.chat.id, msg.message_id, 30)
    auto_delete_message(message.chat.id, message.message_id, 30)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    send_no_result(message.chat.id, "❓ 𝑼𝒏𝒌𝒏𝒐𝒘𝒏 𝒄𝒐𝒎𝒎𝒂𝒏𝒅. 𝑼𝒔𝒆 /help")

# ==================== MAIN ====================
if __name__ == "__main__":
    print("🤖 Bot is running...")
    print("📌 Bot Token: " + ("✓ Set" if BOT_TOKEN else "✗ Missing"))
    print("📌 Commands: /num, /aadhar, /family, /history, /clearhistory")
    print("⏰ Auto-delete: 30 seconds")
    bot.infinity_polling()
