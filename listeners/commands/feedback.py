from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from ai.providers import get_provider_response
from slack_sdk import WebClient
from ..model.types import getTipoFeedbackTextByEnum, TipoFeedback

def parse_prompt(prompt: str) -> dict:
    split_prompt = prompt.split(" ")

    try:
        user_to_receive = split_prompt[0]
        person_type = split_prompt[1]
        feedback_type = split_prompt[2]

        # feedback_type = getTipoFeedbackTextByEnum()

        behavior = split_prompt[3]
    except Exception as e:
        raise Exception("Mensagem mal formatada")

    return {"usuario": user_to_receive, "tipoPessoa": person_type, "tipoFeedback": feedback_type, "comportamento": behavior}

def add_parameters(parsed_prompt: dict) -> str:
  # Adicionar na respoista
  template_prompt = f"""
    Considerando um profissional de uma empresa de TI, me auxilie a dar um feedback para um colega a 
    partir do seguinte comportamento que observei por parte dele (lembre-se que esse é o ponto fundamental desse texto): {parsed_prompt["comportamento"]}.
    Use o primeiro nome desse username: {parsed_prompt["usuario"]}
    para iniciar a mensagem de feedback. Leve em consideração que você irá criar um feedback para o seguinte perfil de pessoa:
    {parsed_prompt["tipoPessoa"]}. Com base no perfil de pessoa, crie um feedback adequado. Construa o feedback seguindo esse modelo de feedback existente (SCI, CNV ou espontâneo): {parsed_prompt["tipoFeedback"]}
    """
  return template_prompt

def novofeedback(client: WebClient, ack: Ack, command, say: Say, logger: Logger, context: BoltContext):    
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
            parsed_prompt = parse_prompt(prompt)
            final_prompt = add_parameters(parsed_prompt)


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
                                "elements": [{"type": "text", "text": get_provider_response(user_id, final_prompt)}],
                            },
                        ],
                    }
                ],
            )
    except Exception as e:
        logger.error(e)
        client.chat_postEphemeral(channel=channel_id, user=user_id, text=f"Received an error from Bolty:\n{e}")
