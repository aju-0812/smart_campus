import sqlite3

def run_migration():
    conn = sqlite3.connect('smart_campus.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN password VARCHAR NOT NULL DEFAULT 'pass123'")
        conn.commit()
        print("Migration successful")
    except Exception as e:
        print("Migration failed or already applied:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    run_migration()
