import mysql.connector


try:
    connection = mysql.connector.connect(user='root', password='@Beastmode9294',
                                         host='127.0.0.1',
                                         database='RAT',
                                         auth_plugin='mysql_native_password')
except:
    connection = mysql.connector.connect(user='root', password='    ',
                                         host='127.0.0.1',
                                         database='RAT',
                                         auth_plugin='mysql_native_password')
cursor = connection.cursor()
cursor.execute("USE RAT")


def get_ronald_chat_ids():
    cursor.execute('SELECT ronald_chat_id FROM Holders')
    ids = cursor.fetchall()
    return [u[0] for u in ids]


def get_holders_addresses(ronald_chat_id):
    cursor.execute(f"SELECT wallet_address FROM Holders WHERE ronald_chat_id = '{ronald_chat_id}';")
    addresses = cursor.fetchall()
    return [u[0] for u in addresses][0]


def add_holder(wallet_address, telegram_username, ronald_chat_id):
    print(f"{wallet_address}", f"{telegram_username}", f"{ronald_chat_id}")
    cursor.execute(f"INSERT INTO Holders (wallet_address, telegram_username, ronald_chat_id) "
                   f'VALUES ("{wallet_address}", "{telegram_username}", "{ronald_chat_id}");')
    connection.commit()


def change_holder_address_by_ronald_id(wallet_address, telegram_username):
    cursor.execute(f"UPDATE Holders SET wallet_address='{wallet_address}' WHERE ronald_chat_id LIKE '{telegram_username}';")
    connection.commit()
