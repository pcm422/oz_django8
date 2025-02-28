from django.core.exceptions import BadRequest
from django.db import IntegrityError
from django.test import TestCase

from tabom.models import Article, Like, User
from tabom.services.like_service import do_like, undo_like


class TestLikeService(TestCase):
    def test_a_user_can_like_an_article(self) -> None:
        # Given - 테스트에 필요한 재료를 준비
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # When - 실제 테스트 대상이 되는 동작을 실행합니다
        like = do_like(user.id, article.id)

        # then - 동작을 마친후에 결과가 "예상한 대로" 나왔는지 검증합니다
        self.assertIsNotNone(like.id)
        self.assertEqual(user.id, like.user_id)
        self.assertEqual(article.id, like.article_id)

    def test_a_user_can_like_an_article_only_once(self) -> None:
        # Given - 테스트에 필요한 재료를 준비
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # Expect
        like1 = do_like(user.id, article.id)
        with self.assertRaises(IntegrityError):
            like2 = do_like(user.id, article.id)

    def test_it_should_raise_exception_when_like_an_user_does_not_exist(
        self,
    ) -> None:
        # Given
        invalid_user_id = 9988
        article = Article.objects.create(title="test_title")

        # Expect
        with self.assertRaises(BadRequest) as e:
            do_like(invalid_user_id, article.id)

        self.assertEqual(str(e.exception), "없는 user_id 입니다: 9988")

    def test_it_should_raise_exception_when_like_an_article_does_not_exist(
        self,
    ) -> None:
        # Given
        user = User.objects.create(name="test")
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(BadRequest) as e:
            do_like(user.id, invalid_article_id)

        self.assertEqual(str(e.exception), "없는 article_id 입니다: 9988")

    def test_like_count_should_increase(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # When
        do_like(user.id, article.id)

        # Then
        article = Article.objects.get(id=article.id)
        self.assertEqual(1, article.like_set.count())

    def test_a_user_can_undo_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")
        like = Like.objects.create(user_id=user.id, article_id=article.id)

        # When
        with self.assertNumQueries(1):
            undo_like(user.id, article.id)

        # Then
        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(id=like.id)
