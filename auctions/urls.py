from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("view/<int:id>", views.view, name="view"),
    path("category/<str:name>", views.category, name="category"),
    path("watchlist/<str:user>", views.watchlist, name="watchlist"),
    path("removewatchitem/<str:user>/<int:id>", views.removewatchitem, name="removewatchitem"),
    path("comment", views.comment, name="comment"),
    path("new", views.new, name="new"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
