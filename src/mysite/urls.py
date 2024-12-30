from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from django.conf.urls.static import static #EC

from django.views.static import serve  #追加


from app import views # 追記箇所


handler400 = views.error_400page # 追記箇所
handler403 = views.error_403page # 追記箇所
handler404 = views.error_404page # 追記箇所
# handler500 = views.error_500page # 追記箇所


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


