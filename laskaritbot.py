#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update, job_queue,):
    job_queue.run_daily(kysyLaskarit,, [0, 1, 2, 3, 4, 5, 6], context=None, name=None) 
    
def kysyLaskarit(bot, update):
    keyboard = [[InlineKeyboardButton("Joo", callback_data='1'),
                 InlineKeyboardButton("Ei :(", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Oletko tehnyt laskarit???', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    updater.dispatcher.add_handler(CommandHandler('start', start, 
                                  pass_job_queue=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(button,
                                  pass_job_queue=True))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()