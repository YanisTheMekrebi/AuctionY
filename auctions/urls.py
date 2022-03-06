from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.view_listing, name="listing"),
    path("listing/<int:listing_id>/comments/add_comment", views.add_comment, name="add_comment"),
    path("listing/comments/<int:comment_id>/delete", views.delete_comment, name="delete_comment"),
    path("listing/close/<int:listing_id>", views.close_view, name="close"),
    path("listing/create", views.create_listing, name="create"),
    path("listing/me/all", views.my_listings_view, name="my_listings"),
    path("listing/me/my_bids", views.my_bids_view, name="my_bids"),
    path("watchlist/modify/<int:listing_id>", views.modify_watchlist, name="modify_watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist"),
]
