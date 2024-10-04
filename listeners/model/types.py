from enum import Enum

class TipoFeedback(Enum):
    SCI = 1,
    CNV = 2,
    ESPONTANEO = 3

def getTipoFeedbackTextByEnum(tipoFeedback: TipoFeedback) -> str:
    if tipoFeedback == TipoFeedback.SCI:
        return """
          Modelo SCI
          O modelo SCI é composto por três etapas: Situação, Comportamento, Impacto

          Também é conhecido como CCC: Contexto, Comportamento, Consequência

          Independente do nome, esse tipo de feedback estruturado buscará identificar qual foi o comportamento do bridger, em determinada situação e o impacto gerado a partir dele. Esses três pontos são essenciais para passar uma mensagem assertiva.

          S (Situação) - identifique a situação
          C (Comportamento) - descreva o comportamento
          I (Impacto) - Comunique o impacto desse comportamento
        """
    elif tipoFeedback == TipoFeedback.CNV:
        return """
          CNV como ferramenta de diálogo
          Outra ferramenta que pode ser utilizada como um meio para formular um feedback é a Comunicação Não-Violenta (CNV). Diferente de alguns modelos clássicos de feedback, a CNV é um método de linguagem e comunicação menos impessoal, visto que necessita a expressão de sentimentos e necessidades daquele que sentiu algum incômodo com o comportamento de outro.

          É interessante utilizar esse método dentro de equipes em que se busca uma maior aproximação entre os membros, visto que possibilita diálogos mais pessoais.

          Ela busca ser uma comunicação mais consciente e honesta sobre nossos sentimentos e desejos, frente ao hábito de reações repetitivas e respostas automáticas.

          A CNV  funciona a partir de 4 passos:
          1. Observação: sem avaliações e julgamentos
          2 - Expressão de sentimentos
          3 - Expressão de necessidades
          4 - Comunicação de um pedido claro e específico
        """
    else:
        return """
          Você pode fazer de forma natural, sem nenhum modelo estruturado, o que: 

          Deixa a comunicação mais espontânea, sem aquele ar muito formal;
          Possibilita desenvolver o assunto na medida que você preferir;
          Não precisa ser planejado com antecedência;
          É mais simples para se tratar de situações corriqueiras, que não exigirão um grande esforço para serem resolvidas;
        """