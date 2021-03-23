import sqlite3


def cleanup_account_data(bot_id):
    # open(file="setting.ini", mode="w").close()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(
        "UPDATE user_ch_data SET user_id = '', user_token = '', user_device = '' WHERE user_bot_id = :bot_id",
        {'bot_id': bot_id})
    conn.commit()
    return True


def cleanup_headers(client):
    client.HEADERS.pop('CH-UserID')
    client.HEADERS.pop('Authorization')
    client.HEADERS.pop('CH-DeviceId')
    return True


def cleanup_auth_session(client, bot_id):
    cleanup_account_data(bot_id)
    cleanup_headers(client)
    return True