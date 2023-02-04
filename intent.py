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

    project_id = env.str("PROJECT_ID")
    print('Выберите откуда скачивать файл с данными (.json). 1 - с сервера, 2 - с локального компьютера')
    choise_direction = int(input())
    if choise_direction == 1:
        print('Укажите url адрес без кавычек https://dvmn.org/media/fil....:')
        url = input()
        response = requests.get(url)
        response.raise_for_status()
        intent_params = response.json()

        print('Укажите название намерения без кавычек или если хотите скачать все намерения из файла напишите all')
        choise_display_name = input()
        if choise_display_name == 'all':
            for display_name, params in intent_params.items():
                answer = intent_params[display_name]['answer']
                questions = intent_params[display_name]['questions']
                create_intent(
                    project_id=project_id,
                    display_name=display_name,
                    training_phrases_parts=questions,
                    message_texts=answer)
            print('Намерения успешно созданы')
        else:
            display_name = choise_display_name
            answer = intent_params[display_name]['answer']
            questions = intent_params[display_name]['questions']
            create_intent(
                project_id=project_id,
                display_name=display_name,
                training_phrases_parts=questions,
                message_texts=answer)
            print('Намерение успешно создано')

    elif choise_direction == 2:
        print('Укажите адрес без кавычек где лежит файл .json D:/my_docyments.... '
              'или просто название файла .json, если он лежит в папке с кодом (без расширения):')
        with open(f'{input()}.json', "r", encoding="utf-8") as my_file:
            intent_params = json.load(my_file)
        print('Укажите название намерения без кавычек или если хотите скачать все намерения из файла напишите all')
        choise_display_name = input()
        if choise_display_name == 'all':
            for display_name, params in intent_params.items():
                answer = intent_params[display_name]['answer']
                questions = intent_params[display_name]['questions']
                create_intent(
                    project_id=project_id,
                    display_name=display_name,
                    training_phrases_parts=questions,
                    message_texts=answer)
            print('Намерения успешно созданы')
        else:
            display_name = choise_display_name
            answer = intent_params[display_name]['answer']
            questions = intent_params[display_name]['questions']
            create_intent(
                project_id=project_id,
                display_name=display_name,
                training_phrases_parts=questions,
                message_texts=answer)
            print('Намерение успешно создано')
    else:
        print('Вы ввели некорректную цифру. Попробуйте заново')