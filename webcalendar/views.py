from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import User, Calendar, Event
from datetime import datetime
import calendar
from django.core.serializers.json import DjangoJSONEncoder


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "webcalendar/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "webcalendar/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "webcalendar/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            newcalendar = Calendar.objects.create(owner=user, title="Default")
            newcalendar.save

        except IntegrityError:
            return render(request, "webcalendar/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "webcalendar/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def index(request, calendar_title=None):
    year=datetime.now().year
    month=datetime.now().month
    monthCalendar = calendar.HTMLCalendar().formatmonth(year, month)
    return render(request, "webcalendar/index.html", 
                {"calendar": monthCalendar})

def get_calendar(request, yearSelection, monthSelection):
    CalendarObjs = Calendar.objects.filter(Q(owner = User.objects.get(username = request.user.username)) | Q(sharedUsers = User.objects.get(username = request.user.username)))
    EventList = []
    for ev in Event.objects.filter(calendar__in=CalendarObjs, year=yearSelection, month=monthSelection):
        EventList.append(ev.Event_Attributes())
    return JsonResponse({"calendar": calendar.HTMLCalendar().formatmonth(yearSelection, monthSelection), "Events": EventList})


def day_view(request, year, month, day):
    CalendarObjs = Calendar.objects.filter(Q(owner = User.objects.get(username = request.user.username)) | Q(sharedUsers = User.objects.get(username = request.user.username)))
    Events = Event.objects.filter(calendar__in=CalendarObjs, year = year, month = month, day = day)
    netTimeList = []
    EventList = []
    for event in Events:
        netTime = (event.startHour * 60 + event.startMin, event.endHour*60+event.endMin, event.id)
        netTimeList.append(netTime)
        EventList.append(event)
    if EventList:
        netTimeList, EventList = zip(*sorted(zip(netTimeList, EventList)))
    return render(request, "webcalendar/dayevent.html", {
                  "events": EventList,
                  "day": day,
                  "month": month,
                  "year": year,
                  "calendars": CalendarObjs
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def add_event(request):
    title = request.POST['title']
    subject = request.POST['subject']
    startMin = request.POST['startMin']
    startHour = request.POST['startHour']
    endMin = request.POST['endMin']
    endHour = request.POST['endHour']
    year = request.POST['year']
    month = request.POST['month']
    day = request.POST['day']
    calendar = request.POST['calendar']
    Event.objects.create(
        title = title, 
        subject = subject, 
        startMin = startMin, 
        startHour = startHour,
        endMin = endMin,
        endHour = endHour,
        owner = request.user, 
        calendar = Calendar.objects.get(id = calendar),
        day = day,
        month = month,
        year = year,
    )
    return HttpResponseRedirect(f"/{year}/{month}/{day}")
def delete_event(request):
    year = request.POST['year']
    month = request.POST['month']
    day = request.POST['day']
    event = request.POST['event']
    Event.objects.filter(id=event).delete()
    return HttpResponseRedirect(f"/{year}/{month}/{day}")
def edit_event(request):
    year = request.POST['year']
    month = request.POST['month']
    day = request.POST['day']
    event = request.POST['event']
    startMin = request.POST['startMin']
    startHour = request.POST['startHour']
    endMin = request.POST['endMin']
    endHour = request.POST['endHour']
    title = request.POST['title']
    subject = request.POST['subject']
    item = Event.objects.filter(id=event)[0]
    item.startMin = startMin
    item.startHour = startHour
    item.endMin = endMin
    item.endHour = endHour
    item.title = title
    item.subject = subject
    item.save()
    return HttpResponseRedirect(f"/{year}/{month}/{day}")
def new_calendar(request):
        Calendar.objects.create(owner=User.objects.get(username = request.user.username), title = request.POST['title'])
        return HttpResponseRedirect(f"/share")
def share(request):
         CalendarObjs = Calendar.objects.filter(owner=User.objects.get(username = request.user.username))
         SharedCalendarObjs = Calendar.objects.filter(sharedUsers=User.objects.get(username = request.user.username))
         return render(request, "webcalendar/share.html", {
                "calendars": CalendarObjs,
                "shared": SharedCalendarObjs
    })
def share_with(request):
    if Calendar.objects.get(id = request.POST["calendar"]).owner == request.user:
        status = request.POST["status"]
        if status == "Add":
            shareWith = request.POST["username"]
            sharedUser = User.objects.get(username = shareWith)
            Calendar.objects.get(id = request.POST["calendar"]).sharedUsers.add(sharedUser)
        if status == "Remove":
            calendarid = request.POST["calendar"]
            removed = request.POST["username"]
            Calendar.objects.get(id = calendarid).sharedUsers.remove(User.objects.get(username = removed))
        return HttpResponseRedirect(f"/share")
    else: 
        return HttpResponse("You are not the Owner of this Calendar")
    

