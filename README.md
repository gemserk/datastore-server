Datastore Server
=============

Datastore-server is a Google App Engine web application written in Python which allows you to manage game high scores remotely.

Installation
-------

The application is really easy to install and use, first download and install [Google App Engine SDK for Python][gae-sdk], and download [datastore-server][datastore-server] from Github.

After that, open [Google App Angine][gae], login with a Google account and create a new application with the name you want for your highscores server, for example, MyGameScoresSystem.

Finally, go to the datastore-server folder and upload the application following this [tutorial][gae-upload].

Your application should be ready to be accessed by opening http://{your application id}.appspot.com

Enjoy it.

[gae-sdk]: http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python
[gae]: https://appengine.google.com/
[gae-upload]: http://code.google.com/appengine/docs/python/gettingstarted/uploading.html
[datastore-server]: git://github.com/gemserk/datastore-server.git
