from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from tabom.models import Article, User
from tabom.services.article_service import get_an_article, get_article_list
from tabom.services.like_service import do_like


class TestArticleService(TestCase):
    def test_you_can_get_an_articel_by_id(self) -> None:
        # Given
        title = "test_title"
        article = Article.objects.create(title=title)

        # When
        result_article = get_an_article(article.id)

        # Then
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_exception_when_article_does_not_exit(self) -> None:
        # Given
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(Article.DoesNotExist) as e:
            get_an_article(invalid_article_id)

        # Then
        self.assertEqual(str(e.exception), f"없는 article_id 입니다: {invalid_article_id}")

    def test_get_article_list_should_prefetch_like(self) -> None:
        user = User.objects.create(name="test_user")
        articles = [Article.objects.create(title=f"test_title_{i}") for i in range(1, 21)]
        do_like(user.id, articles[-1].id)

        with CaptureQueriesContext(connection) as ctx:
            # When
            result_articles = get_article_list(0, 10)
            result_counts = [a.like_set.count() for a in result_articles]

            # Then
            self.assertEqual(10, len(result_articles))
            self.assertEqual(1, result_counts[0])
            self.assertEqual([a.id for a in reversed(articles[10:21])], [a.id for a in result_articles])
