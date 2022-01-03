from garpixcms.urls import *  # noqa


urlpatterns = [
                  # path('', include('miner.urls')),
    path('admin/', admin.site.urls),
    path("api/", include("api.urls"), name="api"),
    path("", include("authentication.urls"), name="auth"),  # Auth routes - login / register
    path("", include("home.urls"), name="home"),  # UI Kits Html files
              ] #+ urlpatterns  # noqa

