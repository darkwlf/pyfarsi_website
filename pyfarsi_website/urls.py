from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = (
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path('account/', include('account.urls')),
    path('blog/', include('blog.urls')),
    path('ck-editor/', include('ckeditor_uploader.urls')),
    path('snippets/', include('snippets.urls'))
)
