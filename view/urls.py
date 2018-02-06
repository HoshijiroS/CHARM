from django.conf.urls import url
from . import views
import model.story_world.story_scenes as scene
import model.externals.core_nlp_server as server

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/process_message/$', views.process_message, name = 'process_message')
]

scene.executeAll()
server.run_server()