from django.conf.urls import url
from . import views
import model.externals.core_nlp_server as server
import model.story_world.story_scenes as scene
import model.externals.logger as logger

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/process_message/$', views.process_message, name = 'process_message'),
    url(r'^ajax/prev_page/$', views.prev_page, name = 'prev_page'),
    url(r'^ajax/next_page/$', views.next_page, name='next_page'),
    url(r'^ajax/generate_log/$', views.generate_log, name='generate_log')
]

server.run_server()
scene.startScene1()
#scene.executeAll()
logger.log("---Page Progress", "Now on page 1.---")
logger.log("---Chapter Progress", "Now on scene 1.---")
#scene.printSentences()
