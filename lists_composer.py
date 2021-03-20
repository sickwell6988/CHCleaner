def compose_user_table(data_from_api) :
    user_dict_list = data_from_api

    def append_user_data(user_data):
        data_list = []
        for dicts in user_dict_list:
            data_list.append(dicts[user_data])
        return data_list

    user_id_list = append_user_data(user_data='user_id')
    user_nick_list = append_user_data(user_data='username')
    user_name_list = append_user_data(user_data='name')

    user_data_list = list(zip(user_id_list, user_nick_list, user_name_list))
    user_data_list_sorted = sorted(user_data_list, key=lambda user:user[0], reverse=True)

    return user_data_list_sorted


def compose_non_mutual_user_table(data_from_api_following, data_from_api_mutual):
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


# def compose_non_mutual_user_table_v2(data_from_api_following, data_from_api_followers) :
#     following_dict = compose_user_table(data_from_api_following)
#     follower_dict = compose_user_table(data_from_api_followers)
#
#     # following_dict = str(tabulate.tabulate(following_dict, headers=["#", "Id", "Username", "Name"], showindex=True, tablefmt="pretty")).encode(encoding='utf-8')
#     # follower_dict = str(tabulate.tabulate(follower_dict, headers=["#", "Id", "Username", "Name"], showindex=True, tablefmt="pretty")).encode(encoding='utf-8')
#     #
#     # open(file="C:/Users/nikita.panada/OneDrive - Algosec Systems Ltd/Desktop/asdasd/followings2.txt", mode="wb").write(following_dict)
#     # open(file="C:/Users/nikita.panada/OneDrive - Algosec Systems Ltd/Desktop/asdasd/follower_dict.txt", mode="wb").write(follower_dict)
#
#     def get_follower_ids() :
#         follower_data = []
#         for user in follower_dict:
#             follower_data.append(user[0])
#         return follower_data
#
#     follower_ids = get_follower_ids()
#     non_mutual = [i for i in following_dict if not i[0] in follower_ids]
#
#     return non_mutual