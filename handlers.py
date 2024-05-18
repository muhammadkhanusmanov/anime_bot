from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler,ConversationHandler
from main import (
    starting,adminst,usrfunc,addadmin,deladmin,
    addobuna,delobuna
)


updater=Updater('7192449430:AAG9ymICUKqb2v2TFZFby1CwwmI891XJTEI')

dp = updater.dispatcher
dp.add_handler(CommandHandler('start',starting))
dp.add_handler(CallbackQueryHandler(adminst,pattern='st'))
dp.add_handler(CallbackQueryHandler(usrfunc,pattern='us'))
dp.add_handler(MessageHandler(Filters.regex(r'^admin\+'),addadmin))
dp.add_handler(MessageHandler(Filters.regex(r'^admin\-'),deladmin))
dp.add_handler(MessageHandler(Filters.regex(r'^obuna\+'),addobuna))
dp.add_handler(MessageHandler(Filters.regex(r'^obuna\-'),delobuna))

updater.start_polling()
updater.idle()