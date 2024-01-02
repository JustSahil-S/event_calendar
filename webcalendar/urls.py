from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:year>/<int:month>/<int:day>", views.day_view, name="day_view"),    
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("addEvent", views.add_event, name="addevent"),
    path("deleteEvent", views.delete_event, name="deleteevent"),
    path("share", views.share, name="share"),
    path("shareWith", views.share_with, name="shareWith"),
    path("editEvent", views.edit_event, name="editevent"),
    path("newCalendar", views.new_calendar, name="newcalendar"),
    path("getcalendar/<int:yearSelection>/<int:monthSelection>", views.get_calendar, name="getcalendar"),
]