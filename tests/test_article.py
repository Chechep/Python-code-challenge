import unittest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

class TestArticle(unittest.TestCase):
    def setUp(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executescript("""
            DELETE FROM articles;
            DELETE FROM authors;
            DELETE FROM magazines;

            INSERT INTO authors (name) VALUES ('Alice');
            INSERT INTO magazines (name, category) VALUES ('Tech Today', 'Tech');
        """)
        conn.commit()
        conn.close()

    def test_save_and_find_by_id(self):
        article = Article(title="AI", author_id=1, magazine_id=1)
        article.save()
        found = Article.find_by_id(article.id)
        self.assertEqual(found.title, "AI")

    def test_relationships(self):
        article = Article(title="ML", author_id=1, magazine_id=1)
        article.save()
        self.assertEqual(article.author().name, "Alice")
        self.assertEqual(article.magazine().name, "Tech Today")

if __name__ == "__main__":
    unittest.main()
