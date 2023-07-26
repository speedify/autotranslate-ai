import json


def mock_translate_text(s, language_code, format):
    return "translation of " + s + " to " + language_code + " with format " + format


def map_translations(translator, in_dict, language_code, format):
    return {
        k: map_translations(translator, v, language_code, format)
        if isinstance(v, dict)
        else translator(v, language_code, format)
        for k, v in in_dict.items()
    }


def test_map_translations():
    in_dict = {
        "key1": "value1",
        "key2": {
            "key3": "value3",
            "key4": "value4",
            "key5": {"key6": "value6", "key7": "value7"},
        },
    }
    out_dict = map_translations(
        translator=mock_translate_text,
        in_dict=in_dict,
        language_code="fr",
        format="json",
    )
    assert out_dict == {
        "key1": "translation of value1 to fr with format json",
        "key2": {
            "key3": "translation of value3 to fr with format json",
            "key4": "translation of value4 to fr with format json",
            "key5": {
                "key6": "translation of value6 to fr with format json",
                "key7": "translation of value7 to fr with format json",
            },
        },
    }


if __name__ == "__main__":
    test_map_translations()
    with open("en.json", "r") as in_file:
        in_dict = json.load(in_file)
        for language_code in ["fr", "es", "de"]:
            out_dict = map_translations(
                translator=mock_translate_text,
                in_dict=in_dict,
                language_code=language_code,
                format="json",
            )
            print(json.dumps(out_dict, indent=2))
            with open(f"{language_code}.json", "w") as out_file:
                json.dump(out_dict, out_file, indent=2)
