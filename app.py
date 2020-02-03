import os
import slack
from flask import Flask, request
from slackeventsapi import SlackEventAdapter

client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
signing_secret = os.environ["SLACK_SIGNING_SECRET"]
state="super-secret-state"
# Scopes needed for this app
oauth_scope = "".join(["chat:write", "channels:read", "channels:join", "channels:manage"])

app = Flask(__name__)

# Route to kick off Oauth flow
@app.route("/begin_auth", methods=["GET"])
def pre_install():
  return f'<a href="https://slack.com/oauth/v2/authorize?scope={ oauth_scope }&client_id={ client_id }&state={state}"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>'

# Route for Oauth flow to redirect to after user accepts scopes
@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
  # Retrieve the auth code and state from the request params
    auth_code = request.args["code"]
    received_state = request.args["state"]

  # Token is not required to call the oauth.v2.access method
    client = slack.WebClient()
  
    if received_state == state:
      # Exchange the authorization code for an access token with Slack
      response = client.oauth_v2_access(
          client_id=client_id,
          client_secret=client_secret,
          code=auth_code
      )
    else:
      return "Invalid State"

    # Save the bot token to an environmental variable or to your data store
    os.environ["SLACK_BOT_TOKEN"] = response["access_token"]

    # See if "the-welcome-channel" exists. Create it if it doesn't. 
    channel_exists()

    # Don't forget to let the user know that auth has succeeded!
    return "Auth complete!"

# verifies if "the-welcome-channel" already exists
def channel_exists():
    token = os.environ["SLACK_BOT_TOKEN"]
    client = slack.WebClient(token=token)

    # grab a list of all the channels in a workspace
    clist = client.conversations_list()
    exists = False
    for k in clist["channels"]:
      # look for the channel in the list of existing channels
      if k["name"] == "the-welcome-channel":
        exists = True
        break
    if exists == False:
      # create the channel since it doesn't exist
      create_channel()

# creates a channel named "the-welcome-channel"
def create_channel():
    token = os.environ["SLACK_BOT_TOKEN"]
    client = slack.WebClient(token=token)
    resp = client.conversations_create(name="the-welcome-channel")

# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
slack_events_adapter = SlackEventAdapter(signing_secret, "/slack/events", app)

# Create an event listener for "member_joined_channel" events
# Sends a DM to the user who joined the channel
@slack_events_adapter.on("member_joined_channel")
def member_joined_channel(event_data):
    user = event_data["event"]["user"]
    channelid = event_data["event"]["channel"]
    token = os.environ["SLACK_BOT_TOKEN"]
    
    # In case the app doesn't have access to the oAuth Token
    if token is None:
      print("ERROR: Autenticate the App!")
      return
    client = slack.WebClient(token=token)

    # Use conversations.info method to get channel name for DM msg
    info = client.conversations_info(channel=channelid)
    msg = f'Welcome! Thanks for joining {info["channel"]["name"]}'
    client.chat_postMessage(channel=user, text=msg)


