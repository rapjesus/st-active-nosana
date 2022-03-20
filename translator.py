from bs4 import BeautifulSoup
import os
import shutil
import random

def start_work():
    project_name = input("Введите название проекта (только латинские буквы и цифры): ")
    lander_directory = input("Введите название преленда (только латинские буквы и цифры): ").replace(' ', '-')
    user_id = random.randint(1000000, 9999999)
    project_languages = input("Введите языка, на которые вы хотите перевести проект через запятую в символьном обозначении. Для того, чтобы узнать символьное обознначение языка посетите: https://cloud.google.com/translate/docs/languages?hl=en_GB: ")
    languages = project_languages.split(', ')
    return file_structure(user_id, project_name, lander_directory, languages)


def file_structure(user_id, project_name, lander_directory, languages):
    template = shutil.copytree(lander_directory, (str(user_id) + "/" + project_name + "/template"))
    # translating_directory = []
    for language in languages:
        translating_directory = shutil.copytree(template, (str(user_id) + "/" + project_name + "/" + language))
        html = open(translating_directory + "/index.html", "r")
    return get_text(languages, translating_directory)
### Функция создала структуру под работу - под переводы на все языки и скопировала все файлы прелендов, теперь нужно перевести

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    return result
    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


def get_text(languages, projects):
    clean_text = ';'.join(BeautifulSoup(source, "html.parser").stripped_strings)
    for_work = clean_text.split(";")
    translate = translating(languages, for_work, source, project_name)
    return translate


def translating(languages, what_to_tanslate, where_we_translating, project_name):
    for i in languages:
        translated_code = where_we_translating
        for x in what_to_tanslate:
            translate_item = translate_text(i, x)['translatedText']
            translated_code = translated_code.replace(x, translate_item, 1)
        create_translated_landing(translated_code, i, project_name)
    return print("well done!")


def create_translated_landing(translated_code, language, project_name):
    os.makedirs(project_name.replace(' ', '-') + '/translated-landings/' + language)
    html = open(project_name.replace(' ', '-') + '/translated-landings/' + language + "/" + "index.html", "w")
    html.write(translated_code)
    html.close()
