from datetime import time, tzinfo
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

class GMT2(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=2)
    def dst(self, dt):
        return timedelta(0)
    def tzname(self,dt):
        return "Europe/Helsinki"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update, job_queue):
    t = time(20, 0, 0)
    logger.info(t.isoformat())
    job_queue.run_daily(kysyLaskarit, t, (0, 1, 2, 3, 4, 5, 6), context=update.message.chat_id, name=None) 
    update.message.reply_text('Laskarit ajoitus aloitettu about 20')
    
def kysyLaskarit(bot, job):
    keyboard = [[InlineKeyboardButton("Joo", callback_data='1'),
                 InlineKeyboardButton("Ei :(", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(job.context, 'Oletko tehnyt laskarit???', reply_markup=reply_markup)

def clearJobs(chat_data):
    if 'job' in chat_data:
        job = chat_data['job']
        job.schedule_removal()
        del chat_data['job']

def button(bot, update, chat_data, job_queue):
    query = update.callback_query
    logger.info('v ' + str(query.data))
    if query.data == '1':
        bot.send_message(text='Hyvä!', chat_id=query.message.chat_id,)
        clearJobs(chat_data)
    else:
        bot.send_message(chat_id=query.message.chat_id, text=':(')
        job = job_queue.run_once(kysyLaskarit, 10*60, context=query.message.chat_id)
        clearJobs(chat_data)
        chat_data['job'] = job
    


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    updater.dispatcher.add_handler(CommandHandler('aloita', start, 
                                  pass_job_queue=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(button,
                                  pass_job_queue=True, pass_chat_data=True))
    updater.dispatcher.add_handler(CommandHandler('apua', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()