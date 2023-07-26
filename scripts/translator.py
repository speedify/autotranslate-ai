import os
import openai
import sys
import json
import tiktoken

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.organization = os.environ["OPENAI_ORG_ID"]
enc = tiktoken.encoding_for_model("gpt-4")


def load_json_app_file(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) != 0:
        with open(file_path) as f:
            return json.load(f)
    else:
        return {}


def define_source_file():
    if len(sys.argv) < 2:
        print(
            "Please provide a source file and an output directory (and an optional language dictionary) as command-line arguments."
        )
        sys.exit(1)
    elif len(sys.argv) < 3:
        print(
            "Please add an output directory (and an optional language dictionary) as a command-line argument."
        )
        sys.exit(1)
    else:
        with open(sys.argv[1]) as f:
            return json.load(f)


# Supported Language Codes
# ar-SA, ca, cs, da, de-DE, el, en-AU, en-CA, en-GB, en-US, es-ES, es-MX, fi, fr-CA, fr-FR, he, hi, hr, hu, id, it, ja, ko, ms, nl-NL, no, pl, pt-BR, pt-PT, ro, ru, sk, sv, th, tr, uk, vi, zh-Hans, zh-Hant
def get_languages():
    try:
        with open(sys.argv[3]) as f:
            return json.load(f)
    except:
        # Default dictionary that is used if one is not specified in the command line
        return {
            "en": "US",
            "ar": "SA",  # Arabic (Saudi Arabia)
            "de": "DE",  # German (Germany)
            "es": "MX",  # Spanish (Mexico)
            "fr": "FR",  # French (France)
            "pt": "BR",  # Portuguese (Brazil)
            "ro": "RO",  # Romanian (Romania)
            "ru": "RU",  # Russian (Russia)
            "tr": "TR",  # Turkish (Turkey)
            "ko": "KR",  # Korean (South Korea)
            "ja": "JP",  # Japanese (Japan)
            "pl": "PL",  # Polish (Poland)
            "it": "IT",  # Italian (Italy)
        }


def load_translation_table(source):
    if (
        os.path.exists("translation_table_{}.json".format(source))
        and os.path.getsize("translation_table_{}.json".format(source)) != 0
    ):
        with open("translation_table_{}.json".format(source)) as f:
            return json.load(f)
    else:
        return {}


def store_translation_table_to_file(translation_table, source):
    with open("translation_table_{}.json".format(source), "w+") as f:
        json.dump(translation_table, f, indent=4, ensure_ascii=False)


def store_translated_text_to_file(dest_filepath, translated_app_table, source):
    if source == "json":
        with open(dest_filepath, "w", encoding="utf-8") as f:
            json.dump(translated_app_table, f, indent=2, ensure_ascii=False)
    # Otherwise, treat as a txt file
    else:
        with open(dest_filepath, "w", encoding="utf-8") as f:
            f.write(translated_app_table)


def add_to_context(context_table: dict, target_language, translated_text, text):
    if len(context_table[target_language]) == 10:
        context_table[target_language].pop(next(iter(context_table[target_language])))

    if len(enc.encode(translated_text)) < 300 and len(enc.encode(translated_text)) > 50:
        context_table[target_language][text] = translated_text

    with open("context.json", "w+", encoding="utf-8") as f:
        json.dump(context_table, f, indent=4, ensure_ascii=False)


def translate_text(text, target_language, source, is_keyword=False):
    # Check if the translation exists in the cache
    translation_table = load_translation_table(source)

    context_table = load_json_app_file("context.json")
    english_context = ""
    lang_context = ""

    if target_language not in context_table:
        context_table[target_language] = {}
        context = False
    else:
        context = True
        for key in context_table[target_language]:
            english_context = key + english_context
            lang_context = context_table[target_language][key] + lang_context

    if text in translation_table and target_language in translation_table[text]:
        translated_text = translation_table.get(text, {}).get(target_language)
        add_to_context(context_table, target_language, translated_text, text)
        return translated_text

    text_to_translate = text

    if source == "json":
        user_content = "Keep the JSON format. Do not include the english that is being translated or any notes. Only include the translated text. Make sure there are the same amount of open brackets as closed brackets. Translate the following text from English to {}: \n{}".format(
            target_language, text_to_translate
        )
    else:
        user_content = "Translate the following text from English to {}: \n{}".format(
            target_language, text_to_translate
        )

    if is_keyword:
        user_content = "Do not expand upon any acronyms. Translate the following keyword from English to {}: \n{}".format(
            target_language, text_to_translate
        )

    if context == True:
        msg = [
            {
                "role": "system",
                "content": "You are a helpful assistant that translates English text to other languages. This is the en example: {} \n This is the {} example: {}".format(
                    english_context, target_language, lang_context
                ),
            },
            {"role": "user", "content": user_content},
        ]
    else:
        msg = [
            {
                "role": "system",
                "content": "You are a helpful assistant that translates English text to other languages.",
            },
            {"role": "user", "content": user_content},
        ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=msg,
        temperature=0.3,
        n=1,
        stop=None,
    )

    # Extract the assistant's response
    full_response = response.choices[0].message.content.strip()

    # Remove the initial prompt from the translated text
    translated_text = full_response[full_response.find("\n") + 1 :]

    if text in translation_table and target_language not in translation_table[text]:
        try:
            translation_table[text][target_language] = translated_text
        except:
            print("Failed to update the translation table")
        store_translation_table_to_file(translation_table, source)

    # Check for a new key here...
    if (text) not in translation_table:
        translation_table[text] = {}
        translation_table[text][target_language] = translated_text
        store_translation_table_to_file(translation_table, source)
        add_to_context(context_table, target_language, translated_text, text)

    return translated_text


sources = ["json", "txt"]
