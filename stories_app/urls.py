from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup', views.signup_page, name='signup_page'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_page, name='logout_page'),

    path('', views.home, name='home'),
    path('write_story', views.write_story, name='write_story'),
    path('all_stories', views.all_stories, name='all_stories'),
    path('story/<int:item_id>', views.story, name='story'),
    path('edit/<int:item_id>', views.edit, name='edit'),
    path('delete/<int:item_id>/', views.delete_story, name='delete_story'),
    path('contact', views.contact, name='contact'),
    path('permissions', views.permissions, name='permissions')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
