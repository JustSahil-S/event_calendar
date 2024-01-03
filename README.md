My final project is a calendar app which allows users to create multiple calendars and events as well as sharing calendars with others. More specifically, the users can create, name, and set a color (which is reflected in the events) for their own calendars. They can share the calendar with others which allows them to see the events that are added and also add their own events to that calendar. The user can decide the timeframe, title, and contents of their events. The events can be deleted or edited by the person who made it but cannot be altered by other calendar viewers.

My program can be run by using manage.py runserver. The index.html, index.js, and index/get_calendar view, are responsible for changing the calendar dates using JavaScript based on the user input and also redirecting to the daily view when a day is pressed. The dayevent.html file and its corresponding views are responsible for displaying the daily view where users can add and edit their events for all the calendars during that day. The share.html and its corresponding views/urls are responsible for managing the calendars by adding users or creating new calendars. My calendar model has fields that have the owner of the calendar, shared users, and the color. The events model has timestamp fields, subject and title fields, and the calendar object that it belongs to. 

Distinctiveness and Complexity:

My project is distinctive from the other projects that I have made or learned about during this course. While adding events is similar to things I have already learned like creating listings in the commerce project, I believe this app has a lot of changes and additional features that aren't in the other projects. Since it revolves around a calendar, it uses new python libraries that I haven't been used in this course before such as the calendar library. It also uses some unique form fields like a color picker. Some other distinctive features of my app is the sharing feature and displaying the days that events take place. I used a lot of techniques in the program that I haven't used in other projects such as sorting between 2 fields that are in seperate models in order to get a list of all the users and owners that are associated with a calendar. 

In terms of complexity, I believe that the program has more complexity than the other projects so far. Some of the things that I think contribute to this is the code for sorting the events based on the time, linking events and calendars between users using the django models, and the general amount of pages and features in the application like editing and deleting calendars/events. My program uses 2 models; one for the events and one for the calendar. It uses a large variety of fields for each model such as many-to-many and foreign key relationships. Like the other projects, it has a social aspect where users make an account and can influence the website for others by changing events or adding calendars. Lastly, I think the program shows complexity in the Javascript which is used to change the calendar by sending requests to the python view for calendar data and then displaying it. It also uses filters to determine which days have events or are the current day and it adds event listeners to many objects recursively. 
