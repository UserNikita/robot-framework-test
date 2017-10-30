*** Settings ***
Resource    ..${/}resources${/}common.robot
Test Setup  Open api session
Test Teardown   Clear DataBase and close connection

*** Test Cases ***
Checking the possibility of subscribing the service by the client
    [Documentation]  Проверка возможности подписки клиента на услуги
    ${client}  DataBase.Get random client with positive balance
    ${user_services}  Get a list of client services connected  ${client}
    ${all_services}  Get a list of all available services
    ${unconnected_service}  Get a service not connected to the client  ${user_services}  ${all_services}
    ${response_status_code}  Connect the service to the client  ${client}  ${unconnected_service}
    Should be equal as strings  ${response_status_code}  202
    Wait Until Keyword Succeeds  1 min  1 s  Check if the service is connected  ${client}  ${unconnected_service}
    ${expected_client_balance}  Get expected client balance  ${client}  ${unconnected_service}
    ${real_client_balance}  DataBase.Get balance by client  ${client}
    Should be equal as money  ${expected_client_balance}  ${real_client_balance}
