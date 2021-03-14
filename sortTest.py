def get_mutual_ids():
    mutual_data = []
    for user in mutual:
        mutual_data.append(user[0])
    return mutual_data


mutual = [(1803970164, 'Екатерина  Путина'), (1726256219, 'Oleg Vihrov'), (1361818758, 'Святослав Муравский'), (851837463, 'Max Chumanov'), (804641627, 'Marina Popova-Bednaya'), (497730412, 'Nastya Gno'), (495929358, 'Сандро Geomen'), (478973006, 'Мнацик Мнацаканян'), (476644570, 'Светлана Викторовна'), (92445489, 'Viacheslav Novikov')]
following = [(1803970164, 'Екатерина  Путина'), (1746750099, 'Anna Zajcev'), (1726256219, 'Oleg Vihrov'), (1598143186, 'Masha Mars'), (1586387928, 'Evgen Fediv'), (1361818758, 'Святослав Муравский'), (1244166827, 'Yaroslava Mincheva'), (851837463, 'Max Chumanov'), (804641627, 'Marina Popova-Bednaya'), (497730412, 'Nastya Gno'), (495929358, 'Сандро Geomen'), (478973006, 'Мнацик Мнацаканян'), (476644570, 'Светлана Викторовна'), (404815727, 'PAVEL Surshkov'), (371323680, 'Станислав Жаков'), (340909194, 'Anasteysha Sindi'), (250812371, 'Oksana Myhaylyshyn'), (217562941, 'Ирина Куликова'), (92445489, 'Viacheslav Novikov'), (3723590, 'Renata George')]

mutual_ids = get_mutual_ids()

non_mutual = [i for i in following if not i[0] in mutual_ids]
print(non_mutual)