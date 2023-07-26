# autotranslate-ai
Created by [Adam Gizis](https://github.com/adamgizis) and [Sophia Butler](https://github.com/sophbutler)

A translator that takes an English .json or a .txt file and outputs translated files for every language listed in the language dictionary by using the OpenAI API.

## Table of Contents
- [Before You Begin](#before-you-begin)
- [JSON Translations](#json-translations)
- [TXT Translations](#txt-translations)
- [Usage](#usage)
- [Notes](#notes)

## Before You Begin
- Clone this repository to your local machine.
- Import OpenAI and make sure you have the OpenAI API Key and an Organization Key ID. You can refer to the [OpenAI documentation](https://platform.openai.com/docs/libraries) for more information.
```
pip install openai
pip install tiktoken
export OPENAI_API_KEY=[your_openai_key]
export OPENAI_ORG_ID=[your_openai_org_id]
```
OR
```
pipenv install
pipenv shell
export OPENAI_API_KEY=[your_openai_key]
export OPENAI_ORG_ID=[your_openai_org_id]
```
- Upload the files/directories you wish to translate into the 'translations' folder.

### Giving Context to OpenAI for JSON Files
Since this script translates JSON files line by line, some translations could be a little off due to a lack of context given to the OpenAI. We solved this issue by providing context, which is empty by default. If you wish to provide your own context before you start translating, you can edit the 'context.json' file. We have provided an example template of what the context file should look like in 'context_example.json'. If you leave 'context.json' empty, it will automatically populate with the first 10 translations OpenAI creates for each language. The context dictionary continuously updates as you translate more files.

## JSON Translations
- 'jsontranslator.py' takes in a .json file as input and outputs translated .json files
- Translated files will be populated in the desired output directory along with a cache file titled ‘translation_table_json.json’ in the 'translations' directory

## TXT Translations
- 'txttranslator.py' takes in a directory of .txt files as input and outputs multiple folder with translated .txt files.
- New directories titled '[\foldername\]-[\language_code\]-[\country_code\]' within the chosen output directory will be populated with translated files named after the output language and country codes along with a cache file titled ‘translation_table_appstore.json' in the 'translations' directory
- If you wish to keep some files in the source directory in English while translating the rest, you can add them to the 'exclude_files' list which is empty by default.

## Usage
To translate a .json file:
```
python3 jsontranslator.py [sourcefile] [outputdirectory]
```
To translate a .txt file:
```
python3 appstoretranslator.py [sourcedirectory] [outputdirectory]
```
The translated files will populate in the chosen output directory and the translation_tables for appstoretranslator.py and jsontranslator.py will appear in the parent directory, translations.

Here is an example of what your directory tree would look like after successfully translating a file using 'jsontranslator.py' to 12 different languages:
```
├── [outoutdirectory]
│   ├── ar-SA.json
│   ├── de-DE.json
│   ├── es-MX.json
│   ├── fr-FR.json
│   ├── it-IT.json
│   ├── ja-JP.json
│   ├── ko-KR.json
│   ├── pl-PL.json
│   ├── pt-BR.json
│   ├── ro-RO.json
│   ├── ru-RU.json
│   └── tr-TR.json
├── [filename].json
├── addtocurrentcache.py
├── context.py
├── jsontranslator_tests.py
├── jsontranslator.py
├── map_translations.py
├── translator.py
└── txttranslator.py
```
Here is an example of what your directory tree would look like after successfully translating a folder using 'txttranslator.py' to Arabic:
```
├── [sourcedirectory]
│   ├── hello_world_1.txt
│   ├── hello_world_2.txt
├── [outputdirectory]
│   ├── [sourcedirectory]-ar-SA -> new directory that is produced
│       ├── hello_world_1.txt
│       ├── hello_world_2.txt
├── addtocurrentcache.py
├── context.py
├── jsontranslator_tests.py
├── jsontranslator.py
├── map_translations.py
├── translator.py
└── txttranslator.py
```
## Notes
### Choosing Which Language to Translate To
If you only want to translate your files to a specific number of langauges other than the default 12, you can add a .json file containing a dictionary of your desired languages to the command line:
```
python3 jsontranslator.py [sourcefile] [outputdirectory] [languagedictionary]
```
OR
```
python3 txttranslator.py [sourcefile] [outputdirectory] [languagedictionary]
```
### Existing Cache/Files
If you wish to add to the cache at any point with a directory of translations, you can call 'addtocurrentcache.py' with the directory of translations and a the name of the English file in the directory to the command line:
```
python3 addtocurrentcache.py [sourcedirectory] [sourcefile]
```
If either program is run with an already existing cache or translated files, the cache will be referenced to see what has already been translated, and take the stored translation from the cache. If existing files that have names that align with the ones produced by the program have updates, the file will be updated with new translations and what is stored on the cache.
### Possible Problems with JSON Files
- For JSON formatted documents, the program is dependent on the API producing the translated output in proper dictionary format. If not, your file will not be able to be translated and you will likely get a JSONDecodeError message.
- If an object in your JSON file is too long, OpenAI will likely timeout or trunacate its answer due to exceeding the token limit. This trunacation will lead to a JSONDecodeError and your file will not be translated.
### Checking Accuracy of Translations
There is currently no check to see if the translations created by the OpenAI are completely accurate. If you want to confirm that your file is being translated correctly, it is best to perform manual checks.
### Manually Fixing Incorrect Translations
Fix the necessary changes in the cache which is named 'translation_table' in order for the changes to be fixed. This will ensure the error is fixed unless the original English file is altered.
