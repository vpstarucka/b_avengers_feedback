from slack_sdk import WebClient
from slack_sdk.errors import SlackApiErrordef 

tarefa():
    # Inicializa o cliente com o token do bot
    client = WebClient(token="token")    
    try:
        # Adiciona um lembrete usando parâmetros nomeados, em vez de um dicionário
        response = client.reminders_add(
            text='Lembrete periódico',  # Texto do lembrete
            time='now',  # Hora do lembrete (exemplo: 'now', 'in 10 minutes', timestamp etc.)
            recurrence='monthly'
            team_id='C07NEDNL6T0'  # ID do canal ou time (opcional, se aplicável)
        )
        print(f"Lembrete adicionado com sucesso: {response}")
    except SlackApiError as e:
        # Tratamento de erro caso o lembrete não seja adicionado corretamente
        print(f"Erro ao adicionar lembrete: {e.response['error']}")