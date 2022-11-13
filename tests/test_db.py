import sqlite3

import pytest
from kgweb.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        print("xxx")
        assert db is get_db()

    phone = '17688888888'
    user = db.execute(
            'SELECT * FROM user WHERE phone = ?', (phone)
        ).fetchone()
    print(user)

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)