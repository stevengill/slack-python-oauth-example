# Slack Python OAuth Example

This repo contains a sample app for doing OAuth with Slack. It uses the [python-slackclient](https://github.com/slackapi/python-slackclient) and [python-slack-events-api](https://github.com/slackapi/python-slack-events-api). It has been tested on `python 3.7.5`.

I recommend using [`ngrok`](https://ngrok.com/download) for local development of slack apps. Checkout [this guide](https://api.slack.com/tutorials/tunneling-with-ngrok) for setting it up.

## Install dependencies

```
pip3 install slackclient
pip3 install slackeventsapi
pip3 install flask
```

## Setup enviroment variables

This app requires you setup a few enviroment variables. You can get these values by navigating to your app's [**BASIC INFORMATION** Page](https://api.slack.com/apps). 

```
export SLACK_CLIENT_ID = YOUR_SLACK_CLIENT_ID
export SLACK_CLIENT_SECRET = YOUR_SLACK_CLIENT_SECRET
export SLACK_SIGNING_SECRET = YOUR_SLACK_SIGNING_SECRET
```
You also need to setup `FLASK_APP` enviroment variable so `flask run` knows what to run. This should point to this repos `app.py`.

```
export FLASK_APP=app.py
```

## Run the App

Start the app by running the following command

```
flask run
```

This will start the app on port `5000`.

Now lets start `ngrok` so we can access the app on an external network and create a `redirect url` for OAuth and a `request url` for events. 

```
ngrok http 5000
```

This should output a forwarding address for `http` and `https`. Take note of the `https` one. It should look something like the following:

```
Forwarding   https://3cb89939.ngrok.io -> http://localhost:5000
```

Go to your app on https://api.slack.com/apps and navigate to your apps **OAuth & Permissions** page. Under **Redirect URLs**, add your `ngrok` forwarding address with the `/finish_auth` path appended. ex:

```
https://3cb89939.ngrok.io/finish_auth
```

Now go to **Event Subscriptions** and enable events. For the **Request URL**, pass your `ngrok` forwarding address with `/slack/events` path appended. ex:

```
https://3cb89939.ngrok.io/slack/events
```

Everything is setup. Go to [`http:localhost:5000/begin_auth`](http:localhost:5000/begin_auth) in your browser to start the OAuth install flow for you app!




