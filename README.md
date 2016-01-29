App Engine application for the Udacity training course.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
1. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
1. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
1. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
1. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
1. (Optional) Generate your client library(ies) with [the endpoints tool][6].
1. Deploy your application.

## Tasks
### Task 1: Add Sessions to a Conference
To implement sessions to the app, I modeled the session classes and methods after the extant Conference classes and methods. The some of the support methods already in place were useful in this regard but others had to be redesigned to fit my needs, in general sessions are much more simple than confrences so it was straight forward to proccess their contents.

#### Extra Credit
I decided to keep the speaker entity simple, becasue linking it to several factors would have been convoluted and pointless. All it really needs is a list of sessions that it will be speaking at. I decided not to link it to a profile because there is no garentee that a speaker would have a profile and it wouldn't add any functionality other than blocking them from adding sessions that they were speaking at to their wish list.

### Task 2: Add Sessions to User Wishlist
Adding wish lists was relatively simple. All that needed to be done was to add a repeated StringField to the Profile Class the required methods

### Task 3: Work on indexes and queries
For the two addittional querys I included getSessionAttendees(websafeSessionKey) and getConferenceAttendees(websafeConferenceKey). I chose these because for the three classes Conference, Profile and Session there was a way to get Sessions of Conferences from a Profile, and a way to get Sessions from a Conference, but no way to get Profiles from a Conference or Session.

Question: Let’s say that you don't like workshops and you don't like sessions after 7 pm. How would you handle a query for all non-workshop sessions before 7 pm? What is the problem for implementing this query? What ways to solve it did you think of?

The problem is that Google datastore API doesn't support multiple inequality filters on a single query(!= and >=). The way I would solve it is to make two queries and compare the results.

#### Extra Credit
I implemented this ability by checking queries for multiple inequality filters if they were there, The query is done by a seperate method that makes a query for each filter then

### Task 4: Add a Task
Implemented featured speaker functionality using task queue and memcache. Logic for functionality is in main.py while taskqueue call is made in conference.py.


[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:8080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool
