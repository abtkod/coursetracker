from django.conf.urls import url
from history import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^display', views.display_history, name='display'),
]