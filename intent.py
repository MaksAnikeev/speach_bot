import argparse
import environs
import google.cloud.dialogflow_v2 as dialogflow
import requests
import json


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
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()

    parser = argparse.ArgumentParser()
    parser.add_argument('--url',
                        help='url адрес без кавычек https://dvmn.org/media/fil....:')
    parser.add_argument('intent',
                        type=str,
                        help='название намерения в кавычках или если хотите скачать все намерения из файла напишите "all"')
    parser.add_argument('--json',
                        help='адрес в кавычках где лежит файл .json D:/my_docyments.... '
                             'или просто название файла .json в кавычках, если он лежит в папке с кодом (без расширения)')
    args = parser.parse_args()

    project_id = env.str("PROJECT_ID")

    if args.url:
        response = requests.get(args.url)
        response.raise_for_status()
        intent_params = response.json()

    elif args.json:
        with open(f'{args.json}.json', "r", encoding="utf-8") as intent_file:
            intent_params = json.load(intent_file)
    else:
        print('Необходимо ввести либо --url, либо --json, введите -h, для просмотра справки')

    if not args.intent == 'all':
        display_name = args.intent
        answer = intent_params[display_name]['answer']
        questions = intent_params[display_name]['questions']
        intent_params = {
            display_name: {
                "questions": questions,
                "answer": answer
            }
        }

    if args.json or args.url:
        for display_name in intent_params:
            answer = intent_params[display_name]['answer']
            questions = intent_params[display_name]['questions']
            create_intent(
                project_id=project_id,
                display_name=display_name,
                training_phrases_parts=questions,
                message_texts=answer)
        print('Намерения успешно созданы')
