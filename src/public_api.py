from flask_api import app
import awsgi

def handler(event, context):
    return awsgi.response(app, event, context)