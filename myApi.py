from tkinter import messagebox

import mysql
from mysql.connector import Error

# details of database:
db_name = "mydatabase"
user = "root"
pas = "ilanAmitOhad"
host = '127.0.0.1'
port = '3307'


# in this function we send queries to the DB:
def get_sql_func(query, func):
    try:
        connection = mysql.connector.connect(
            user=user, host=host, port=port, database=db_name
            , password=pas
        )
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        if func is not None:
            func()
    except Error as e:
        messagebox.showerror("Error", f"Error while connecting to MySQL: {e}")
    finally:
        connection.close()
    return results


def user_and_friends(user_id):
    """
    this function get user_id, and return a list of tuples which each tuple represents a friend and contain
    his id and his name
    input: user_id (int)
    output: list of tuples(id- int, name- string)
    """
    friends_list = []
    query = f'SELECT * FROM friends WHERE user_id_1 = {user_id} OR user_id_2 = {user_id}'
    items = get_sql_func(query, None)
    for index, item in enumerate(items):
        if item[1] != user_id:
            query = f'SELECT * FROM users WHERE id = {item[1]}'
        else:
            query = f'SELECT * FROM users WHERE id = {item[2]}'
        friend_item = get_sql_func(query, None)
        friend_id = friend_item[0][0]
        friend_name = friend_item[0][1]
        friends_list.append((friend_id, friend_name))
    return friends_list


def get_likes(squad_id, num):
    """
    this function gets squad_id and returns the amount of likes it has. in case of num that is different than zero,
    it also adds like to this squad.
    input: squad_id - int, num - int
    output - amount of likes - int
    """
    if num != 0:
        add_like_query = f'UPDATE user_squads ' \
                          f'SET likes = likes + 1 ' \
                          f'WHERE id = {squad_id}'
        try:
            connection = mysql.connector.connect(
                user=user, host=host, port=port, database=db_name
                , password=pas
            )
            cursor = connection.cursor()
            cursor.execute(add_like_query)
            connection.commit()
            cursor.close()
        except Error as e:
            messagebox.showerror("Error", f"Error while connecting to MySQL: {e}")
        finally:
            connection.close()
    likes = get_sql_func(f'SELECT likes FROM user_squads WHERE id = {squad_id}', None)[0][0]
    return likes


def get_players_squad(squad_id):
    # Query to get the players in the selected squad
    query = f'SELECT short_name, overall, player_positions FROM players_season ' \
            f'JOIN user_squad_players ON players_season.id_season = user_squad_players.id_player ' \
            f'JOIN players ON players_season.id_player = players.id_player ' \
            f'WHERE user_squad_players.user_squad_id = {squad_id}'
    players = get_sql_func(query, None)
    return players


def get_list_squads(user_id):
    # Retrieve list of squads from database
    squads = get_sql_func(f"SELECT id, squad_name FROM user_squads WHERE user_id = {user_id}", None)
    return squads


# this function is for adding a new friend:
def add_friend(user_id, friend_name):
    query = f'SELECT * FROM users WHERE username = \'{friend_name}\''
    results = get_sql_func(query, None)
    if results:
        try:
            connection = mysql.connector.connect(
                user=user, host=host, port=port, database=db_name
                , password=pas
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO friends(user_id_1, user_id_2) VALUES(%s, %s)", (user_id, results[0][0]))
            connection.commit()
            cursor.close()
        except Error as e:
            messagebox.showerror("Error", f"Error while connecting to MySQL: {e}")
        finally:
            connection.close()
    else:
        messagebox.showinfo("fail", "username does not exist")


def insert_squad_sql(user_id, squad_players, squad_name):
    try:
        connection = mysql.connector.connect(
            user=user, host=host, port=port, database=db_name
            , password=pas
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user_squads(user_id, squad_name, likes) VALUES(%s, %s, %s)", (user_id,
                                                                                                  squad_name.get(), 0))

        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror("Error", f"Error while connecting to MySQL: {e}")
    finally:
        connection.close()

    squad_id = get_sql_func('SELECT MAX(id) FROM user_squads;', None)[0][0]
    for player in squad_players:
        player_q = f'SELECT id_season FROM players_season ' \
                   f'JOIN players ON players_season.id_player = players.id_player ' \
                   f'WHERE short_name = \'{player[0]}\' AND season = {player[-1]};'
        player_details = get_sql_func(player_q, None)[0]
        try:
            connection = mysql.connector.connect(
                user=user, host=host, port=port, database=db_name
                , password=pas
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO user_squad_players(user_squad_id, id_player) "
                           "VALUES(%s, %s)", (squad_id, player_details[0]))
            connection.commit()
            cursor.close()
        except Error as e:
            messagebox.showerror("Error", f"Error while connecting to MySQL: {e}")
        finally:
            connection.close()


