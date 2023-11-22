# Test Flask project

## Table of Contents

- [CI-status](#status)
- [Restfull api](#getting_started)
- [Swagger](#swagger)
- [Testing](#test)

## CI-status <a name = "status"></a>

ci status - [![CircleCI](https://dl.circleci.com/status-badge/img/gh/apimanov/flask-sqlite3-todo-crud.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/apimanov/flask-sqlite3-todo-crud)

## Rest api <a name = "rest"></a>
    endpoints:
      /api/task
        - GET получить список всех задач
        - PUT in body {'description':'new task'} создать новую задачу
        - DELETE in query 'id'=int удалить задачу


## Swagger <a name = "Swagger"></a>
URI swagger
  * swagger yml - /swagger
  * swagger ui - /swagger-ui


[Используется версия сваггера 2.0](https://editor.swagger.io/?url=https://raw.githubusercontent.com/apimanov/flask-sqlite3-todo-crud/master/swagger.yml)


## Testing <a name = "testing"></a>

Dredd генерирует тесты на основе swagger спецификации

### Test results <a name = "test_results"></a>

[Отчет dredd](report.md)
