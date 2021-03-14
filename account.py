from clubhouse.clubhouse import Clubhouse

client = Clubhouse()


def cleanup_account_data():
    open(file="setting.ini", mode="w").close()
    return True


def cleanup_headers():
    client.HEADERS.pop('CH-UserID')
    client.HEADERS.pop('Authorization')
    client.HEADERS.pop('CH-DeviceId')
    return True


def cleanup_auth_session():
    cleanup_account_data()
    cleanup_account_data()
    return True
