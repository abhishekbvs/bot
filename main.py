#!/usr/bin/python3.6
import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from decouple import config


from leave_record import LeaveRecord

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TYPE, REASON = range(2)


def start(bot, context):
    user = bot.message.from_user
    bot.message.reply_text("Hi @" + user['username'] + "!\n I am chowkidar of amFOSS.")
    bot.message.reply_text(
        "Here is what I can do for you - \n"
        "/leaverecord - register your leave record"
    )
    bot.message.reply_text("/help - for more details")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    token = config('BOT_TOKEN')
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    l = LeaveRecord
    leave_handler = ConversationHandler(
        entry_points=[CommandHandler('leaverecord', l.getType)],

        states={
            TYPE: [MessageHandler(Filters.regex('^(Health|Family/Home|Tired|Academics|Duty)$'), l.getReason)],
            REASON: [MessageHandler(Filters.text, l.registerLeave)]
        },

        fallbacks=[CommandHandler('cancel', l.cancel)]
    )

    dp.add_handler(leave_handler)
    dp.add_error_handler(error)
    updater.start_webhook(listen='0.0.0.0',
                      port=8443,
                      url_path=token,
                      key='private.key',
                      cert='cert.pem',
                      webhook_url='https://ec2-18-232-129-114.compute-1.amazonaws.com:8443/'+token)
    updater.idle()


if __name__ == '__main__':
    main()
