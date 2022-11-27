from django.urls import path, include
from salary import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


index_view = TemplateView.as_view(template_name="toppage.html")

urlpatterns = [
    path("", login_required(index_view), name="index"),
    path('', include("django.contrib.auth.urls")),
    path("signup/", views.SignUpView.as_view(), name="signup"),

    path("top/<int:year_wage_id>/", views.apptop_template, name="top"),
    path("list/", views.List, name="list"),
    path('detail/<int:work_id>/', views.Detail, name="detail"),
    path('create/', views.Creatework.as_view(), name="create"),
    path('update/<pk>/', views.Updatework.as_view(), name="update"),
    path('delete/<pk>', views.Delete.as_view(), name="delete"),

    path("listwage/", views.wagelist, name="wage_list"),
    path('createwage/',views.Createwage.as_view(), name="wage_create"),
    path('createwage/first/',views.FirstCreatewage.as_view(), name="wage_create_first"),
    path('updatewage/<pk>/',views.Updatewage.as_view(), name="wage_update"),
    path('deletewage/<pk>', views.Deletewage.as_view(), name="wage_delete"),

    path("listyearwage/", views.yearwagelist, name="yearwage_list"),
    path('createyearwage/',views.Createyearwage.as_view(), name="yearwage_create"),
    path('createyearwage/first/',views.FirstCreateyearwage.as_view(), name="yearwage_create_first"),
    path('updateyearwage/<pk>/',views.Updateyearwage.as_view(), name="yearwage_update"),
    path('deleteyearwage/<pk>', views.Deleteyearwage.as_view(), name="yearwage_delete"),
    
    path('createyukyu/',views.Createyukyu.as_view(), name="yukyu_create"),
    path('updateyukyu/',views.Updateyukyu, name="yukyu_update"),

    path('createzangyo/',views.Createzangyo.as_view(), name="zangyo_create"),
    path('updatezangyo/',views.Updatezangyo, name="zangyo_update"),
]

# エラー画面表示用
handler500 = views.my_customized_server_error