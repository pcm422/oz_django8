from django.core.exceptions import BadRequest
from django.db import IntegrityError

from tabom.models import Like


def do_like(user_id: int, article_id: int) -> Like:
    try:
        return Like.objects.create(user_id=user_id, article_id=article_id)
    except IntegrityError as e:
        if "FOREIGN KEY (`user_id`)" in e.args[1]:
            raise BadRequest(f"없는 user_id 입니다: {user_id}")
        if "FOREIGN KEY (`article_id`)" in e.args[1]:
            raise BadRequest(f"없는 article_id 입니다: {article_id}")
        # if "중복에 의한 integrity error 검사" in e.args[1]:
        #     raise BadRequest(f"이미 좋아요 하셨습니다.")
        raise
