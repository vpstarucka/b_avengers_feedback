from slack_bolt import App
from .ultimo_feedback import ultimo_feedback

def register(app: App):
    app.command("/ultimo-feedback")(ultimo_feedback)
