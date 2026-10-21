import sqlite3
from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

STAGES = ('Imported', 'Watching', 'Drafting', 'Submitted', 'Received', 'Awarded', 'Paid', 'Passed')

def source_url(value):
    parsed = urlparse(value)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('A valid HTTPS source URL without credentials is required')
    return value

class Store:
    def __init__(self, path):
        if str(path) != ':memory:':
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute('CREATE TABLE IF NOT EXISTS opportunities (id TEXT PRIMARY KEY, title TEXT NOT NULL, source_url TEXT NOT NULL, stage TEXT NOT NULL, evidence_url TEXT)')
        self.db.commit()

    def close(self):
        self.db.close()

    def add(self, title, url):
        if not isinstance(title, str) or not title.strip() or len(title) > 500:
            raise ValueError('Title must contain 1-500 characters')
        key = str(uuid4())
        with self.db:
            self.db.execute('INSERT INTO opportunities VALUES (?, ?, ?, ?, ?)', (key, title.strip(), source_url(url), 'Imported', None))
        return key

    def update_stage(self, key, stage, evidence=None):
        if stage not in STAGES:
            raise ValueError('Unknown stage')
        if stage in ('Submitted', 'Received', 'Awarded', 'Paid') and not evidence:
            raise ValueError('This stage requires an evidence link; a link is not independent verification')
        if evidence:
            source_url(evidence)
        with self.db:
            cursor = self.db.execute('UPDATE opportunities SET stage=?, evidence_url=? WHERE id=?', (stage, evidence, key))
            if cursor.rowcount != 1:
                raise KeyError(key)

    def list(self):
        return [dict(row) for row in self.db.execute('SELECT * FROM opportunities ORDER BY rowid')]
