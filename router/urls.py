"""
URL configuration for router project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import RedirectView

# Initialize urlpatterns at the start
urlpatterns = []

# Add debug toolbar URLs if in DEBUG mode
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [re_path(r"^__debug__/", include(debug_toolbar.urls))]

urlpatterns += [
    path("admin/", admin.site.urls, name="admin"),
    path(
        "financial_data/",
        include(("financial_data_engine.urls", "financial_data_engine"), namespace="financial_data_engine"),
    ),
    path("analysis/", include(("analysis_engine.urls", "analysis_engine"), namespace="analysis_engine")),
    path("400/", default_views.bad_request, kwargs={"exception": Exception("Bad Request!")}),
    path("403/", default_views.permission_denied, kwargs={"exception": Exception("Permission Denied")}),
    path("404/", default_views.page_not_found, kwargs={"exception": Exception("Page not Found")}),
    path("500/", default_views.server_error),
]
