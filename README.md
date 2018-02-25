# Engage

[![Build Status](https://travis-ci.org/ograycode/engage.svg?branch=master)](https://travis-ci.org/ograycode/engage)
[![Maintainability](https://api.codeclimate.com/v1/badges/39d4a37116054c786c39/maintainability)](https://codeclimate.com/github/ograycode/engage/maintainability)

## About

Engage is a platform for running A/B tests with emails. The idea behind it is simple:

- Decouple email templates, and A/B tests from your system so your application is only responsible for generating the context to fill in the blanks of the email. This simple idea means that those responsible for A/B testing can do so with minimal involvement with the underlying system sending it.

## Status

Engage is incomplete. The basics are there, but it requires the following to finish it up:

- Hook up an email provider (sendgrid is the first target).
- Create callback hooks for email events.
- Implement a system of click tracking (google analytics, redirects, or another system).
- Create a view for email stats.
- Double check that all forms and flows are implemented.

## Workflow notes

- Engage is meant to hold all templates and A/B tests (called Experiments).
- Templates are rendered using context provided by other systems, and use handlebars for rendering.

An example api call from your system to engage would look something like:

```json
{
  "to_emails": ["to@test.com"],
  "from_email": "from@test.com",
  "subject": "this is the subject",
  "content_type": "plaintext",
  "data": {
    "message": "hello world"
  },
  "email_group": "123"
  "provider": "456"
}
```

While your email template, assigned to the email group `123` would look something like:

```html
<h1>Some title</h1>
<p>{{message}}</p>
```

Using this system means you could setup an A/B test for email group `123` and change something about the email, and Engage would take care of rendering the B email, sending it using your provider, and tracking the results.

## Why is this open source?

I originally created this as a closed-source project, but am unsure if I will ever be able to finish it. Because of this, I have decided to open source it. Even if I did finish the project, it will likely remain open source and money would be generated to support it by running a hosted version.
