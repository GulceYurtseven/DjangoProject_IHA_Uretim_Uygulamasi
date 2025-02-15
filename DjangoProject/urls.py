from django.contrib import admin
from django.urls import path
from IhaKontrol import views
from IhaKontrol.views import dashboard, login_view, logout_view, recycle_part, list_team_parts, list_aircraft
urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("login/dashboard/", dashboard, name="dashboard"),
    path('stock_change/', views.stock_change, name='stock_change'),
    path('aircraft_assemble/', views.aircraft_assemble, name='aircraft_assemble'),
    path("takim_parcalari/", list_team_parts, name="list_team_parts"),
    path("recycle_part/<int:part_id>/", recycle_part, name="recycle_part"),
    path("aircraft_list/", list_aircraft, name="aircraft_list"),
]
