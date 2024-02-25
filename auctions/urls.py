from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listing, name="create"),
    path("category_view/", views.category_view, name="category_view"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("removewatchlist/<int:listing_id>", views.removewatchlist, name="removewatchlist"),
    path("addwatchlist/<int:listing_id>", views.addwatchlist, name="addwatchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("addcomment/<int:listing_id>", views.addcomment, name="addcomment"),
    path("addbid/<int:listing_id>", views.addbid, name="addbid"),
    path("closelisting/<int:listing_id>", views.closelisting, name="closelisting"),   
    path("closedlistings", views.closedlistings_view, name="closedlistings"),   
]
