import logging
from textwrap import dedent

import environs
import google.cloud.dialogflow_v2 as dialogflow
from telegram import ForceReply
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


def detect_intent_texts(session_id, text, language_code, project_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    fallback = response.query_result.intent.is_fallback
    answer = response.query_result.fulfillment_text

    return answer, fallback


def logging_config():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )