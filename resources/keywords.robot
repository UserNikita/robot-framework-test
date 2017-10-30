*** Settings ***
Library     RequestsLibrary

*** Keywords ***
Open api session
    [Documentation]  Создание сессии для работы с API
    Create session  api  ${SCHEMA}${HOST}:${PORT}

Get a list of client services connected
    [Documentation]  Получение услуг подключенных клиенту
    [Arguments]  ${client}
    ${data}  create dictionary  client_id=${client['client_id']}
    ${headers}  create dictionary  Content-Type=application/json
    ${response}  post request  api  /client/services  data=${data}  headers=${headers}
    ${json}  to json  ${response.text}
    [Return]  ${json}

Get a list of all available services
    [Documentation]  Получение всех доступных услуг
    ${response}  get request  api  /services
    ${json} =  to json  ${response.text}
    [Return]  ${json}

Connect the service to the client
    [Documentation]  Подключение услуги клиенту
    [Arguments]  ${client}  ${service}
    ${data}  create dictionary  client_id=${client['client_id']}  service_id=${service['id']}
    ${headers}  create dictionary  Content-Type=application/json
    ${response}  post request  api  /client/add_service  data=${data}  headers=${headers}
    [Return]  ${response.status_code}

Check if the service is connected
    [Documentation]  Проверка подключена ли услуга у клиента
    [Arguments]  ${client}  ${service}
    Set suite variable  ${CLIENT}  ${client}
    Set suite variable  ${SERVICE}  ${service}
    ${client_services}  Get a list of client services connected  ${client}
    Check if the service was connected  ${service}  ${client_services}

Clear DataBase and close connection
    [Documentation]  Удаление пользователя, если он был создан
    DataBase.Clean  ${CLIENT}  ${SERVICE}
    DataBase.Close
