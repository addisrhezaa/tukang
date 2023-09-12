from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login_request, name='login'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('blog/', views.blog, name='blog'),
    path('blog-single/<str:id>', views.blogsingle, name='blogsingle'),
    path('viewbanner/', views.view_banner, name='viewbanner'),
    path('createbanner/', views.create_banner, name='addbanner'),
    path('updatebanner/<str:id>',views.update_banner,name='updatebanner'),
    path('deletebanner/<str:id>',views.delete_banner,name='deletebanner'),
    path('viewblog/', views.view_blog, name='viewblog'),
    path('createblog/', views.create_blog, name='addblog'),
    path('updateblog/<str:id>',views.update_blog,name='updateblog'),
    path('deleteblog/<str:id>',views.delete_blog,name='deleteblog'),
    path('createprofesional/', views.create_prof_form, name='createprofesional'),
    path('createworker/', views.create_work_form, name='createworker'),
    path('createitem/', views.create_item_form, name='createitem'),
    path('viewprofesional/', views.profesional, name='viewprofesional'),
    path('viewworker/', views.worker, name='viewworker'),
    path('viewitem/', views.item, name='viewitem'),
]