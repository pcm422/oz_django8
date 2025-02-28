from django.db.models import QuerySet

from tabom.models import Article


def get_an_article(article_id: int) -> Article:
    try:
        return Article.objects.get(id=article_id)
    except Article.DoesNotExist as e:
        if "Article matching query does not exist" in e.args[0]:
            print(e.args[0])
            raise Article.DoesNotExist(f"없는 article_id 입니다: {article_id}")

        raise


def get_article_list(offset: int, limit: int) -> QuerySet[Article]:
    return Article.objects.order_by("-id").prefetch_related("like_set")[offset : offset + limit]
