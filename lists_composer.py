def compose_user_table(data_from_api) :
    user_dict_list = list(data_from_api['users'])

    def append_user_data(user_data) :
        data_list = []
        for dicts in user_dict_list :
            data_list.append(dicts[user_data])
        return data_list

    user_id_list = append_user_data(user_data='user_id')
    user_name_list = append_user_data(user_data='name')
    user_data_list = list(zip(user_id_list, user_name_list))
    user_data_list_sorted = sorted(user_data_list, key=lambda user :user[0], reverse=True)

    return user_data_list_sorted


def compose_non_mutual_user_table(data_from_api_following, data_from_api_mutual) :
    following_dict = compose_user_table(data_from_api_following)
    mutual_dict = compose_user_table(data_from_api_mutual)

    def get_mutual_ids() :
        mutual_data = []
        for user in mutual_dict :
            mutual_data.append(user[0])
        return mutual_data

    mutual_ids = get_mutual_ids()
    non_mutual = [i for i in following_dict if not i[0] in mutual_ids]

    return non_mutual


def compose_non_mutual_user_table_v2(data_from_api_following, data_from_api_follower) :
    following_dict = compose_user_table(data_from_api_following)
    follower_dict = compose_user_table(data_from_api_follower)

    def get_follower_ids() :
        follower_data = []
        for user in follower_dict:
            follower_data.append(user[0])
        return follower_data

    follower_ids = get_follower_ids()
    non_mutual = [i for i in following_dict if not i[0] in follower_ids]

    return non_mutual
