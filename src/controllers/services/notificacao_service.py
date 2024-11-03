#!/usr/bin/env python
import pika, sys, os, json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(alerta):
    # Configuração do servidor SMTP (Gmail como exemplo)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'testes203.l2@gmail.com'
    sender_password = ''  # Lembre-se de usar a senha de app se usar Gmail
    recipient_email = 'gr8147972@gmail.com'  # Email para o qual será enviado o alerta

    # Criar mensagem de email
    mensagem = MIMEMultipart()
    mensagem['From'] = sender_email
    mensagem['To'] = recipient_email
    mensagem['Subject'] = f"Alerta de Preço: {alerta['produto']}"

    # Corpo do email
    corpo_email = f"""
    <html>
    <body>
        <h1>Alerta de Preço</h1>
        <p>Produto: {alerta['produto']}</p>
        <p>Preço Limite: {alerta['preco_limite']}</p>
        <p>Status: {alerta['status']}</p>
    </body>
    </html>
    """
    
    mensagem.attach(MIMEText(corpo_email, 'html'))

    # Conectar ao servidor SMTP e enviar o email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciar TLS (segurança)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, mensagem.as_string())
        server.quit()
        print(f" [x] Alerta enviado por email para {recipient_email}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

def main():
    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declarar a fila 'alertas'
    channel.queue_declare(queue='alertas')

    # Função callback que processa a mensagem recebida
    def callback(ch, method, properties, body):
        alerta = json.loads(body)  # Converte a mensagem recebida de JSON para um dicionário
        print(f" [x] Alerta Recebido: Produto: {alerta['produto']}, Preço Limite: {alerta['preco_limite']}, Status: {alerta['status']}")
        enviar_email(alerta)  # Envia o alerta via email

    # Consumir mensagens da fila 'alertas'
    channel.basic_consume(queue='alertas', on_message_callback=callback, auto_ack=True)

    print(' [*] Aguardando mensagens. Para sair, pressione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Processo interrompido')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
