import sqlite3


def check_type_and_fare(user_bot_id):
    acc_type = get_acc_type(user_bot_id)
    fare_count = get_fare_count(user_bot_id)
    if acc_type == 'demo':
        if fare_count > 0:
            return True
        else:
            return False
    else:      #== 'full'
        return True


def get_acc_type(user_bot_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    acc_type = c.execute("SELECT acc_type FROM user_bot_data WHERE id = :id", {'id': user_bot_id}).fetchone()
    c.close
    return acc_type[0]


def get_fare_count(user_bot_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    fare_count = c.execute("SELECT fare FROM user_bot_data WHERE id = :id", {'id': user_bot_id}).fetchone()
    return fare_count[0]


def decrease_fare_count(user_bot_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE user_bot_data SET fare = fare - 1 WHERE id = :id", {'id': user_bot_id}).fetchone()
    conn.commit()
    c.close()
    return True


def get_user_bot_data():
    user_name = input("Enter your CHCleaner username: ")
    user_pwd = input("Enter your CHCleaner password: ")
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    resp = c.execute("SELECT * FROM user_bot_data WHERE user_name = :username and password = :pwd",
                     {'username': user_name, 'pwd': user_pwd}).fetchone()
    if resp is None:
        print("Something went wrong. Please, contact administrator (error code: 1)")
        conn.close()
        return False

    act_status = resp[3]  # get is_active value
    if act_status != 1: # if not active
            print("Something went wrong. Please, contact administrator (error code: 2)")
            conn.close()
            return False
    conn.close()
    return resp[0]  # return id


def get_user_ch_data(id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    resp = c.execute("SELECT * FROM user_ch_data WHERE user_bot_id = :id",
                     {'id': id}).fetchone()
    user_id = resp[0]
    user_token = resp[1]
    user_device = resp[2]
    conn.close()
    return user_id, user_token, user_device


def write_user_ch_data(id, token, device, bot_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE user_ch_data SET user_id = :id, user_token = :token, user_device = :device WHERE user_bot_id = :bot_id", {'id': id, 'token': token, 'device': device, 'bot_id': bot_id})
    conn.commit()