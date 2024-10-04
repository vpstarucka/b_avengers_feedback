import schedule
import time
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError#

def tarefa():
    client = WebClient(token="token")# The channel ID or name where you want to send the message
    channel_id = "C07NEDNL6T0"# The bot name
    bot_name = "Bolty"# The message you want to send
    message = "Oi :D"
    try:
        # Use the chat.postMessage method to send a message to the channel
        response = client.chat_postMessage(channel=channel_id, text=message,username=bot_name)
        print("Message sent successfully!")
    except SlackApiError as e:
        # Error handling in case the message fails to send
        print(f"Error sending message: {e}")

def tempo_para_proxima_execucao():
    """Calcula o tempo restante até a próxima execução agendada."""
    proxima_execucao = schedule.next_run()  # Obtém o horário da próxima execução
    agora = datetime.now()  # Horário atual
    segundos_restantes = (proxima_execucao - agora).total_seconds()
    return max(0, segundos_restantes)

def executar()
    # Agendando a tarefa para ser executada todo dia em um horário específico
    # schedule.every().day.at("15:30").do(tarefa)
    schedule.every(2).minutes.do(tarefa)
    while True:
        schedule.run_pending()
        sleep_time = tempo_para_proxima_execucao()
        print(f"Dormindo por {sleep_time} segundos até a próxima verificação...")
        time.sleep(sleep_time)  # Dorme até a próxima execução