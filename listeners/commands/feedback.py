from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from ai.providers import get_provider_response
from slack_sdk import WebClient

# Salvar usuário para mensagem final
# Adicionar palavras chave para tipo de personalidade
# Adicionar palavras chave para tipo de comunicação

"""/novofeedback @arthurwinck proativo nao-violenta "Gostaria de falar para ele que ele coda mal" """
"""/feedback @user comportamento"""

# > Crie um feedback para uma pessoa que tem as seguintes caracts: "${input}".
# ${feedback}

def parse_prompt(prompt: str) -> dict:
    split_prompt = prompt.split(" ")

    try:
        user_to_receive = split_prompt[0]
        person_type = split_prompt[1]
        feedback_type = split_prompt[2]
        behavior = split_prompt[3]
    except Exception as e:
        raise Exception("Mensagem mal formatada")

    return {"usuario": user_to_receive, "tipoPessoa": person_type, "tipoFeedback": feedback_type, "comportamento": behavior}

def add_parameters(parsed_prompt: dict) -> str:
  # Adicionar na respoista
  template_prompt = f"""
    Crie um feedback a partir desse comportamento. Use o primeiro nome desse username {parse_prompt["usuario"]}
    para iniciar a mensagem de feedback. Leve em consideração essas características da pessoa que irá receber o feedback
    {parse_prompt["tipoPessoa"]} e construa o feedback seguindo esse tipo {parse_prompt["tipoFeedback"]}

    Leve em consideração os seguintes valores:

    Fazer bem feito, inclusive o café
    Buscamos nos desafiar e dedicar em todas as atividades, até mesmo no cafezinho do dia a dia.

    Compartilhar dá mais XP
    Estamos sempre compartilhando conhecimento. Acreditamos que assim todos saem ganhando.

    Ser a diferença
    Assim como nossas soluções, buscamos fazer a diferença onde estamos.

    Conectar pessoas a momentos
    Prezamos sempre pelo bem das pessoas, proporcionando momentos de qualidade.

    Explorar novos mundos
    Estamos sempre explorando e inovando para construir melhores soluções.

    O comportamento no qual o feedback vai ser criado é esse: {parse_prompt["comportamento"]}
    """
  return 

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
