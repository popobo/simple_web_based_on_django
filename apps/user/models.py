from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


# Create your models here.


class User(AbstractUser, BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class UserFavorite(BaseModel):
    user = models.ForeignKey("user.User")
    question = models.ForeignKey("question.Question")
    class Meta:
        db_table = "user_favorite"
        verbose_name = "收藏夹"
        verbose_name_plural = verbose_name
