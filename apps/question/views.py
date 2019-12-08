from django.shortcuts import render
from django.views.generic import View
from apps.workbook.models import Workbook, WorkbookChapter
from apps.question.models import Question, UserQuestionImage
from apps.user.models import UserFavorite
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import requests


# Create your views here.

class IndexView(View):
    def get(self, request):
        lastest_questions = Question.objects.all().order_by("-create_time")
        lastest_questions = lastest_questions[0:6]
        return render(request, "index.html", {"lastest_questions": lastest_questions})

    def post(self):
        pass


class IndexQuestionsView(View):

    def get(self, request):
        workbooks = Workbook.objects.all()
        return render(request, "index_question.html", {"workbooks": workbooks})


class WorkbookView(View):

    def get(self, request, grade, subject, term):
        grade = int(grade)
        grade += int(term) * 0.25
        subject = int(subject)
        # 遍历workbooks并拼接json数据：id workbook_name
        grade_dict = {0: "一年级", 0.25: "一年级上", 0.50: "一年级下",
                      1: "二年级", 1.25: "二年级上", 1.50: "二年级下",
                      2: "三年级", 2.25: "三年级上", 2.50: "三年级下",
                      3: "四年级", 3.25: "四年级上", 3.50: "四年级下",
                      4: "五年级", 4.25: "五年级上", 4.50: "五年级下",
                      5: "六年级", 5.25: "六年级上", 5.50: "六年级下",
                      6: "七年级", 6.25: "七年级上", 6.50: "七年级下",
                      7: "八年级", 7.25: "八年级上", 7.50: "八年级下",
                      8: "九年级", 8.25: "九年级上", 8.50: "九年级下",
                      9: "九年级", 9.25: "十年级上", 9.50: "十年级下",
                      10: "十一年级", 10.25: "十一年级上", 10.50: "十一年级下",
                      11: "十二年级", 11.25: "十二级上", 11.50: "十二年级下"}
        subject_dict = {0: "语文", 1: "数学", 2: "英语", 3: "物理", 4: "化学", 5: "生物", 6: "地理", 7: "历史", 8: "政治", }
        grade_name = grade_dict[grade]
        subject_name = subject_dict[subject]
        workbook_list = []
        if grade % 1 == 0:
            grade_name = grade_dict[grade + 0.25]
            workbooks = Workbook.objects.filter(subject=subject_name, grade=grade_name)
            if workbooks:
                for workbook in workbooks:
                    workbook_list.append((workbook.id, workbook.workbook_name))
            grade_name = grade_dict[grade + 0.50]
            workbooks = Workbook.objects.filter(subject=subject_name, grade=grade_name)
            if workbooks:
                for workbook in workbooks:
                    workbook_list.append((workbook.id, workbook.workbook_name))
        else:
            workbooks = Workbook.objects.filter(subject=subject_name, grade=grade_name)

            if workbooks:
                for workbook in workbooks:
                    workbook_list.append((workbook.id, workbook.workbook_name))

        return JsonResponse({"workbooks": workbook_list})


class ChapterView(View):

    def get(self, request, workbook_name):
        workbook = Workbook.objects.get(workbook_name=workbook_name)
        chapters = WorkbookChapter.objects.filter(workbook=workbook.id)
        chapter_list = []
        if chapters:
            for chapter in chapters:
                chapter_list.append((chapter.id, chapter.workbook_chapter_name))
        return JsonResponse({"chapters": chapter_list})


class QuestionView(View):

    def get(self, request, workbook_name, chapter_index):
        chapter_index = int(chapter_index)
        workbook = Workbook.objects.get(workbook_name=workbook_name)
        chapters = WorkbookChapter.objects.filter(workbook=workbook.id)
        chapter = chapters[chapter_index]
        questions = Question.objects.filter(workbook=workbook.id, workbook_chapter=chapter.id)
        question_list = []
        if questions:
            for question in questions:
                question_list.append((question.id, question.content))

        user_favorites = UserFavorite.objects.filter(user=request.user.id)
        user_favorite_list = []
        if user_favorites:
            for user_favorite in user_favorites:
                user_favorite_list.append((user_favorite.id, user_favorite.question_id))

        return JsonResponse({"questions": question_list, "user_favorites": user_favorite_list})


class IndexQuestionImageView(View):

    def get(self, request):
        return render(request, "index_question_image.html")


class UploadUserQuestionImageHandleView(View):
    def post(self, request):
        img = request.FILES.get("img")
        save_path = "%s/user_question_image/%s" % (settings.MEDIA_ROOT, img.name)
        with open(save_path, "wb") as file:
            for content in img.chunks():
                file.write(content)
        UserQuestionImage.objects.create(user_question_image_path="user_question_image")
        image_complete_path = "http://121.192.164.197:8888/static/media/user_question_image/%s" % (img.name)
        print(image_complete_path)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }
        ocr_url = "http://localhost:9201/?type=2&imgUrl=%s&isSave=0" % (image_complete_path)
        response = requests.get(ocr_url, timeout=20, headers=headers)
        response = response.json()
        match_answer = response["match_answer"]
        result_str = response["result_str"]
        match_id = response["match_ID"]
        match_result = response["result"]
        json_dict = {"match_answer": match_answer, "result_str": result_str, "match_id": match_id,
                     "match_result": match_result}
        return JsonResponse(json_dict)


class QuestionAnswerView(View):

    def get(self, request, question_id):
        question_id = int(question_id)
        question = Question.objects.get(id=question_id)
        question_answer = question.answer
        answer_list = []
        if question_answer:
            answer_list.append((question_id, question_answer))
        else:
            question_answer = "题目" + str(question_id) + "暂无解析"
            answer_list.append((question_id, question_answer))
        return JsonResponse({"question_answer": answer_list})


class QuestionCollectView(View):

    def get(self, request, question_id):
        question_id = int(question_id)
        user = request.user
        user_favorite = UserFavorite.objects.filter(question=question_id, user=user.id)
        if not user_favorite:
            user_favorite = UserFavorite()
            user_favorite.question_id = question_id
            user_favorite.user_id = user.id
            user_favorite.save()
        return HttpResponse("ok")
