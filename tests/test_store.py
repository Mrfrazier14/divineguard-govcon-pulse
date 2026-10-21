import tempfile
import unittest
from pathlib import Path
from pulse.store import Store

class StoreTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(':memory:')
        self.addCleanup(self.store.close)

    def test_default_imported(self):
        self.store.add("Example ' quoted", 'https://sam.gov/example')
        self.assertEqual(self.store.list()[0]['stage'], 'Imported')

    def test_reject_invalid_source(self):
        for url in ('http://sam.gov', 'javascript:alert(1)', 'https://key:secret@sam.gov'):
            with self.assertRaises(ValueError):
                self.store.add('Example', url)

    def test_claim_requires_evidence(self):
        key = self.store.add('Example', 'https://sam.gov/example')
        with self.assertRaises(ValueError):
            self.store.update_stage(key, 'Awarded')
        self.assertEqual(self.store.list()[0]['stage'], 'Imported')
        self.store.update_stage(key, 'Awarded', 'https://sam.gov/evidence')
        self.assertEqual(self.store.list()[0]['evidence_url'], 'https://sam.gov/evidence')

    def test_unknown_record_and_stage(self):
        with self.assertRaises(KeyError):
            self.store.update_stage('missing', 'Watching')
        with self.assertRaises(ValueError):
            self.store.update_stage('missing', 'Won')

    def test_persistence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'nested' / 'pulse.db'
            store = Store(path)
            key = store.add('Sample', 'https://sam.gov/example')
            store.close()
            reopened = Store(path)
            try:
                self.assertEqual(reopened.list()[0]['id'], key)
            finally:
                reopened.close()
