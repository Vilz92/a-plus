from django.conf.urls import url

from . import views


COURSE_URL_PREFIX = r'^(?P<course>[\w\d\-\.]+)/'
INSTANCE_URL_PREFIX = COURSE_URL_PREFIX + r'(?P<instance>[\w\d\-\.]+)/'
EDIT_URL_PREFIX = INSTANCE_URL_PREFIX + r'teachers/'
USER_URL_PREFIX = INSTANCE_URL_PREFIX + r'user/'
MODULE_URL_PREFIX = INSTANCE_URL_PREFIX + r'(?P<module>[\w\d\-\.]+)/'

urlpatterns = [
    url(r'^$',
        views.HomeView.as_view(),
        name='home'),
    url(r'^archive/$',
        views.ArchiveView.as_view(),
        name="archive"),
    url(r'^accounts/$',
        views.ProfileView.as_view(),
        name="profile"),
    url(INSTANCE_URL_PREFIX + r'$',
        views.InstanceView.as_view(),
        name="course"),
    url(MODULE_URL_PREFIX + r'$',
        views.ModuleView.as_view(),
        name="module"),
]
