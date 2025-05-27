import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Setup
author = Author("Slatt Genius")
author.save()

magazine = Magazine("Tech Pulse", "Technology")
magazine.save()

# Create and save an article
article = Article("AI Takes Over", author.id, magazine.id)
article.save()
print("Saved Article:", article)

# Fetch the article and print related author and magazine
fetched_article = Article.find_by_id(article.id)
print("Fetched Article:", fetched_article)
print("Author:", fetched_article.author())
print("Magazine:", fetched_article.magazine())
