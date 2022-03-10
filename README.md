# Sobre o RabbitMQ

O RabbitMQ é um mediador de mensagens (broker), no caso as mensagens são dados binários (blobs) sendo transitados. Ele fica no meio entre receber a mensagem e a entrega da mesma. A diferença é que ele cuida das 3 partes.


## Separação e jargões

- Quem envia a mensagem é chamado de **Producer**, pode ser um programa por exemplo.
- Quem recebe a mensagem é chamado de **Consumer**. Ele é um programa que espera para receber mensagens.
- **Exchange** serve pra decidir o que vai fazer com a mensagem que foi enviada pelo **Consumer**.
- Entre o **Producer** e o **Consumer** existe a **Queue** que nada mais é que uma fila que existe dentro do RabbitMQ, essa fila recebe mensagens que podem ser enviadas e salvas dentro da fila. Vários **Producers** podem enviar mensagens para uma **Queue** e vários **Consumers** podem tentar receber mensagens de uma fila.


## Sobre o repo e configurações

**O repositório foi baseado no [tutorial do RabbitMQ para o Python](https://www.rabbitmq.com/tutorials/tutorial-one-python.html).**

Para rodar, é interessante ter o Python 3.9+.

Tenha o Docker instalado na sua máquina (Linux por favor nunca te pedi nada) e rode o servidor do RabbitMQ:

```bash
bash run-rabbitmq.sh
```

> Para facilmente remover o container você pode rodar `bash rm-rabbitmq.sh` no terminal também.

Crie um ambiente virtual, inicialize ele, e instale as dependências:

```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Agora é só rodar o script e testar o RabbitMQ, para cada parte do tutorial foram desenvolvidos sempre 2 arquivos: um que é o consumer e o outro que é o producer.


## Exemplos rodando cada script

[Tutorial um: "Hello World!"](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)

```bash
python send.py
python receive.py
```

[Tutorial dois: Work Queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)

```bash
python new_task.py "A very hard task which takes three seconds..."
python worker.py
``` 

[Tutorial três: Publish/Subscribe](https://www.rabbitmq.com/tutorials/tutorial-three-python.html)

```bash
python receive_logs.py
python emit_log.py "info: This is the log message"
```

[Tutorial quatro: Routing](https://www.rabbitmq.com/tutorials/tutorial-four-python.html)

```bash
python receive_logs_direct.py info
python emit_log_direct.py info "The message"
```

[Tutorial cinco: Topics](https://www.rabbitmq.com/tutorials/tutorial-five-python.html)

```bash
python receive_logs_topic.py "*.rabbit"
python emit_log_topic.py red.rabbit Hello
```

[Tutorial seis: RPC](https://www.rabbitmq.com/tutorials/tutorial-six-python.html)

```bash
python rpc_server.py
python rpc_client.py
```
