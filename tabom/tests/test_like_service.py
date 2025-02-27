from django.test import TestCase

from tabom.models import Article, User
from tabom.services.like_service import do_like


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
