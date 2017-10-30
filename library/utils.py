from robot.libraries.BuiltIn import assert_equal


class ServiceNotConnectedException(Exception):
    pass


def should_be_equal_as_money(first, second):
    """Функция для проверки равенства денежных сумм"""
    first = round(first, 2)
    second = round(second, 2)
    assert_equal(first, second)


def get_a_service_not_connected_to_the_client(client_services, all_services):
    """Получить услугу, которая не подключена клиенту"""
    unconnected_service = None
    service_ids = [service['id'] for service in client_services['items']]
    for client_service in all_services['items']:
        if client_service['id'] not in service_ids:
            unconnected_service = client_service
            break
    return unconnected_service


def check_if_the_service_was_connected(unconnected_service, client_services):
    """Проверить была ли подключена клиенту услуга"""
    unconnected_service_id = unconnected_service['id']
    services_ids = [service['id'] for service in client_services['items']]
    if unconnected_service_id not in services_ids:
        raise ServiceNotConnectedException('Услуга не была подключена')


def get_expected_client_balance(client, service):
    """Проверить текущий баланс клиента"""
    expected_client_balance = client['balance'] - service['cost']
    return expected_client_balance
