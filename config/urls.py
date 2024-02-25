from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('users/', include('users.urls', namespace="users")),
    path('tournament/', include('tournament.urls'))
]


admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Естественно Научный Турнир"