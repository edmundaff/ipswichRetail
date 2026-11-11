from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Ipswich Retail Admin'
admin.site.site_title = 'Ipswich Retail'
admin.site.index_title = 'Store management'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]
