import unittest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

class TestMagazine(unittest.TestCase):
    def setUp(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executescript("""
            DELETE FROM articles;
            DELETE FROM authors;
            DELETE FROM magazines;

            INSERT INTO authors (name) VALUES ('Alice'), ('Bob');
            INSERT INTO magazines (name, category) VALUES ('Tech Today', 'Tech'), ('Nature World', 'Science');
        """)
        conn.commit()
        conn.close()

    def test_with_multiple_authors(self):
        Article(title="A", author_id=1, magazine_id=1).save()
        Article(title="B", author_id=2, magazine_id=1).save()
        mags = Magazine.with_multiple_authors()
        self.assertEqual(len(mags), 1)
        self.assertEqual(mags[0].name, "Tech Today")

    def test_article_counts(self):
        Article(title="One", author_id=1, magazine_id=1).save()
        Article(title="Two", author_id=1, magazine_id=2).save()
        counts = Magazine.article_counts()
        self.assertEqual(counts[0]["article_count"], 1)
        self.assertEqual(counts[1]["article_count"], 1)

if __name__ == "__main__":
    unittest.main()
