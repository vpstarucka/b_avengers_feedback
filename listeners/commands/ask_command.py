from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from ai.providers import get_provider_response
from slack_sdk import WebClient
import re

"""
Callback for handling the 'ask-bolty' command. It acknowledges the command, retrieves the user's ID and prompt,
checks if the prompt is empty, and responds with either an error message or the provider's response.
"""

def response_by_name(prompt):
    lines = prompt.splitlines()
    
    last_line = lines[-1]
    
    # Extrai o nome após o '@' e antes do primeiro espaço
    # Formato: '@joao proativo nao-violenta "Gostaria de falar para ele que ele coda fofo"'
    name_match = re.match(r"@(\w+)", last_line)
    
    if name_match:
        name = name_match.group(1)
        
        feedback_pattern = fr"Feedback de {name.capitalize()}"
        
        filtered_feedback = []
        for line in lines[:-1]:
            if re.match(feedback_pattern, line):
                filtered_feedback.append(line)
        
        return "\n".join(filtered_feedback)
    else:
        return "Nome não encontrado."


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
