import sqlite3


def get_user_bot_data():
    user_name = input("Enter your CHCleaner username: ")
    user_pwd = input("Enter your CHCleaner password: ")
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    resp = c.execute("SELECT * FROM user_bot_data WHERE user_name = :username and password = :pwd",
                     {'username': user_name, 'pwd': user_pwd}).fetchone()
    act_status = resp[3]  # get is_active value
    if act_status != 1:
        print("Something went wrong. Please, contact administrator")
        conn.close()
        return False
    conn.close()
    return resp[0]  # return id


def get_user_ch_data(id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    resp = c.execute("SELECT * FROM user_ch_data WHERE user_bot_id = :id",
                     {'id': id}).fetchone()
    print(resp)
    user_id = resp[0]
    user_token = resp[1]
    user_device = resp[2]
    conn.close()
    return user_id, user_token, user_device


def write_user_ch_data(id, token, device, bot_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    resp = c.execute("UPDATE user_ch_data SET user_id = :id, user_token = :token, user_device = :device WHERE user_bot_id = :bot_id", {'id': id, 'token': token, 'device': device, 'bot_id': bot_id})
    conn.commit()
    print(resp)