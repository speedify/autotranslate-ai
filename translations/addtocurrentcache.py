import sys
import os
import tiktoken
import json
from translator import (
    load_json_app_file,
    load_translation_table,
    store_translation_table_to_file,
    get_languages,
)


def populate_table(source_data, lang_data, lang: str):
    for key in source_data:
        if key not in lang_data:
            continue
        if isinstance(source_data[key], dict) and isinstance(lang_data[key], dict):
            populate_table(source_data[key], lang_data[key], lang)
        else:
            if (
                source_data[key] in translation_table
                and lang not in translation_table[source_data[key]]
            ):
                translation_table[source_data[key]][lang] = lang_data[key]
            if (source_data[key]) not in translation_table:
                translation_table[source_data[key]] = {}
                translation_table[source_data[key]][lang] = lang_data[key]


source = "json"

if len(sys.argv) < 2:
    print(
        "Please provide a source directory and a source english file as a command-line argument."
    )
    sys.exit(1)
elif len(sys.argv) < 3:
    print("Please provide a source english file as a command-line argument.")
    sys.exit(1)
else:
    folder_path = sys.argv[1]
    english_file = sys.argv[2]
source_path = os.path.join(folder_path, english_file)
source_table = load_json_app_file(source_path)

enc = tiktoken.encoding_for_model("gpt-4")

translation_table = load_translation_table(source)

languages = get_languages()
for language, country_code in languages.items():
    if language == "en":
        continue
    lang_path = os.path.join(folder_path, "{}.json".format(language))
    lang_data = load_json_app_file(lang_path)
    if len(lang_data) == 0:
        print("{} not detected".format(language))
        continue
    for key in source_table:
        if key not in lang_data:
            continue
        else:
            temp_text = ""
            if isinstance(source_table[key], str):
                temp_text = source_table[key]
            else:
                temp_text = json.dumps(source_table[key], ensure_ascii=False)
            if len(enc.encode(temp_text)) > 5000:
                populate_table(source_table[key], lang_data[key], language)
            else:
                if (
                    temp_text in translation_table
                    and language not in translation_table[temp_text]
                ):
                    translation_table[temp_text][language] = json.dumps(
                        lang_data[key], ensure_ascii=False
                    )
                if (temp_text) not in translation_table:
                    translation_table[temp_text] = {}
                    translation_table[temp_text][language] = json.dumps(
                        lang_data[key], ensure_ascii=False
                    )
store_translation_table_to_file(translation_table, source)
