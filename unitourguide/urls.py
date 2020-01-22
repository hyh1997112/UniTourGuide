from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logoutpage, name='logout'),
    path('find_uni', views.find_uni, name='find_uni'),
    path('find_guide/<int:school_id>', views.find_guide, name='find_guide'),
    path('my_tour', views.my_tour, name='my_tour'),
    path('to_be_guide', views.to_be_guide, name='to_be_guide'),
    path('manage_guide', views.manage_guide, name='manage_guide'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('my_info', views.my_info, name='my_info'),
    path('write_review/<int:tour_id>', views.write_review, name='write_review'),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)