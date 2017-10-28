# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .managers import PostManager, CommentManager, LikeManager


class Post(models.Model):
    """
    model to store blog post details
    """
    post = models.CharField(_("Post message"), max_length=500)
    created_by = models.ForeignKey(User, related_name=_("post_author"))
    created_at = models.DateTimeField(_("Post Creation at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Post Updated at"), auto_now=True)
    delete = models.BooleanField(default=False)

    objects = PostManager()

    class Meta:
        app_label = "posts"
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __unicode__(self):
        return "%s" % (self.message)


class Comment(models.Model):
    """
    model to store comment for blog post details
    """
    post = models.ForeignKey(Post, related_name=_("post_comment"))
    comment = models.CharField(_("Comment message"), max_length=500)
    created_by = models.ForeignKey(User, related_name=_("comment_author"))
    created_at = models.DateTimeField(_("Comment Creation at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Comment Updated at"), auto_now=True)
    delete = models.BooleanField(default=False)

    objects = CommentManager()

    class Meta:
        app_label = "posts"
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __unicode__(self):
        return "%s" % (self.message)


class Like(models.Model):
    """
    model to store blog post details
    """
    post = models.ForeignKey(Post, related_name=_("post_like"))
    created_by = models.ForeignKey(User, related_name=_("liked_by"))
    created_at = models.DateTimeField(_("Liked At"), auto_now_add=True)

    objects = LikeManager()

    class Meta:
        app_label = "posts"
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __unicode__(self):
        return "%s" % (self.post.message)
