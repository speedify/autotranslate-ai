import unittest
import json
from copy import deepcopy
from unittest.mock import patch
import os
from translator import (
    load_json_app_file, load_translation_table,
    store_translation_table_to_file, store_translated_text_to_file
)

class TestTranslation(unittest.TestCase):
    def setUp(self):
        self.target_language = 'es'
        self.source = 'json'
        self.translation_table = load_translation_table(self.source)
        self.copy_translation_table = deepcopy(self.translation_table)
        self.data = {}
        self.translated_app_table = {}

    
    def tearDown(self):
        if os.path.exists('test_file_1.json'):
            os.remove('test_file_1.json')

    def test_load_app_file_existing_file(self):
        with open('test_file_1.json', 'w') as f:
            json.dump(self.data, f)
        result = load_json_app_file('es', self.source)
        self.assertEqual(result, self.data)

    def test_load_app_file_non_existing_file(self):
        result = load_json_app_file('es', self.source)
        self.assertEqual(result, {})

    def test_load_translation_table_existing_file(self):
        with open('translation_table_json.json', 'w') as f:
            json.dump(self.translation_table, f)
        result = load_translation_table(self.source)
        self.assertEqual(result, self.translation_table)

    def test_load_translation_table_non_existing_file(self):
        result = load_translation_table('test')
        self.assertEqual(result, {})

    def test_store_translation_table_to_file(self):
        store_translation_table_to_file(self.copy_translation_table, self.source)
        self.assertTrue(os.path.exists('translation_table_json.json'))
        with open('translation_table_json.json') as f:
            result = json.load(f)
        self.assertEqual(result, self.copy_translation_table)

    @patch('translator.translate_text')
    def test_store_translated_text_to_file(self, mock_translate_text):
        mock_translate_text.return_value = 'translated_text'
        translated_app_table = {
            'text1': 'translated_text',
            'text2': 'translated_text'
        }
        store_translated_text_to_file('test_file_1.json', translated_app_table, self.source)
        self.assertTrue(os.path.exists('test_file_1.json'))
        with open('test_file_1.json') as f:
            result = json.load(f)
        self.assertEqual(result, translated_app_table)

if __name__ == '__main__':
    unittest.main()