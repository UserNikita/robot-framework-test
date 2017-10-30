import sqlite3


class DataBase:
    _GET_CLIENTS_WITH_A_POSITIVE_BALANCE_SQL = """
        SELECT * FROM clients
        INNER JOIN balances
        ON clients.client_id = balances.clients_client_id
        WHERE balances.balance > 0 AND CLIENTS.CLIENT_ID NOT IN (
            SELECT clients_client_id FROM (
                SELECT CLIENTS_CLIENT_ID, count(*) AS count_client_services FROM CLIENT_SERVICE
                GROUP BY CLIENTS_CLIENT_ID
                ) AS table1
            WHERE table1.count_client_services = (SELECT count(*) FROM SERVICES)
        )
        ORDER BY random()
        LIMIT 1
    """
    _GET_CLIENT_BY_ID_SQL = """
        SELECT * FROM clients
        INNER JOIN balances
        ON clients.client_id = balances.clients_client_id
        WHERE clients.client_id = ?
    """
    _GET_MAX_CLIENT_ID_SQL = """
        SELECT max(client_id) as max_id FROM clients
    """
    _CREATE_CLIENT_SQL = """
        INSERT INTO clients (client_name)
        VALUES (?)
    """
    _CREATE_CLIENT_BALANCE_SQL = """
        INSERT INTO balances (clients_client_id, balance)
        VALUES (?, ?)
    """
    _DELETE_CLIENT_BALANCE_SQL = """
        DELETE FROM balances
        WHERE balances.clients_client_id = ?
    """
    _DELETE_CLIENT_SERVICE_SQL = """
        DELETE FROM client_service
        WHERE client_service.clients_client_id = ?
        AND services_service_id = ?
    """
    _DELETE_CLIENT_SQL = """
        DELETE FROM clients
        WHERE clients.client_id = ?
    """
    _RESTORE_BALANCE_SQL = """
        UPDATE balances
        SET balance = ?
        WHERE clients_client_id = ?
    """

    def __init__(self, db_path):
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = self._dict_row_factory
        self._cursor = self._connection.cursor()
        self._client_has_been_created = False
        self._client_balance = None

    @staticmethod
    def _dict_row_factory(cursor, row):
        """Фабрика, создающая словари из записей, выбранных из БД"""
        dict_row = {}
        for column, row_element in zip(cursor.description, row):
            dict_row[column[0].lower()] = row_element
        return dict_row

    def _create_client_with_positive_balance(self):
        """Создать пользователя с балансом 5"""
        client_name = 'Bob Marley'
        balance = 5
        self._cursor.execute(self._CREATE_CLIENT_SQL,
                             (client_name,))
        client_id = self._cursor.lastrowid
        self._cursor.execute(self._CREATE_CLIENT_BALANCE_SQL,
                             (client_id, balance))
        self._connection.commit()
        client = {
            'client_id': client_id,
            'balance': balance,
        }
        return client

    def get_random_client_with_positive_balance(self):
        """Получить случайного пользователя с положительным балансом"""
        clients = self._cursor.execute(
            self._GET_CLIENTS_WITH_A_POSITIVE_BALANCE_SQL).fetchall()
        if clients:
            client = clients[0]
            self._client_balance = client['balance']
        else:
            client = self._create_client_with_positive_balance()
            self._client_has_been_created = True
        return client

    def _get_client_by_id(self, client_id):
        """Получить пользователя по его id"""
        users = self._cursor.execute(
            self._GET_CLIENT_BY_ID_SQL, (client_id,)).fetchall()
        return users[0]

    def get_balance_by_client(self, client):
        """Получаем баланс по ID клиента"""
        client_id = client['client_id']
        client = self._get_client_by_id(client_id)
        balance = client['balance']
        return balance

    def _delete_client_balance(self, client_id):
        """Удалить баланс клиента"""
        self._cursor.execute(self._DELETE_CLIENT_BALANCE_SQL, (client_id,))

    def _delete_client_service(self, client_id, service_id):
        """Удаление связей между клиентом и услугами"""
        self._cursor.execute(self._DELETE_CLIENT_SERVICE_SQL,
                             (client_id, service_id))

    def _delete_client(self, client_id):
        """Удалить клиента"""
        self._cursor.execute(self._DELETE_CLIENT_SQL, (client_id,))

    def _restore_client_balance(self, client_id, client_balance):
        """Восстановить баланс клиента"""
        self._cursor.execute(self._RESTORE_BALANCE_SQL,
                             (client_balance, client_id))

    def clean(self, client, service):
        """Очистить базу данных после выполнения тестов"""
        client_id = client['client_id']
        service_id = service['id']
        if self._client_has_been_created:
            self._delete_client_service(client_id, service_id)
            self._delete_client_balance(client_id)
            self._delete_client(client_id)
        else:
            self._delete_client_service(client_id, service_id)
            self._restore_client_balance(client_id, self._client_balance)
        self._connection.commit()

    def close(self):
        """Закрыть соединение с базой данных"""
        self._connection.close()
