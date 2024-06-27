from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('company/<int:company_id>/', views.company_detail, name='company_detail'),
    path('submit/', views.submit_job, name='submit_job'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
]