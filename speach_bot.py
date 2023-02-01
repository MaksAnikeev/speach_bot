import logging
from textwrap import dedent

import environs
from dialogflow_functions import detect_intent_texts, logging_config
from telegram import ForceReply
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from functools import partial


logger = logging.getLogger(__name__)


def start(update, context):
    user = update.effective_user

    greetings = dedent(fr'''
            Приветствую {user.mention_markdown_v2()}\!
            Давайте поздороваемся\.''')

    update.message.reply_markdown_v2(
        greetings,
        reply_markup=ForceReply(selective=True),
    )


def reply_message(update, context, project_id):
    answer = detect_intent_texts(
        f'tg-{update.message.chat_id}', update.message.text, 'ru', project_id=project_id)
    logger.info(
        f"message:{update.message.text}, answered: {answer}")
    update.message.reply_text(answer)


def error(update, context):
    update.message.reply_text('an error occured')


if __name__ == '__main__':

    logging_config()

    env = environs.Env()
    env.read_env()

    telegram_bot_token = env.str("TG_BOT_TOKEN")
    project_id = env.str("PROJECT_ID")

    updater = Updater(telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                          partial(reply_message, project_id=project_id)))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()
