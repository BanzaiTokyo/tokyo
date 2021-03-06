from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from django.views.static import serve
from django.conf.urls.static import static
from django.http import HttpResponse

from askapp import settings
from askapp import views, api
from askapp.sitemaps import sitemap_dict
from markdownx.urls import urlpatterns as markdownx_urls
#from registration.backends.default.urls import urlpatterns as reg_urls

urlpatterns = [
    # system URLs
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', admin.site.urls),
    url(r'^markdownx/', (markdownx_urls, 'markdownx', 'markdownx')),
    #url(r'^i18n/', django.conf.urls.i18n),
    url(r'^sitemap\.xml$', cache_page(86400)(sitemaps_views.index), {'sitemaps': sitemap_dict, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$', cache_page(86400)(sitemaps_views.sitemap), {'sitemaps': sitemap_dict}, name='sitemaps'),

    # static templates
    # url(r'^newregister$', views.NewRegisterView.as_view(), name="new_register"),
    # url(r'^newlogin$', views.NewLoginView.as_view(), name="new_login"),
    # url(r'^thankyou$', views.ThankyouView.as_view(), name="thankyou"),
    # url(r'^question$', views.QuestionView.as_view(), name="question"),

    # content pages
    url(r'^$', views.HomeView.as_view(), name="index"),
    url(r'^recent$', views.RecentThreadsView.as_view(), name="recent"),
    url(r'^profile/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$', views.ProfileView.as_view(), name="profile"),
    url(r'^thread/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$', views.ThreadView.as_view(), name="thread"),
    url(r'^tag/(?P<slug>[-\w]+)$', views.TagView.as_view(), name="tag"),
    url(r'^domains$', views.DomainsView.as_view(), name="domains"),
    url(r'^domains/(?P<domain>[-\w\.]+)$', views.DomainThreadsView.as_view(), name="domain_thread"),

    #url(r'^accounts/register/$', views.AskappRegistrationView.as_view(), name='register'),
    #url(r'^accounts/', (reg_urls, 'registration', 'registration')),
    url(r'^accounts/', include('allauth.urls')),

    # API
    url(r'api/v1/article/add$', api.AddArticle.as_view(), name="api_add_article"),

    # authenticated users
    url(r'^profile/edit$', views.ProfileEditView.as_view(), name="profile_edit"),
    url(r'^profile/(?P<pk>\d+)/edit$', views.AdminProfileEditView.as_view(), name="admin_profile_edit"),
    url(r'^submit$', views.NewThreadView.as_view(), name="new_thread"),
    url(r'^favorites$', views.FavoriteThreadsView.as_view(), name="favorites"),
    url(r'^thread/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))/edit$', views.EditThreadView.as_view(), name="edit_thread"),
    url(r'^thread/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))/delete$', views.DeleteThreadView.as_view(), name="delete_thread"),
    url(r'^thread/(?P<thread_id>\d+)(?:/(?P<slug>[\w\d-]+))/(?P<action>lock|unlock)', views.LockThreadView.as_view(),
        name="lock_thread"),
    url(r'^thread/(?P<thread_id>\d+)(?:/(?P<slug>[\w\d-]+))/reply$', views.ReplyThreadView.as_view(),
        name="reply_thread"),
    url(r'^comment/(?P<post_id>\d+)$', views.ReplyCommentView.as_view(), name="comment_page"),
    url(r'^comment/(?P<post_id>\d+)/delete$', views.DeleteCommentView.as_view(), name="delete_comment"),
    url(r'^comment/(?P<post_id>\d+)/delete_all$', views.DeleteCommentTreeView.as_view(), name="delete_comment_tree"),

    url(r'^thread/(?P<thread_id>\d+)(?:/(?P<slug>[\w\d-]+))/vote/(?P<verb>up|down)$', views.ThreadLikeView.as_view(),
        name="thread_like"),
    url(r'^post/(?P<post_id>\d+)/vote/(?P<verb>up|down)$', views.PostLikeView.as_view(), name="post_like"),
    url(r'^post/(?P<post_id>\d+)/accept$', views.AcceptAnswerView.as_view(), name="accept_answer"),

    url(r'^ytinfo$', views.YoutubeInfo.as_view(), name="youtube_info"),
    # robots.txt
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: * \n Allow: / ", content_type="text/plain")),
]

# in debug mode launch debug_toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', debug_toolbar.urls + ('djdt', )),
    ]
