from django.conf.urls import url
from . import views
import model.Story_World.Scenes as scene

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/process_message/$', views.process_message, name = 'process_message')
]

scene.executeAll()