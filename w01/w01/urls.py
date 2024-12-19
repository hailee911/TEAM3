from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin1/', include('admin1.urls')),
    path('loginpage/', include('loginpage.urls')),
    path('customer/', include('customer.urls')),
    path('emotion/', include('emotion.urls')),
    path('', include('home.urls')),
    path('main/', include('home.urls')),
    path('diary/', include('diary.urls')),
    path('mypage/', include('mypage.urls')),
    path('comment/', include('comment.urls')),
    path('calendar1/', include('calendar1.urls')),
    path('family1/', include('family1.urls')),
]


# settings.py 안에
# MEDIA_URL = 'media/' 로 들어오면
# MEDIA_ROOT = os.path.join(BASE_DIR,'media') 에서 찾아라
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)