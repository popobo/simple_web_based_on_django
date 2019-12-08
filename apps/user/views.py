from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout

import re
from apps.user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from FifthDemo import settings
from celery_tasks.tasks import send_register_active_email
from itsdangerous import SignatureExpired
from utils.mixin import LoginRequiredMixin
from apps.user.models import UserFavorite
from apps.question.models import Question


class RegisterView(View):
    '''注册'''

    def get(self, request):
        '''显示注册页面'''
        return render(request, "register.html")

    def post(self, request):
        '''进行注册处理'''
        # 接收数据
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
        # 进行数据的校验
        if not all([username, password, email]):
            return render(request, "register.html", {"error_message": "数据不完整"})
        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(request, "register.html", {"error_message": "邮箱格式不正确"})
        if allow != "on":
            return render(request, "register.html", {"error_message": "请同意协议"})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, "register.html", {"error_message": "用户名已存在"})
        # 进行业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
        # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密
        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {"confirm": user.id}
        token = serializer.dumps(info)
        token = token.decode("utf8")
        # 发邮件
        send_register_active_email.delay(email, username, token)
        # 　返回应答
        return redirect(reverse("question:index"))


class ActiveView(View):
    '''用户激活'''

    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as error:
            # 激活链接已过期
            return HttpResponse('激活链接已过期')


class LoginView(View):
    '''登录'''

    def get(self, request):
        # 判断是否记住了用户名
        if "username" in request.COOKIES:
            username = request.COOKIES.get("username")
            checked = "checked"
        else:
            username = ""
            checked = ""
        return render(request, "login.html", {"username": username, "checked": checked})

    def post(self, request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 校验数据
        if not all([username, password]):
            return render(request, "login.html", {"error_message": "数据不完整"})

        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)

                # 获取登录后要跳转到的地址
                next_url = request.GET.get("next", reverse("question:index"))
                response = redirect(next_url)
                # 判断是否需要记住用户名
                remember = request.POST.get("remember")

                if remember == "on":
                    response.set_cookie("username", username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie("username")

                return response

            else:
                # 用户未激活
                return render(request, "login.html", {"error_message": "用户未激活"})
        else:
            # 用户名或密码错误
            return render(request, "login.html",
                          {"error_message": "用户名或密码错误", "username": username, "password": password})


class UserCenterView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        user_favorites = UserFavorite.objects.filter(user=user.id)
        user_favorite_question_list = []
        for user_favorite in user_favorites:
            question = Question.objects.get(id=user_favorite.question_id)
            user_favorite_question_list.append(question)
        return render(request, "user_center.html", {"user_favorite_questions": user_favorite_question_list})


class LoginOutView(View):
    '''退出登录'''

    def get(self, request):
        logout(request)
        return redirect("question:index")


class CancelFavoriteView(View):
    '''取消收藏'''

    def get(self, request, cancel_favorite_id):
        cancel_favorite_id = int(cancel_favorite_id)
        favorite_delete = UserFavorite.objects.get(question=cancel_favorite_id)
        favorite_delete.delete()
        print(favorite_delete.id)
        status_list = [("ok",)]
        return JsonResponse({"status_list": status_list})

    # Create your views here.

# def index(request):
#     '''首页'''
#     return render(request, "index.html")
#
#
# def register(request):
#     '''注册'''
#     if request.method == "GET":
#         return render(request, "register.html")
#     else:
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         email = request.POST.get("email")
#         allow = request.POST.get("allow")
#         # 进行数据的校验
#         if not all([username, password, email]):
#             return render(request, "register.html", {"error_message": "数据不完整"})
#         if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
#             return render(request, "register.html", {"error_message": "邮箱格式不正确"})
#         if allow != "on":
#             return render(request, "register.html", {"error_message": "请同意协议"})
#         # 校验用户名是否重复
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             user = None
#
#         if user:
#             return render(request, "register.html", {"error_message": "用户名已存在"})
#         # 进行业务处理：进行用户注册
#         user = User()
#         user.username = username
#         user.password = password
#         user.email = email
#         user.save()
#
#
#         # 　返回应答
#         return redirect(reverse("App:index"))


# def register_handle(request):
#     '''进行注册处理'''
#     # 接收数据
#     username = request.POST.get("username")
#     password = request.POST.get("password")
#     email = request.POST.get("email")
#     allow = request.POST.get("allow")
#     # 进行数据的校验
#     if not all([username, password, email]):
#         return render(request, "register.html", {"error_message": "数据不完整"})
#     if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
#         return render(request, "register.html", {"error_message": "邮箱格式不正确"})
#     if allow != "on":
#         return render(request, "register.html", {"error_message": "请同意协议"})
#     # 校验用户名是否重复
#     try:
#         User.objects.get(username=username)
#     except User.DoesNotExist:
#         user = None
#
#     if user:
#         return render(request, "register.html", {"error_message": "用户名已存在"})
#     # 进行业务处理：进行用户注册
#     user = User()
#     user.username = username
#     user.password = password
#     user.email = email
#     user.save()
#     # 　返回应答
#     return redirect(reverse("App:index"))
