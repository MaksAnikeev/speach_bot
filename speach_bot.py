import logging
import environs
import google.cloud.dialogflow_v2 as dialogflow

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pprint import pprint
from textwrap import dedent

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

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


def reply_message(update, context):
    try:
        answer = detect_intent_texts(
            update.message.chat_id, update.message.text, 'ru')
        logger.info(
            f"message:{update.message.text}, answered: {answer}")
        update.message.reply_text(answer)
    except:
        logger.exception('detect intent not working')


def detect_intent_texts(session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    answer = response.query_result.fulfillment_text
    return answer


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()

    telegram_bot_token = env.str("TG_BOT_TOKEN")
    project_id = env.str("PROJECT_ID")
    GOOGLE_APPLICATION_CREDENTIALS = env.str("GOOGLE_APPLICATION_CREDENTIALS")

    updater = Updater(telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_message))

    updater.start_polling()
    updater.idle()
