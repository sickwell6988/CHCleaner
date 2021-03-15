def cleanup_account_data():
    open(file="setting.ini", mode="w").close()
    return True


def cleanup_headers(client):
    client.HEADERS.pop('CH-UserID')
    client.HEADERS.pop('Authorization')
    client.HEADERS.pop('CH-DeviceId')
    return True


def cleanup_auth_session(client):
    cleanup_account_data()
    cleanup_headers(client)
    return True