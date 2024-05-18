from telegram.ext import Updater,CommandHandler,CallbackContext,Filters,MessageHandler,CallbackQueryHandler,ConversationHandler
from telegram import (
    Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,
    InlineKeyboardButton,ChatAdministratorRights,ParseMode, MenuButtonWebApp,WebAppInfo,InputFile
    )
import sqlite3

bot = Bot('7192449430:AAG9ymICUKqb2v2TFZFby1CwwmI891XJTEI')

def starting(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    a=cr.execute(command).fetchall()
    if a:
        text = "Assalomu alaykum botga xush kelibsiz, bo'limlardan birini tanlang."
        btn0 = InlineKeyboardButton('Animelar⚙️', callback_data='st anim')
        btn1 = InlineKeyboardButton('Majburiy Obuna',callback_data=f'st ob')
        btn2 = InlineKeyboardButton('Admin⚙️',callback_data='st adm')
        btn3 = InlineKeyboardButton("Statistika",callback_data='st stc')
        btn4 = InlineKeyboardButton('Xabar yuborish',callback_data='st snd')
        btn = InlineKeyboardMarkup([[btn0],[btn1,btn3], [btn2,btn4]])
        bot.send_message(chat_id=chat_id, text=text, reply_markup=btn)
    else:
        command = f"""
        SELECT * FROM Users WHERE chat_id = "{chat_id}"
        """
        b = cr.execute(command).fetchall()
        if not b:
            command = f"""
            INSERT INTO Users (chat_id) VALUES ("{chat_id}")
            """
            cr.execute(command)
            cnt.commit()
        text = f"Assalomu alaykum {update.message.from_user.first_name} botga xush kelibsiz!"
        command = f"""
        SELECT name FROM Obuna
        """
        channels = cr.execute(command).fetchall()
        if channels:
            btn = []
            for channel in channels:
                chat = context.bot.get_chat(channel[0])
                channel_name = chat.title
                btn.append([InlineKeyboardButton(channel_name,callback_data='obuna',url=f'https://t.me/{channel[0][1:]}')])
            text+="Botdan to'liq foydalanish uchun quyidagi kanallarga obuna bo'ling."
            btn.append([InlineKeyboardButton('Tekshirish',callback_data='us chk')])
            bot.send_message(chat_id,text,reply_markup=InlineKeyboardMarkup(btn))
        else:
            bot.send_message(chat_id,text)
    # except:
    #     pass

def adminst(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    b = query.data.split(' ')[1]
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    if b == 'stc':
        command = "SELECT COUNT(*) FROM Users"
        n = cr.execute(command).fetchone()[0]
        bot.send_message(chat_id,f'Botdagi umumiy foydalanuvchilar {n} ta')
    elif b == 'adm':
        text = 'Adminlar:\n'
        admns = cr.execute('SELECT * FROM Admins').fetchall()
        k=0
        for admn in admns:
            text+=f'1)`{admn[1]}`\n'
            k+=1
        text+="Yanggi admin qo'shish uchun:\nadmin+user_id\n\nAdmin o'chirish uchun:\nadmin-user_id"
        bot.send_message(chat_id,text,parse_mode=ParseMode.MARKDOWN)
    elif b == 'anim':
        btn1 = InlineKeyboardButton("Anime qoshish",callback_data='anm add')
        btn2 = InlineKeyboardButton("Anime o'chirish",callback_data='anm del')
        btn = InlineKeyboardMarkup([[btn1,btn2]])
        bot.send_message(chat_id,"Bo'limlardan birini tanlang",reply_markup=btn)
    elif b =='ob':
        text = "Majburiy obuna qo'shish uchun:\n`obuna+username`\n\nMavjud obunani o'chirish uchun:\n `obuna-username`"
        bot.send_message(chat_id,text,parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id,f"Foydalanuvchilarga xabar yuborish uchun yubormoqchi xabaringizga reply qilib `send` so'zini yuboring.",parse_mode=ParseMode.MARKDOWN)

def check(chat_id,bot,channels):
    for channel in channels:
        chan1=bot.getChatMember(channel[0],str(chat_id))['status']
        if chan1=='left':
            return False
    return True

def usrfunc(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    b = query.data.split(' ')[1] 
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    command = f"""
     SELECT name FROM Obuna
    """
    channel = cr.execute(command).fetchall()
    a = check(chat_id,bot,channel)
    bot.delete_message(chat_id,msg)
    if a:
        text = "Obuna mufavaqiyatli amalga oshirildi!\nBo'limlardan birini tanlang."
        btn1 = InlineKeyboardButton("🔍Anime Qidirish",callback_data='ser ser')
        btn2 = InlineKeyboardButton("💸Reklama va Homiylik",callback_data='ser rek')
        btn3 = InlineKeyboardButton("📚Qo'llanma",callback_data='ser qul')
        btn = InlineKeyboardMarkup([[btn1],[btn2,btn3]])
        bot.sendMessage(chat_id,text,reply_markup=btn)
    else:
        bot.sendMessage(chat_id,'Obuna bo\'lishda xatolik!')


def addadmin(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin:
        user_id = update.message.text[6:]
        command = f"""
        INSERT INTO Admins (chat_id) VALUES ("{user_id}")
        """
        cr.execute(command)
        cnt.commit()
        bot.send_message(chat_id,'✅')


def deladmin(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin:
        user_id = update.message.text[6:]
        try:
            a=cr.execute(f'DELETE FROM Admins WHERE chat_id = "{user_id}"').fetchall()
            cnt.commit()
            bot.sendMessage(chat_id,'☑️')
        except:
            bot.sendMessage(chat_id,'Qandaydir xatolik')


def addobuna(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin:
        channel = update.message.text[6:]
        try:
            a = bot.get_chat_member(channel,chat_id)['status']
            command = f"""
                INSERT INTO Obuna (name) VALUES ("{channel}")
            """
            cr.execute(command)
            cnt.commit()
            bot.sendMessage(chat_id,'✅')
        except:
            bot.sendMessage(chat_id,'Qandaydir xatolik')


def delobuna(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin:
        channel = update.message.text[6:]
        try:
            a = bot.get_chat_member(channel,chat_id)['status']
            command = f"""
                DELETE FROM Obuna WHERE name = "{channel}"
            """
            cr.execute(command)
            cnt.commit()
            bot.sendMessage(chat_id,'✅')
        except:
            bot.sendMessage(chat_id,'Qandaydir xatolik')
    