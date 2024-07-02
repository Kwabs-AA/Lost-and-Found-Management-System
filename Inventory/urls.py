from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('upload/',views.uploadview,name="upload"),
    path('find/',views.findview,name="find"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.login_user,name="login"),
    path('success/',views.success,name="success"),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('logout/',views.logout_view,name="logout"),
    path('search_file/',views.search_file,name="search_file"),
    path('review/<int:lost_item_id>/',views.review,name="review"),
    path('temp/',views.temporary,name="temp")
]