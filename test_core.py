import unittest, tempfile, json, sqlite3, copy
from pathlib import Path
import app as c

class CoreTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'test.sqlite'
        self.config = json.loads((Path(__file__).resolve().parent / 'scenario.json').read_text(encoding='utf-8'))

    def test_same(self):
        self.assertEqual(c.compare({'type': 'string'}, {'type': 'string'}), [])

    def test_request_narrow(self):
        self.assertTrue(c.compare({'type': 'string', 'enum': ['a', 'b']}, {'type': 'string', 'enum': ['a']})[0]['breaking'])

    def test_response_expand(self):
        self.assertTrue(c.compare({'type': 'string', 'enum': ['a']}, {'type': 'string', 'enum': ['a', 'b']}, 'response')[0]['breaking'])

    def test_response_unbounded(self):
        self.assertTrue(c.compare({'type': 'string', 'enum': ['a']}, {'type': 'string'}, 'response')[0]['breaking'])

    def test_unknown_review(self):
        self.assertIsNone(c.compare({'type': 'string'}, {'type': 'string', 'pattern': 'a'})[0]['breaking'])

    def test_direction(self):
        with self.assertRaises(ValueError):
            c.compare({}, {}, 'other')

    def test_nested_array(self):
        old = {'type': 'array', 'items': {'type': 'number'}}
        new = {'type': 'array', 'items': {'type': 'string'}}
        self.assertEqual(c.compare(old, new)[0]['path'], '$[]')

    def test_request_enum_expansion(self):
        self.assertFalse(c.compare({'type': 'string', 'enum': ['a']}, {'type': 'string', 'enum': ['a', 'b']})[0]['breaking'])
if __name__ == '__main__':
    unittest.main()
