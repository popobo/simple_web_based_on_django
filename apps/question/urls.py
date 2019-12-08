from django.conf.urls import url
from apps.question.views import IndexView, IndexQuestionsView, WorkbookView, ChapterView, QuestionView, \
    IndexQuestionImageView, UploadUserQuestionImageHandleView, QuestionAnswerView, QuestionCollectView

urlpatterns = [
    url(r"^index$", IndexView.as_view(), name="index"),
    url(r"^index_question$", IndexQuestionsView.as_view(), name="index_question"),
    url(r"^index_question_image$", IndexQuestionImageView.as_view(), name="upload_user_question_image"),
    url(r"^upload_user_question_image_handle$", UploadUserQuestionImageHandleView.as_view(),
        name="upload_user_question_image_handle"),
    url(r"^workbook/(?P<grade>\d+)/(?P<subject>\d+)/(?P<term>\d+)$", WorkbookView.as_view(), name="workbook"),
    url(r"^chapter/(?P<workbook_name>.*)$", ChapterView.as_view(), name="chapter"),
    url(r"^questions/(?P<workbook_name>.*)/(?P<chapter_index>.*)$", QuestionView.as_view(), name="question"),
    url(r"^question_answer/(?P<question_id>\d*)$", QuestionAnswerView.as_view(), name="question_answer"),
    url(r"^question_collect/(?P<question_id>\d*)$", QuestionCollectView.as_view(), name="question_collect"),
]
