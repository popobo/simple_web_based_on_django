from django.db import models
from db.base_model import BaseModel


# Create your models here.

class Workbook(BaseModel):
    workbook_name = models.CharField(max_length=30, verbose_name="练习册名",null=True,blank=True)
    subject = models.CharField(max_length=20, verbose_name="科目",null=True,blank=True)
    grade = models.CharField(max_length=20, verbose_name="年级",null=True,blank=True)

    class Meta:
        db_table = "workbook"
        verbose_name = "练习册"
        verbose_name_plural = verbose_name


class WorkbookChapter(BaseModel):
    workbook_chapter_name = models.CharField(max_length=100, verbose_name="章节名")
    workbook = models.ForeignKey("Workbook", verbose_name="练习册id")

    class Meta:
        db_table = "workbook_chapter"
        verbose_name = "章节"
        verbose_name_plural = verbose_name
