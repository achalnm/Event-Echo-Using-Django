from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add_event/', views.add_event_view, name='add_event'),
    path('event/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('ticket/<int:registration_id>/', views.ticket_view, name='ticket'),
    path('events/search/', views.search_events, name='search_events'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
