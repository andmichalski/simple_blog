from django.conf.urls import url
from . import views
from .views import MainList, PostDetail, AboutMeView

urlpatterns = [
    url(r'^$', MainList.as_view(), name='index'),
    url(r'^about_me$', AboutMeView.as_view(), name='about_me'),
    url(r'^post/(?P<pk>\d+)$', PostDetail.as_view(), name='post_detail'),
]