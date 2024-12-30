from django.urls import path
from app import views

urlpatterns = [
    path('', views.movies.as_view(), name='movies'),
    path('title/<int:movie_id>', views.movies.as_view(), name='movies'),
    path('genre/<int:genre_id>', views.genres.as_view(), name='genre'),
    
    #レビュー機能
    path('review_menu/', views.ReviewMenuView.as_view(), name='review_menu'),
    path('review/post/<int:movie_id>', views.ReviewPost.as_view(), name='review_post'),
    path('review_edit/<int:id>', views.ReviewEdit.as_view(), name='review_edit'),
    path('review_delete/<int:id>', views.ReviewDelete.as_view(), name='review_delete'),
    path('review_list/', views.ReviewList.as_view(), name='review_list'),
    path('review/success', views.ReviewSuccess.as_view(), name='review_success'),

    #一覧
    path('mylist', views.MyListView.as_view(), name='mylist'),
    path('playing', views.PlayingView.as_view(), name='playing'),
    path('upcoming', views.UpcomingView.as_view(), name='upcoming'),

    #Ajax
    path('mylist_add', views.MyListAdd, name='mylist_add'),
    path('genreScroll', views.genreScroll, name='genreScroll'),
    path('scroll', views.scroll, name='scroll'),
    path('mylistscroll', views.mylistScroll, name='mylistscroll'),
    path('modal', views.modal, name='modal'),
    path('review', views.review, name='review'),
]