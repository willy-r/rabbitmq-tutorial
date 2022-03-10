# Sobre RabbitMQ

O RabbitMQ é um mediador de mensagens (broker), no caso as mensagens são dados binários (blobs) sendo transitado. Ele fica no meio entre receber a mensagem e a entrega da mesma. A diferença é que ele cuida das 3 partes.


## Separação e jargões

- Quem envia a mensagem é chamado de **Producer**, pode ser um programa por exemplo.
- Quem recebe a mensagem é chamado de **Consumer**. Ele é um programa que espera para receber mensagens.
- **Exchange** serve pra decidir o que vai fazer com a mensagem que foi enviada pelo **Consumer**.
- Entre o **Producer** e o **Consumer** existe a **Queue** que nada mais é que uma fila que existe dentro do RabbitMQ, essa fila recebe mensagens que podem ser enviadas e salvas dentro da fila. Vários **Producers** podem enviar mensagens para uma **Queue** e vários **Consumers** podem tentar receber mensagens de uma fila.


## Round-robin

RabbitMQ envia cada mensagem para o próximo consumer, em sequência. Cada consumer receberá a mesma quantidade de mensagens.
