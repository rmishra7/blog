
from django.db import models
from django.db.models.query import QuerySet


class PostMixin(object):
    pass


class PostQuerySet(QuerySet, PostMixin):
    pass


class PostManager(models.Manager, PostMixin):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db).filter(delete=False)


class CommentMixin(object):
    pass


class CommentQuerySet(QuerySet, CommentMixin):
    pass


class CommentManager(models.Manager, CommentMixin):

    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db).filter(delete=False)


class LikeMixin(object):
    pass


class LikeQuerySet(QuerySet, LikeMixin):
    pass


class LikeManager(models.Manager, LikeMixin):

    def get_queryset(self):
        return LikeQuerySet(self.model, using=self._db)
