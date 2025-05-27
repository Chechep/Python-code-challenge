from lib.db.connection import get_connection
from lib.models.article import Article  # We'll create this file next

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"])
        return None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"]) for row in rows]

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"

    def articles(self):
        from lib.models.article import Article  # Delayed import to avoid circular dependency
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"]) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(id=row["id"], name=row["name"], category=row["category"]) for row in rows]

# Find all authors who have written for a specific magazine
def authors_for_magazine(magazine_id):
    from lib.models.author import Author
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT au.* FROM authors au
        JOIN articles a ON au.id = a.author_id
        WHERE a.magazine_id = ?
    """, (magazine_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Author(id=row["id"], name=row["name"]) for row in rows]

# Find magazines with articles by at least 2 different authors
def magazines_with_multiple_authors():
    from lib.models.magazine import Magazine
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, COUNT(DISTINCT a.author_id) as author_count
        FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
        HAVING author_count >= 2
    """)
    rows = cursor.fetchall()
    conn.close()
    return [Magazine(id=row["id"], name=row["name"], category=row["category"]) for row in rows]

# Count the number of articles in each magazine
def article_counts_per_magazine():
    from lib.models.magazine import Magazine
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, COUNT(a.id) as article_count
        FROM magazines m
        LEFT JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [(Magazine(id=row["id"], name=row["name"], category=row["category"]), row["article_count"]) for row in rows]

# Find the author who has written the most articles
def top_author():
    from lib.models.author import Author
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT au.*, COUNT(a.id) as article_count FROM authors au
        JOIN articles a ON au.id = a.author_id
        GROUP BY au.id
        ORDER BY article_count DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        return Author(id=row["id"], name=row["name"])
    return None
@classmethod
def for_magazine(cls, magazine_id):
    from lib.db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT au.*
        FROM authors au
        JOIN articles a ON au.id = a.author_id
        WHERE a.magazine_id = ?
    """, (magazine_id,))
    rows = cursor.fetchall()
    conn.close()
    return [cls(id=row["id"], name=row["name"]) for row in rows]
@classmethod
def top_author(cls):
    from lib.db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT au.*, COUNT(a.id) AS article_count
        FROM authors au
        JOIN articles a ON au.id = a.author_id
        GROUP BY au.id
        ORDER BY article_count DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        return cls(id=row["id"], name=row["name"])
    return None