def player_data(player_details):
    query = "SELECT short_name, overall, nationality_name, value_eur, wage_eur, age, player_positions, potential," \
            " season" \
            " FROM" \
                " (SELECT players.short_name, players_season.overall, nations.nationality_name," \
                " players_season.value_eur, players_season.wage_eur, players_season.age" \
                ", players_season.player_positions, players_season.potential," \
                " players_season.season FROM players " \
                "JOIN players_season ON players.id_player = players_season.id_player " \
                f"JOIN nations ON players.nationality_id = nations.nationality_id " \
                f"WHERE short_name = '{player_details[0]}' AND season = {player_details[-1]}) as subquery;"
    data = get_sql_func(query, None)
    return data


def find_players(dic_data, name, by_type):
    query = ''
    # define the query:
    if by_type == 1:
        # query for players
        query = "SELECT short_name, overall, nationality_name, value_eur, wage_eur, age, player_positions, potential," \
                " season" \
                " FROM" \
                    " (SELECT players.short_name, players_season.overall, nations.nationality_name," \
                    " players_season.value_eur, players_season.wage_eur, players_season.age" \
                    ", players_season.player_positions, players_season.potential," \
                    " players_season.season FROM players " \
                    "JOIN players_season ON players.id_player = players_season.id_player " \
                    "JOIN nations ON players.nationality_id = nations.nationality_id"
    elif by_type == 2:
        # query for teams:
        query = "SELECT DISTINCT short_name, club_name, overall, nationality_name, value_eur, wage_eur, age," \
                " player_positions, potential, season FROM" \
                    " (SELECT players.id_player, players.short_name, players_season.overall," \
                    " nations.nationality_name, teams.club_name, players_season.value_eur, players_season.wage_eur," \
                    " players_season.age, players_season.player_positions, players_season.potential," \
                    " players_season.season FROM players " \
                    "JOIN players_season ON players.id_player = players_season.id_player " \
                    "JOIN nations ON players.nationality_id = nations.nationality_id " \
                    "JOIN teams ON players_season.club_team_id = teams.club_team_id " \
                    "JOIN teams_season ON players_season.club_team_id = teams_season.club_team_id"
    else:
        # query for leagues:
        query = "SELECT DISTINCT short_name, club_name, league_name, overall, nation, value_eur, wage_eur," \
                " age, player_positions, potential, season FROM" \
                    " (SELECT players.id_player, players.short_name, players_season.overall," \
                    " leagues.nation, teams.club_name, players_season.value_eur, players_season.wage_eur," \
                    " teams_season.league_name, players_season.age, players_season.player_positions," \
                    " players_season.potential, players_season.season FROM players JOIN players_season " \
                    "ON players.id_player = players_season.id_player " \
                    "JOIN teams ON players_season.club_team_id = teams.club_team_id " \
                    "JOIN teams_season ON players_season.club_team_id = teams_season.club_team_id " \
                    "AND players_season.season = teams_season.season " \
                    "JOIN leagues ON teams_season.league_name = leagues.league_name"
    flag = False
    s = 'players_season.season'
    if by_type == 1:
        s = 'season'
    my_filter = ' WHERE '
    for k in dic_data:
        # check if the credential is filled:
        if dic_data[k]:
            # check if the credential is the first filled:
            if not flag:
                if k == 'nationality_name' or k == 'nation' or k == 'player_positions' or k == s:
                    if k == s:
                        my_filter += f'{s} =  {dic_data[k]} '
                    elif k == 'player_positions':
                        my_filter += f'{k} LIKE  \'%{dic_data[k]}%\' '
                    else:
                        my_filter += f'{k} =  \'{dic_data[k]}\' '
                else:
                    my_filter += f'{k} >  {dic_data[k]} '
                flag = True
            else:
                if k == 'nationality_name' or k == 'nation' or k == 'player_positions' or k == s:
                    if k == s:
                        my_filter += f'AND {s} = {dic_data[k]} '
                    elif k == 'player_positions':
                        my_filter += f'AND {k} LIKE \'%{dic_data[k]}%\' '
                    else:
                        my_filter += f'AND {k} = \'{dic_data[k]}\' '
                else:
                    my_filter += f'AND {k} > {dic_data[k]} '
    # check if filter is needed
    if flag:
        query += my_filter
    if name.get():
        if flag:
            if by_type == 1:
                query += f'AND short_name = \'{name.get()}\' '
            elif by_type == 2:
                query += f'AND club_name = \'{name.get()}\' '
            else:
                query += f'AND league_name = \'{name.get()}\' '
        else:
            if by_type == 1:
                query += f'{my_filter} short_name = \'{name.get()}\' '
            elif by_type == 2:
                query += f'{my_filter} club_name = \'{name.get()}\' '
            else:
                query += f'{my_filter} league_name = \'{name.get()}\' '
    query += ') as subquery;'
    players = get_sql_func(query, None)
    return players


