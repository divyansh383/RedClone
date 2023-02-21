#acount urls
from django.urls import path,include
from django.views.generic import TemplateView
from . import views

from backend.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from django.conf import settings
urlpatterns=[
    path('',TemplateView.as_view(template_name='index.html')),
    
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    #path('auth/',include('djoser.social.urls')),

    path('auth/verifyUser',views.verify),
    path('userpost',views.postItem),
    path('getpost',views.getItem),
    path('getUser/<int:pk>',views.getUser),
    path('search/',views.searchPost),
    path('getpostid/<int:pk>', views.getItemid),
    path('getLike/<int:pk>/',views.getLike),
    path('updateLike/<int:pk>/',views.updateLike),
    path('addComment',views.addComment),
    path('getComments',views.getComments),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)