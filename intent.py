import requests
import environs
from pprint import pprint
import google.cloud.dialogflow_v2 as dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[message_texts])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))

if __name__ == '__main__':
    env = environs.Env()
    env.read_env()

    project_id = env.str("PROJECT_ID")
    GOOGLE_APPLICATION_CREDENTIALS = env.str("GOOGLE_APPLICATION_CREDENTIALS")
    url = "https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json"
    response = requests.get(url)
    response.raise_for_status()
    response_params = response.json()

    display_name = 'Устройство на работу'
    answer = response_params[display_name]['answer']
    questions = response_params[display_name]['questions']
    create_intent(
        project_id=project_id,
        display_name=display_name,
        training_phrases_parts=questions,
        message_texts=answer)
