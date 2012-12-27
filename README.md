email-renderer
==============

This app renders Guardian emails from content in the Content API.

## Running the email renderer

This is a Python appengine application. Grab the source and then run
the dev appserver provided in the Google appengine SDK. From within
the email renderer's directory and assuming you have the linux tools
in yuor home directory:

    ~/linux-dev/google_appengine/dev_appserver.py . --port=8888

You can then view the daily email at http://localhost:8888/daily-email.

## Details

Currently, only the daily Guardian Today email is rendered with this
app. The `mail_renderer.py` file contains the main logic for the
application which is roughly:

1. Fetch the article info from the content API, as well as a picture of the day
2. Fetch an advert from OAS
3. Pass this data to the Jinja2 template for the daily email

This content is also cached with memcached so the application will
first try to serve the rendered content out of the cache.

The application is hosted on appengine and is available at
http://***REMOVED***.appspot.com/daily-email

## Template

The `master.html` template contains the basic layout of the
email. Stories are rendered using macros found in the `macro`
subfolder.

## ExactTarget integration

The email content is scraped out of the daily-email page by
ExactTarget. The Exact Target configuration is at
https://members.s4.exacttarget.com, ask someone for the credentials.

The Today email uses a custom template that includes two main components.

1. A custom content block that scrapes the content from this application
2. The Today email's footer, which includes an ExactTarget unsubscribe link
