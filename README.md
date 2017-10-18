email-renderer
==============

This app renders Guardian emails from content in the Content API.

## Running the email renderer

This is a Python appengine application. Grab the source and then run
the dev appserver provided in the Google appengine SDK. From within
the email renderer's directory and assuming you have the linux tools
in your home directory:

    ~/linux-dev/google_appengine/dev_appserver.py . --port=8888

You can then view the daily emails at http://localhost:8888/.


### Configuration

To hide implementation details the application takes some of its service connection details from configuration (and these get bound at startup time).

You will need to define configuration values for the following keys:

* `CAPI_BASE_URL`: root url of CAPI
* `CONTAINER_API_BASE_URL`: root url of the container service
* `CAPI_KEY`: valid CAPI key for the CAPI instance you're running against
* `OPHAN_BASE_URL`: the base url for the Ophan API
* `OPHAN_API_KEY`: a valid key for the Ophan API

## Running the tests

The script is in the root directory of the project:

    ./test_runner.py <path-to-appengine>

On my machine this is:

    ./test_runner.py ~/linux-dev/google_appengine/

## Releasing

Push a unique revision (normally the next number on from the last release) and use the dashboard to make it the default version when you want to actually release the changes. Due to caching you might also want to flush memcache if the data needs to be changed immediately.

To revert to a historic version use the Appengine dashboard to set a new default version. This will usually take effect immediately but you may need to flush Memcache to regenerate the emails.

### Testing a release

To test a release you can use the [checker script](https://github.com/guardian/gdn-email-renderer-check) which will look for a 200 status on all links on the top index page.

### Historic releases

The application used to deploy just to the `prod` and `qa` revisions. The qa revision is still the default target.

## Details

The front page lists all the emails the application has available. In general the v1 version of the email is the one that goes out to punters and the other versions are used in variant testing in ExactTarget.

The `mail_renderer.py` file contains the main logic for the
application which is roughly:

1. Fetch the article info from the content API, as well as a picture of the day
2. Fetch an advert from OAS
3. Pass this data to the Jinja2 template for the daily email

This content is also cached with memcached so the application will
first try to serve the rendered content out of the cache. Remember to flush the cache when making and deploying changes!

The application is hosted on appengine and is available at
http://gu-email-renderer.appspot.com/daily-email

## Template

Emails are rendered using one of two base templates.

Use `base_email.html` for a normal email structure and `base_scrape.html` for emails where the bulk of the rendering is done in ExactTarget and the application is just supplying a panel or two.

Stories are rendered using macros found in the `macro`
subfolder.

## Data sources
Data sources come from a combination of Content API, Ophan and Fronts API.

Examples of Fronts API queries can be can be found in the README of the [facia-tool-node-api repo](https://github.com/guardian/facia-tool-node-api)

## ExactTarget integration

The email content is scraped out of the daily-email page by
ExactTarget. The Exact Target configuration is at
https://members.s4.exacttarget.com, ask someone for the credentials.

The Today email uses a custom template that includes two main components.

1. A custom content block that scrapes the content from this application
2. The Today email's footer, which includes an ExactTarget unsubscribe link

## License

Copyright 2015 Guardian News and Media

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
