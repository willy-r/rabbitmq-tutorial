docker run -d --name rabbitmq_studies --hostname bugs_bunny -p 5672:5672 -p 8080:15672 -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest rabbitmq:management