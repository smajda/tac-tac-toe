from django.conf.urls import patterns, url


urlpatterns = patterns('tic_tac_toe.views',
    url(r'^$', 'index', name='tic_tac_toe_index'),
    url(r'^(?P<board>[012]{9})/$', 'play', name='tic_tac_toe_play'),
)
