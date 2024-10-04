from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from ai.providers import get_provider_response
from slack_sdk import WebClient
import re

"""
Callback for handling the 'ask-bolty' command. It acknowledges the command, retrieves the user's ID and prompt,
checks if the prompt is empty, and responds with either an error message or the provider's response.
"""


    # result = client.conversations_history(channel=channel_id)
    # conversation_history = result["messages"]

    # for message in conversation_history:
    #     if  in message["text"]:
    #         print(f'Found "ball" in message: {message["text"]}')
    #         break


    #     # Print results
    # logger.info("{} messages found in {}".format(len(conversation_history), channel_id))
    # print("{} messages found in {}".format(conversation_history, channel_id))
    


def last_feedback_by_name(conversation_history, prompt):
    last_feedback = ""
    match = re.search(r'@\w+', prompt)
    if match:
        username = match.group(0)  # Retrieve the matched username
        for message in conversation_history:
            if username in message["text"]:
                last_feedback = message["text"]
                print(f'Found message: {last_feedback}')
                break
    
    return last_feedback


def ask_callback(client: WebClient, ack: Ack, command, say: Say, logger: Logger, context: BoltContext):
    try:
        ack()
        user_id = context["user_id"]
        channel_id = context["channel_id"]
        prompt = command["text"]

        if prompt == "":
            client.chat_postEphemeral(
                channel=channel_id, user=user_id, text="Looks like you didn't provide a prompt. Try again."
            )
        else:
            # filtered_prompt = response_by_name(prompt)

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
                                "elements": [{"type": "text", "text": get_provider_response(user_id, prompt)}],
                            },
                        ],
                    }
                ],
            )
    except Exception as e:
        logger.error(e)
        client.chat_postEphemeral(channel=channel_id, user=user_id, text=f"Received an error from Bolty:\n{e}")
