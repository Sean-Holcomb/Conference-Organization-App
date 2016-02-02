#!/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by wesc on 2014 may 24

"""

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from conference import ConferenceApi
from google.appengine.api import memcache
from models import Session

__author__ = 'wesc+api@google.com (Wesley Chun)'


class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )


class SetFeaturedSpeakerHandler(webapp2.RequestHandler):
    def post(self):
        """Set Featured Speaker in Memcahce"""
        wsck = self.request.get('websafeConferenceKey')
        sessions = Session.query()
        sessions = sessions.filter(
            Session.websafeConferenceKey == wsck)

        # Find Speaker who will be seaking at the most sessions
        # for this conference
        speakers = {}
        topCount = 0
        for session in sessions:
            if speakers.has_key(session.speaker):
                speakers[session.speaker] += 1
            else:
                speakers[session.speaker] = 1
            if speakers[session.speaker] > topCount:
                featuredSpeaker = session.speaker
                topCount = speakers[session.speaker]
        sessions = sessions.filter(
            Session.speaker == featuredSpeaker)

        # Create string with speaker and all their sessions
        # for memcache
        returnString = "Featuring " + featuredSpeaker + " speaking at:"
        for session in sessions:
            returnString = returnString + " " + session.name

        memcache.set(wsck, returnString)

app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/set_featured_speaker', SetFeaturedSpeakerHandler)
], debug=True)
