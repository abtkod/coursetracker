from timer import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^course_start_time$', views.course_start_time, name='course_start_time')
]
