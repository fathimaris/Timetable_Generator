from django.urls import path

from timetable import views

urlpatterns=[path('',views.Mainpage,name="Mainpage"),
             path('Homepage',views.Homepage,name="Homepage"),
             path('Courses',views.Courses,name="Courses"),
             path('create_course',views.create_course,name="create_course"),
             path('update_course/<int:id>/',views.update_course,name="update_course"),
             path('delete_course/<int:id>/',views.delete_course,name="delete_course"),
             path('Subjects', views.Subjects, name="Subjects"),
             path('create_subject', views.create_subject, name="create_subject"),
             path('update_subject/<int:id>/',views.update_subject,name="update_subject"),
             path('delete_subject/<int:id>/',views.delete_subject,name="delete_subject"),
             path('Staffs/', views.Staffs, name="Staffs"),
             path('create_staff/', views.create_staff, name="create_staff"),
             path('update_staff/<int:id>/', views.update_staff, name="update_staff"),
             path('delete_staff/<int:id>/', views.delete_staff, name="delete_staff"),
             path('generate-timetable/', views.generate_timetable, name='generate_timetable'),

             ]