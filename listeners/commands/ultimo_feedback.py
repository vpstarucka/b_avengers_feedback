from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from slack_sdk import WebClient
import re


def ultimo_feedback(client: WebClient, ack: Ack, command, say: Say, logger: Logger, context: BoltContext):    
    try:
        ack()
        user_id = context["user_id"]
        channel_id = context["channel_id"]
        prompt = command["text"]

        result = client.conversations_history(channel=channel_id)
        conversation_history = result["messages"]

        if prompt == "":
            client.chat_postEphemeral(
                channel=channel_id, user=user_id, text="Looks like you didn't provide a prompt. Try again."
            )

        else:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                blocks=[
                    {
                        "type": "rich_text",
                        "elements": [
                            {
                                "type": "rich_text_quote",
                                "elements": [{"type": "text", "text": prompt}],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [{"type": "text", "text": last_feedback_by_name(conversation_history, prompt)}],
                            },
                        ],
                    }
                ],
            )
    except Exception as e:
        logger.error(e)
        client.chat_postEphemeral(channel=channel_id, user=user_id, text=f"Received an error from Bolty:\n{e}")


def last_feedback_by_name(conversation_history, prompt):
    last_feedback = "Last feedback not found"
    cleaned_text = re.sub(r'\|.*?(?=>)', '', prompt)
    
    for message in conversation_history:
        if cleaned_text in message["text"]:
            last_feedback = message["text"]
            break
    return last_feedback
