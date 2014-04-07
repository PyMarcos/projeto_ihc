from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from busca.views import SearchChar, Search, Index, Heroes, Hero, Login, Characters

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', Index.as_view(), name="home"),
     url(r'^busca/$', SearchChar.as_view(), name='search'),
     url(r'^personagens/$', Heroes.as_view(), name='characters'),
     url(r'^heroi/$', Hero.as_view()),
     url(r'^personagem/(?P<detail_url>.+)/$', Hero.as_view(), name='character'),
     url(r'^login/$', Login.as_view()),
     url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
