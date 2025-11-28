# Alert Formatter

Um pequeno utilitário em Python com interface gráfica (Tkinter) para facilitar a formatação de alertas usados no Teams.  
O programa permite que você insira:

- Número do alerta  
- Descrição  
- Link do Dynatrace (ou de outro programa de monitoramento) (opcional)

Com essas informações, o app gera automaticamente a mensagem no formato correto e já copia para a área de transferência.

---

## 🚀 Funcionalidades

- Interface simples e rápida  
- Botão **Próximo** para avançar na coleta das informações  
- Botão **Pular** para ignorar campos opcionais (como o link do Dynatrace)  
- Botão **Concluir** que gera a mensagem final  
- Mensagem já fica disponível para colar no Teams  
- Não utiliza bibliotecas externas — apenas Python padrão
- Possibilidade de aprimoramento do código para necessidades individuais.

---

## 🖥️ Como rodar o projeto

1. Certifique-se de ter o **Python 3.8+** instalado.
2. Baixe o projeto ou clone o repositório:
   ```bash
   git clone https://github.com/GustavoAlves-dev/alert-formatter.git
