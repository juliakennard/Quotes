from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_reg),
    path('create_user', views.create_user),
    path('login', views.login),
    path('quotes', views.quotes_wall),
    path('post_quote', views.create_quote),
    path('logout', views.logout),
    path('delete_quote/<int:quote_id>', views.delete_quote),
    path('profile/<int:user_id>', views.profile),
    path('edit', views.edit_profile),
    path('edit_user', views.edit_user),
    path('like/<int:quote_id>', views.like),
]