from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/interviews/', include('interviews.urls')),
    path('api/agents/', include('agents.urls')),
    path('api/reports/', include('reports.urls')),  # ← Add this
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)