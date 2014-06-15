Uber challenge
==============

Here is my coding challenge submission.

- URL: [http://sbezboro.com/uber](http://sbezboro.com/uber)
- GitHub repo: [https://github.com/drusz/uber](https://github.com/drusz/uber)


**Project choice**

I chose to do the email service project.


**Technical track**

I went for a backend approach as it is what I'm most experienced working with during the past few years.


**Technical choices**

I chose Flask to write the email service app in. I've been using Python for almost all of my backend work during the
past few years. I decided to try out and learn Flask recently by building a simple gaming-related web site, and ended up
greatly appreciating the simplicity and straight-forwardness of the microframework. So Flask seemed to be an ideal fit
for this project due to the project's small size and requirements. I'm not fond of the more bloated feel of larger
frameworks such as Django or Pyramid if the app is not too complex.

The app consists of a basic frontend that allows the user to submit email sending requests via a simple form. There is
also an API layer (docs [here](https://github.com/drusz/uber/blob/master/docs/api.md)) that exposes the same email sending
functionality but asynchronously using a task system. API email sending requests return a task id that can be queried
afterwards to determine the status of the request.

The email services are defined in uber/email/services.py. Adding a new email service is just as simple as adding
a new `BaseEmailService` subclass in that module. As long as it is is a fully implementing subclass,
it will be automatically served to deliver emails requested by the user.

Memcache is used as a simple cache to store when an email service is unavailable to speed up future requests for a
small period of time. I'm much more familiar with relational databases, but I ended up deciding to learn and use MongoDB
as a database to store status logs of the sent emails. Something like MySQL seemed to be overkill for the simple
requirements of the app. I use celery for the asynchronous task processing with redis as the broker.

I included some decently thorough automated tests covering the major functionality of the frontend, backend and API
layers. The tests can be started by simply running `nosetests` from the project root.


**Trade-offs and things left out**

If I were to continue on the project, I'd like to really flesh out the frontend more by learning backbone and using the
asynchronous task system for a more pleasant UX. The form would return immediately, and the user would see their active
requests update in real time on the page.

Another improvement could be rate limiting IP addresses. I could also add and require simple user logins/profiles/API
keys to use the service, to better restrict illegitimate usage while also making the sending process more friendly for
users. Some more in-depth tests with celery properly mocked/tested would be nice.


**Other Notes**

Pretty much all of the code in the repo is written by me, apart from a handful of Flask code samples (for example
`def make_celery()` in uber/factory.py). Flask itself doesn't contain any boilerplate code, which I like.

Took just over 4 hours to write the first [prototype](https://github.com/drusz/uber/commit/c9509c07261aaf98ca007209f2e3552f8bbe7b3b),
then I spent the next 5 days outside of work just continuing to add on new features, tests, docs and whatnot until
I was more or less happy with the result.

Some of my larger side-projects I'm fond of:
- [standard-web-flask](https://github.com/sbezboro/standard-web-flask)
  (running [standardsurvival.com](http://standardsurvival.com))
- [standard-plugin](https://github.com/sbezboro/standard-plugin)
- [standard-rts](https://github.com/sbezboro/standard-rts)

Other stuff:
- [GitHub profile](https://github.com/sbezboro)

Thanks for your time!

Sergei Bezborodko
