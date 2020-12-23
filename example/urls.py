from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import TemplateView
from .demo import views

admin.autodiscover()
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile),
    path("notify/", views.notify_by_message_api),
    path('admin/', admin.site.urls),
]


# https://access.line.me/oauth2/v2.1/authorize?client_id=1655321706&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2F&scope=profile&response_type=code&state=TzVDnVSaMAqO

# やりたいこと
# social login後の通知

