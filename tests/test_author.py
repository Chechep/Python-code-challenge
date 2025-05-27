import unittest
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

class TestAuthor(unittest.TestCase):
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

    def test_save_and_find_by_id(self):
        author = Author(name="Charlie")
        author.save()
        found = Author.find_by_id(author.id)
        self.assertEqual(found.name, "Charlie")

    def test_for_magazine(self):
        # create article with author_id=1 and magazine_id=1
        article = Article(title="AI in 2025", author_id=1, magazine_id=1)
        article.save()
        authors = Author.for_magazine(1)
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].name, "Alice")

    def test_top_author(self):
        Article(title="One", author_id=1, magazine_id=1).save()
        Article(title="Two", author_id=1, magazine_id=1).save()
        Article(title="Three", author_id=2, magazine_id=2).save()
        top = Author.top_author()
        self.assertEqual(top.name, "Alice")

if __name__ == "__main__":
    unittest.main()
