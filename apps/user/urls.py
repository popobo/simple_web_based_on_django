from django.conf.urls import url
from apps.user.views import RegisterView, ActiveView, LoginView, UserCenterView, LoginOutView, CancelFavoriteView

urlpatterns = [
    url(r"^register$", RegisterView.as_view(), name="register"),
    url(r"^active/(?P<token>.*)$", ActiveView.as_view(), name="active"),
    url(r"^login$", LoginView.as_view(), name="login"),
    url(r"^user_center$", UserCenterView.as_view(), name="login"),
    url(r"^login_out$", LoginOutView.as_view(), name="login_out"),
    url(r"^cancel_favorite/(?P<cancel_favorite_id>\d*)$", CancelFavoriteView.as_view(), name="cancel_favorite"),
]
