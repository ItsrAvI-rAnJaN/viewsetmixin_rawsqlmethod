from django.urls import path
from . import views

urlpatterns = [
    # path('add_detail/', views.add_detail, name='add_detail'),
    # path('retrive_detail/', views.retrive_detail, name='retrive_detail'),
    # path('update_detail/', views.update_detail, name='update_detail'),
    # path('delete_detail/', views.delete_detail, name='delete_detail'),
    path("choice/", views.ChoiceAPI.as_view(), name="choicapi"),
    path('polls/<int:id>', views.PollsAPI.as_view(), name='pollsapi'),
    path('polls/', views.PollsAPI.as_view(), name='pollsapi'),

]
