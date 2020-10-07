from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:pk>", views.listing, name='listing'),
    path("watchlist/<int:pk>", views.watchlist, name='watchlist'),
    path("add_watchlist/<int:pk>", views.add_watchlist, name='add_watchlist'),
    path("remove_watchlist/<int:pk>",
         views.remove_watchlist, name='remove_watchlist'),
    path('create_listing', views.create_listing, name='create_listing'),
    path("bid/<int:pk>", views.bidding, name='bidding'),



]
