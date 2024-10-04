from ai.ai_constants import DM_SYSTEM_CONTENT
from ai.providers import get_provider_response
from logging import Logger
from slack_bolt import Say
from slack_sdk import WebClient
from ..listener_utils.listener_constants import DEFAULT_LOADING_TEXT
from ..listener_utils.parse_conversation import parse_conversation

"""
Handles the event when a direct message is sent to the bot, retrieves the conversation context,
and generates an AI response.
"""

def parse_prompt(prompt: str) -> dict:
    split_prompt = prompt.split(" ")

    try:
        user_to_receive = split_prompt[0]
        feedback_type = split_prompt[1]
        behavior = split_prompt[2]
    except Exception as e:
        raise Exception("Mensagem mal formatada")

    return {"usuario": user_to_receive, "tipoFeedback": feedback_type, "comportamento": behavior}

def add_parameters(parsed_prompt: dict) -> str:
  # Adicionar na respoista
  template_prompt = f"""
    Considerando um profissional de uma empresa de TI, construa uma mensagem para dar de feedback para um colega a 
    partir do seguinte comportamento que observei por parte dele (lembre-se que esse é o ponto fundamental desse texto): {parsed_prompt["comportamento"]}.
    Use o primeiro nome desse username: {parsed_prompt["usuario"]}
    para iniciar a mensagem de feedback. Construa o feedback seguindo esse modelo de feedback existente (SCI, CNV ou espontâneo): {parsed_prompt["tipoFeedback"]}.
    No final da mensagem adicione "Feedback para {parsed_prompt["usuario"]}"
    """
  return template_prompt

def app_messaged_callback(client: WebClient, event: dict, logger: Logger, say: Say):
    channel_id = event.get("channel")
    thread_ts = event.get("thread_ts")
    user_id = event.get("user")
    text = event.get("text")

    try:
        if event.get("channel_type") == "im":
            conversation_context = ""

            if thread_ts:  # Retrieves context to continue the conversation in a thread.
                conversation = client.conversations_replies(channel=channel_id, limit=10, ts=thread_ts)["messages"]
                parsed_prompt = conversation[:-1]
                
                conversation_context = parse_conversation(add_parameters(parsed_prompt))

            waiting_message = say(text=DEFAULT_LOADING_TEXT, thread_ts=thread_ts)
            response = get_provider_response(user_id, text, conversation_context, DM_SYSTEM_CONTENT)
            client.chat_update(channel=channel_id, ts=waiting_message["ts"], text=response)
    except Exception as e:
        logger.error(e)
        client.chat_update(channel=channel_id, ts=waiting_message["ts"], text=f"Received an error from Bolty:\n{e}")