def find_players_advanced(flag, name):
    if flag:
        name = name.get()
        query = f'SELECT players.short_name AS player_name, players_season.player_positions,' \
                f' players_season.overall, players_season.season ' \
                f'FROM players JOIN players_season ON players.id_player = players_season.id_player ' \
                f'JOIN nations ON nations.nationality_id = players.nationality_id ' \
                f'JOIN (SELECT id_player, MAX(overall) as max_overall FROM players_season ' \
                f'GROUP BY id_player) as max_ratings ' \
                f'ON max_ratings.id_player = players_season.id_player ' \
                f'AND max_ratings.max_overall = players_season.overall ' \
                f'WHERE nations.nationality_name = \'{name}\' ORDER BY players_season.overall DESC LIMIT 11'
    else:
        query = f'SELECT short_name, overall, player_positions, SUM(likes) as total_likes, season ' \
                f'FROM players_season ' \
                f'JOIN players ON players_season.id_player = players.id_player ' \
                f'JOIN user_squad_players ON players_season.id_season = user_squad_players.id_player ' \
                f'JOIN user_squads ON user_squad_players.user_squad_id = user_squads.id ' \
                f'GROUP BY id_season ' \
                f'ORDER BY total_likes DESC ' \
                f'LIMIT 11;'
    players = get_sql_func(query, None)
    return players


def get_username(user_id):
    name = get_sql_func(f'SELECT username FROM users WHERE id= {user_id}', None)[0][0]
    return name


def sign(username, password, flag):
    query = f'SELECT * FROM users WHERE username = \'{username}\''
    if flag:
        query += f' AND password = \'{password}\''

    results = get_sql_func(query, None)
    return results


def register(username, password):
    try:
        connection = mysql.connector.connect(
            user=user, host=host, port=port, database=db_name
            , password=pas
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Success", "Registration successful.")
    except Error as e:
        messagebox.showerror("Error", f"Error while connecting to MySQL: {e}")
    finally:
        connection.close()


def user_likes():
    query = 'SELECT users.username, SUM(user_squads.likes) as total_likes ' \
            'FROM user_squads ' \
            'JOIN users ON user_squads.user_id = users.id ' \
            'GROUP BY user_squads.user_id ' \
            'ORDER BY total_likes DESC ' \
            'LIMIT 1;'
    res = get_sql_func(query, None)[0]
    return res


def squad_likes():
    query = 'SELECT user_squads.squad_name, users.username, SUM(user_squads.likes) as total_likes ' \
            'FROM user_squads ' \
            'JOIN users ON user_squads.user_id = users.id ' \
            'GROUP BY user_squads.id ' \
            'ORDER BY total_likes DESC ' \
            'LIMIT 1;'
    res = get_sql_func(query, None)[0]
    return res
