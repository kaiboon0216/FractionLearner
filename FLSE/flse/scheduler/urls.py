from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('calender/', views.CalendarView.as_view(), name='calendar'),
    path('calender/event/new/', views.create_event, name='schedule_new'),
    path('calender/event/edit/<int:pk>/', views.ScheduleEdit.as_view(), name='schedule_edit'),
    path('calender/event/<int:pk>/details/', views.schedule_details, name='schedule-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)