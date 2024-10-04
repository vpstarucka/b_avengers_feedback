# Aplicativo b_IA para o Slack

Esse aplicativo funciona diretamente no Slack, serve para as referências do bridge construirem um feedback para qualquer pessoa com o auxílio da inteligência artifical.

Também existe uma funcionalidade para avisar no canal geral em uma frequência configurável, que deve ser realizada uma rodada de feedback.

## Instalação

#### Pré-requisitos
* Para usar os modelos da OpenAI e Anthropic, você deve ter uma conta com créditos suficientes.
* Para usar os modelos do Vertex, você deve ter um projeto no Google Cloud Provider com créditos suficientes.

#### Criar um aplicativo para o Slack
1. Acesse https://api.slack.com/apps/new e escolha "From an app manifest"
2. Escolha o workspace no qual você deseja instalar o aplicativo
3. Copie o conteúdo de manifest.json e cole no campo de texto que diz *Paste your manifest code here* (na aba JSON) e clique em Next
4. Revise a configuração e clique em Create
5. Clique em Install to Workspace e Allow na tela que aparecer em seguida. Você será redirecionado para o painel de configuração do aplicativo.

#### Environment Variables
Antes de executar o aplicativo, será necessário armazenar algumas variáveis de ambiente.

1. Abra a página de configuração do seu app, clique em **OAuth & Permissions** no menu à esquerda, e copie o Bot User OAuth Token. Armazene isso na sua variável de ambiente como `SLACK_BOT_TOKEN`.
2. Clique em **Basic Information** no menu à esquerda e siga as instruções na seção App-Level Tokens para criar um token de nível de aplicativo com o escopo `connections:write`. Copie este token e armazene como `SLACK_APP_TOKEN`.


```zsh
# Execute esses comandos no terminal. Substitua pelos seus tokens de app, bot e o token da API que você planeja usar
export SLACK_BOT_TOKEN=<your-bot-token>
export SLACK_APP_TOKEN=<your-app-token>
export OPENAI_API_KEY=<your-api-key>
```

### Setup do projeto
```zsh
# Clone o projeto
git clone https://github.com/vpstarucka/b_avengers_feedback

# Entre no diretorio do projeto
cd bolt-python-ai-chatbot

# Setup python
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Inicia a aplicação
python3 app.py
```

## Utilização

É possível gerar um feedback enviando uma mensagem diretamente para o b_IA com o seguinte padrão:

```
@nome.usuario tipo_feedback comportamento
```

Exemplo:
```
usuario.nome proativo nao-violento "Gostaria de falar para ele que ele coda mal"
```

É possível resgatar o histórico de feedback de um usuário:
```
/ultimo-feedback usuario.nome
```

## Estrutura do projeto

### `manifest.json`

`manifest.json` é uma configuração para aplicativos do Slack. Com um manifesto, você pode criar um app com uma configuração pré-definida ou ajustar a configuração de um app existente.


### `app.py`

`app.py` é o ponto de entrada para a aplicação e o arquivo que você executará para iniciar o servidor. Este projeto visa manter este arquivo o mais enxuto possível, utilizando-o principalmente como uma forma de rotear solicitações recebidas.


### `/listeners`

Toda solicitação recebida é roteada para um "listener". Dentro deste diretório, agrupamos cada listener com base no recurso da plataforma Slack utilizado, então /listeners/commands lida com solicitações de Slash Commands, /listeners/events lida com Eventos e assim por diante.

### `/ai`

* `ai_constants.py`: Define constantes usadas em todo o módulo de IA.

<a name="byo-llm"></a>
#### `ai/providers`
Este módulo contém classes para comunicação com diferentes provedores de API, como Anthropic, OpenAI e Vertex AI. Para adicionar seu próprio LLM, crie uma nova classe para ele usando o base_api.py como exemplo, e depois atualize ai/providers/__init__.py para incluir e utilizar sua nova classe para comunicação com a API.

* `__init__.py`: 
Este arquivo contém funções utilitárias para lidar com respostas das APIs dos provedores e recuperar os provedores disponíveis.
