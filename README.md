# Yandex BS Task Part 2

## Requirements

Для установки приложения на чистой системе требуются следующие приложения:
- Docker
- Docker Compose
- Containerd (для Linux систем)

Инструкции по установке описаны на [этих](https://docs.docker.com/install/) [страницах](https://docs.docker.com/compose/install/)


Библиотеки, используемые для запуска приложения описаны в папке `requirements`

## Commands

### Запуск приложения

Hеобходимо перейти в папку с приложением и выполнить следующие команды:

1) `sudo docker-compose -f production.yml build`
2) `sudo docker-compose -f production.yml up`

После этого приложение становится доступным по адресу `0.0.0.0:8080`

###Запуск тестов

`sudo docker-compose -f local.yml  run --rm django pytest`