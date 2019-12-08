from django.db import models
from db.base_model import BaseModel


# Create your models here.


class Question(BaseModel):
    content = models.CharField(max_length=3500, verbose_name="题目内容", null=True, blank=True)
    answer = models.CharField(max_length=1000, verbose_name="题目答案", null=True, blank=True)
    picture_path = models.CharField(max_length=100, verbose_name="题目图片存储路径", null=True, blank=True)
    grade = models.CharField(max_length=20, verbose_name="年级")
    subject = models.CharField(max_length=20, verbose_name="科目", null=True, blank=True)
    type = models.CharField(max_length=20, verbose_name="类型", null=True, blank=True)
    workbook = models.ForeignKey("workbook.Workbook", null=True, blank=True)
    workbook_chapter = models.ForeignKey("workbook.WorkbookChapter", null=True, blank=True)

    class Meta:
        db_table = "question"
        verbose_name = "题目"
        verbose_name_plural = verbose_name


class SubImage(BaseModel):
    question = models.ForeignKey("Question", verbose_name="题目id")
    sub_image_path = models.CharField(max_length=100, verbose_name="小题图片路径")

    class Meta:
        db_table = "sub_image"
        verbose_name = "小题图片"
        verbose_name_plural = verbose_name


class UserQuestionImage(BaseModel):
    '''用户长传的问题图片'''
    user = models.ForeignKey("user.User", null=True, blank=True)
    question = models.ForeignKey("Question", null=True, blank=True)
    user_question_image_path = models.ImageField(upload_to="user_question_image")

    class Meta:
        db_table = "user_question_image"
        verbose_name = "用户上传的题目图片"
        verbose_name_plural = "用户上传的题目图片"
