import tkinter as tk
from tkinter import messagebox
import myApi


# update the friend list after we add a new friend:
def update_friends_list(user_id, friends_list_frame):
    for widget in friends_list_frame.winfo_children():
        widget.destroy()
    friends_list = myApi.user_and_friends(user_id)
    for index, friend in enumerate(friends_list):
        friend_button = tk.Button(friends_list_frame, text=friend[1], relief="solid",
                                  command=lambda friend_id=friend[0]: move_to_squad_page(friend_id, False),
                                  bg="white", activebackground="lightblue", font=("Arial", 12), width=20, height=2)
        friend_button.grid(row=index, column=0)


def update_squads_list(user_id, frame, view_frame):

    # function to change the view of the players:
    def set_squad(selected_squad):
        # Remove any existing widgets from the view_frame
        for widget in view_frame.winfo_children():
            widget.destroy()

        # Create a new frame to hold the squad name and like button
        top_frame = tk.Frame(view_frame)
        top_frame.grid(row=0, column=0)

        # Create a new frame to hold the player information
        players_frame = tk.Frame(view_frame)
        players_frame.grid(row=1, column=0)

        squad_id = selected_squad[0]

        # Create a label to display the squad name
        squad_name = tk.Label(top_frame, text=selected_squad[-1], bg='#4CAF50', fg='white', relief="solid",
                              font=('Arial', 18, 'bold'))
        squad_name.grid(row=0, column=1, padx=5, pady=5)

        # Create a button to allow the user to "like" the squad
        def update_likes(num):
            likes = myApi.get_likes(squad_id, num)
            num_likes = tk.Label(top_frame, text=f'{likes} likes', bg='grey', fg='white', relief="solid",
                                  font=('Arial', 12, 'bold'))
            num_likes.grid(row=1, column=0, padx=5, pady=5)

        update_likes(0)
        like_button = tk.Button(top_frame, text="Like!", command=lambda: update_likes(1),
                                bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'))
        like_button.grid(row=1, column=2, padx=5, pady=5)

        players = myApi.get_players_squad(squad_id)

        # Create labels to display player information
        column_name = tk.Label(players_frame, text='name', bg="grey", relief="solid", font=('Arial', 12))
        column_name.grid(row=0, column=0, padx=5, pady=5)
        column_overall = tk.Label(players_frame, text='overall', bg="grey", relief="solid", font=('Arial', 12))
        column_overall.grid(row=0, column=1, padx=5, pady=5)
        column_position = tk.Label(players_frame, text='position', bg="grey", relief="solid", font=('Arial', 12))
        column_position.grid(row=0, column=2, padx=5, pady=5)
        for i, player in enumerate(players):
            player_name = tk.Label(players_frame, text=player[0], bg="white", relief="solid", font=('Arial', 12))
            player_name.grid(row=i+1, column=0, padx=5, pady=5)
            player_position = tk.Label(players_frame, text=player[1], bg="white", relief="solid", font=('Arial', 12))
            player_position.grid(row=i+1, column=1, padx=5, pady=5)
            player_overall = tk.Label(players_frame, text=player[2], bg="white", relief="solid", font=('Arial', 12))
            player_overall.grid(row=i+1, column=2, padx=5, pady=5)

    # Retrieve list of squads from database
    squads = myApi.get_list_squads(user_id)

    for widget in frame.winfo_children():
        widget.destroy()
    for index, squad in enumerate(squads):
        squad_button = tk.Button(frame, text=squad[-1], relief="solid", command= lambda squad=squad: set_squad(squad),
                                  bg="white", activebackground="lightblue", font=("Arial", 12), width=20, height=2)
        squad_button.grid(row=index, column=0)


# this function is for adding a new friend:
def add_friend(user_id, name_input, frame):
    friend_name = name_input.get()
    myApi.add_friend(user_id, friend_name)
    update_friends_list(user_id, frame)


def insert_squad(user_id, squad_players, squad_name, frame, view_frame):
    myApi.insert_squad_sql(user_id, squad_players, squad_name)
    update_squads_list(user_id, frame, view_frame)


# small window for input friend name:
def add_friends_window(user_id, frame):
    add_friend_window = tk.Toplevel(root)
    add_friend_window.title("add friend")

    # Create the inputs for the username, password, and confirmation password
    name_input = tk.Entry(add_friend_window)
    # Add labels for the inputs
    label = tk.Label(add_friend_window, text="friend name:")

    # Create a button to submit the registration
    button = tk.Button(add_friend_window, text="add", command=lambda: (add_friend(user_id, name_input, frame),
                                                                       add_friend_window.destroy()))

    # Add the inputs and labels to the window and position them
    label.grid(row=0, column=0)
    name_input.grid(row=0, column=1)
    button.grid(row=3, column=1, pady=10)


def add_squad_to_db(user_id, squad_players, reset, frame, view_frame):
    add_squad = tk.Toplevel(root)
    add_squad.title("add_squad")

    squad_name_label = tk.Label(add_squad, text="squad name:")
    squad_name_label.grid(row=0, column=0, padx=10)
    squad_name = tk.Entry(add_squad)
    squad_name.grid(row=0, column=1)

    squad_button = tk.Button(add_squad, text="add", command=lambda: (insert_squad(user_id, squad_players,
                                                                squad_name, frame, view_frame), add_squad.destroy()))
    squad_button.grid(row=0, column=2)


def list_player_results(user_id, results, update):
    list_players_results = tk.Toplevel(root)
    list_players_results.title("list player results")

    canvas = tk.Canvas(list_players_results)
    scrollbar = tk.Scrollbar(list_players_results, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the widgets
    table_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=table_frame, anchor="nw")

    name_label = tk.Label(table_frame, text="name")
    name_label.grid(row=0, column=0, padx=10)

    overall_label = tk.Label(table_frame, text="overall")
    overall_label.grid(row=0, column=1, padx=10)

    season_label = tk.Label(table_frame, text="season")
    season_label.grid(row=0, column=2, padx=10)

    more_details_label = tk.Label(table_frame, text="more details")
    more_details_label.grid(row=0, column=3, padx=10)

    add_label = tk.Label(table_frame, text="add")
    add_label.grid(row=0, column=4, padx=10)

    def open_details(player_details):
        details = myApi.player_data(player_details)
        details_window = tk.Toplevel(root)
        details_window.title(player[0])
        for i, field in enumerate(details):
            label = tk.Label(details_window, text=field)
            label.grid(row=0, column=i, padx=10)

    # show the results:
    for i, player in enumerate(results):

        player_name_label = tk.Label(table_frame, text=player[0])
        player_name_label.grid(row=i+1, column=0, padx=10)

        player_overall_label = tk.Label(table_frame, text=player[1])
        player_overall_label.grid(row=i+1, column=1, padx=10)

        player_season_label = tk.Label(table_frame, text=player[-1])
        player_season_label.grid(row=i+1, column=2, padx=10)

        more_details_label = tk.Button(table_frame, text="more details", command=lambda player=player: open_details(player))
        more_details_label.grid(row=i+1, column=3, padx=10)

        add_label = tk.Button(table_frame, text="add", command=lambda player=player: update(player))
        add_label.grid(row=i+1, column=4, padx=10)


# function that for finding player by the credentials:
def find_by_player(user_id, dic_data, name, by_type, update):
    # fix names:
    if by_type != 3:
        dic_data['nationality_name'] = dic_data.pop('nation')
    if by_type != 1:
        dic_data['players_season.season'] = dic_data.pop('season')
    # get the values from the inputs:
    for k in dic_data:
        if not isinstance(dic_data[k], str):
            dic_data[k] = dic_data[k].get()

    results = myApi.find_players(dic_data, name, by_type)
    list_player_results(user_id, results, update)
    dic_data.clear()
    return 0


def create_squad_advanced(user_id, frame, view_frame):

    create_squad_page = tk.Toplevel(root)
    create_squad_page.title("Build Squad")

    # Create the search frame
    search_frame = tk.Frame(create_squad_page)
    search_frame.pack(pady=10)

    national_team_label = tk.Label(search_frame, text="national team name:", font=("Arial", 14))
    national_team_label.grid(row=0, column=0, padx=10)
    national_team = tk.Entry(search_frame, font=("Arial", 14))
    national_team.grid(row=0, column=1)

    team_search_button = tk.Button(search_frame, text="create national team!", font=("Arial", 14), bg='green',
                                   command=lambda national_team=national_team: update_listbox(True, national_team))
    team_search_button.grid(row=0, column=2, pady=10)

    divider = tk.Frame(search_frame, bg="black", height=2, width=search_frame.winfo_width())
    divider.grid(row=1, column=0, columnspan=8, pady=10, padx=10, sticky='ew')

    popular_players_label = tk.Label(search_frame, text="create the squad with the most popular players! ",
                                     font=("Arial", 14))
    popular_players_label.grid(row=2, column=0, padx=10)

    popular_players_button = tk.Button(search_frame, text="click here!", font=("Arial", 14), bg='green',
                                       command=lambda: update_listbox(False, None))
    popular_players_button.grid(row=2, column=2, pady=10)

    divider = tk.Frame(create_squad_page, height=2, bd=1, relief=tk.SUNKEN)
    divider.pack(fill=tk.X, padx=5, pady=5)

    # Create the list box for the chosen players
    players_list = tk.Listbox(create_squad_page)
    players_list.pack()
    players_list_data = []

    # Create the remove button for the players
    remove_button = tk.Button(create_squad_page, text="Remove", font=("Arial", 14), bg='green',
                              command=lambda: remove_listbox())
    remove_button.pack(fill=tk.X, padx=5, pady=5)

    # Create the save squad button
    save_button = tk.Button(create_squad_page, text="Save Squad", font=("Arial", 14), bg='green',
                            command=lambda: save_squad())
    save_button.pack(fill=tk.X, padx=5, pady=5)

    def save_squad():
        if len(players_list_data) < 11:
            messagebox.showinfo("violation", "you have less than 11 players!")
        else:
            add_squad_to_db(user_id, players_list_data, None, frame, view_frame)

    def remove_listbox():
        players_list.delete(0, tk.END)
        players_list_data.clear()

    def update_listbox(flag, name):
        remove_listbox()
        players_from_db = myApi.find_players_advanced(flag, name)
        i = 0
        for player in players_from_db:
            if i == 0:
                # print(player)
                i += 1
            players_list_data.append(player)
            players_list.insert(tk.END, player[0])


def create_squad(user_id, frame, view_frame):
    create_squad_page = tk.Toplevel(root)
    create_squad_page.title("Build Squad")

    # Create the search frame
    search_frame = tk.Frame(create_squad_page)
    search_frame.pack(pady=10)

    dic_data ={}
    # player overall:
    overall_label = tk.Label(search_frame, text="overall:")
    overall_label.grid(row=0, column=0, padx=10)
    overall = tk.Entry(search_frame)
    overall.grid(row=0, column=1)

    # player nation:
    nation_label = tk.Label(search_frame, text="nation:")
    nation_label.grid(row=0, column=2, padx=10)
    nation = tk.Entry(search_frame)
    nation.grid(row=0, column=3)

    # player price:
    price_label = tk.Label(search_frame, text="price:")
    price_label.grid(row=0, column=4, padx=10)
    price = tk.Entry(search_frame)
    price.grid(row=0, column=5)

    # player salary:
    salary_label = tk.Label(search_frame, text="salary:")
    salary_label.grid(row=0, column=6, padx=10)
    salary = tk.Entry(search_frame)
    salary.grid(row=0, column=7)

    # player age:
    age_label = tk.Label(search_frame, text="age:")
    age_label.grid(row=1, column=0, padx=10)
    age = tk.Entry(search_frame)
    age.grid(row=1, column=1)

    # player positions:
    positions_label = tk.Label(search_frame, text="positions:")
    positions_label.grid(row=1, column=2, padx=10)
    positions = tk.Entry(search_frame)
    positions.grid(row=1, column=3)

    # player potential:
    potential_label = tk.Label(search_frame, text="potential:")
    potential_label.grid(row=1, column=4, padx=10)
    potential = tk.Entry(search_frame)
    potential.grid(row=1, column=5)

    # player season:
    season_label = tk.Label(search_frame, text="season:")
    season_label.grid(row=1, column=6, padx=10)
    season = tk.Entry(search_frame)
    season.grid(row=1, column=7)
    # dic_data["season"] = season

    divider = tk.Frame(search_frame, bg="black", height=2, width=search_frame.winfo_width())
    divider.grid(row=2, column=0, columnspan=8, pady=10, padx=10, sticky='ew')

    # player:
    player_name_label = tk.Label(search_frame, text="Player:")
    player_name_label.grid(row=3, column=0, padx=10)
    player_name = tk.Entry(search_frame)
    player_name.grid(row=3, column=1)

    def update_dic_data():
        dic_data["overall"] = overall
        dic_data["nation"] = nation
        dic_data["wage_eur"] = price
        dic_data["value_eur"] = salary
        dic_data["age"] = age
        dic_data["player_positions"] = positions
        dic_data["potential"] = potential
        dic_data["season"] = season


    # Create the search button for player
    player_search_button = tk.Button(search_frame, text="Search",
            command=lambda: (update_dic_data(), find_by_player(user_id, dic_data, player_name, 1, update_players_list)))
    player_search_button.grid(row=4, column=0, pady=10)

    # Create the team search label and input
    team_label = tk.Label(search_frame, text="Team:")
    team_label.grid(row=5, column=0, padx=10)
    team = tk.Entry(search_frame)
    team.grid(row=5, column=1)

    # Create the search button for team
    team_search_button = tk.Button(search_frame, text="Search",
                                   command=lambda: (update_dic_data(), find_by_player(user_id, dic_data, team, 2,
                                                                                      update_players_list)))
    team_search_button.grid(row=6, column=0, pady=10)

    # Create the league search label and input
    league_label = tk.Label(search_frame, text="League:")
    league_label.grid(row=7, column=0, padx=10)
    league = tk.Entry(search_frame)
    league.grid(row=7, column=1)

    # Create the search button for league
    league_search_button = tk.Button(search_frame, text="Search",
                                     command=lambda: (update_dic_data(), find_by_player(user_id, dic_data, league, 3,
                                                                                        update_players_list)))
    league_search_button.grid(row=8, column=0, pady=10)

    divider = tk.Frame(create_squad_page, height=2, bd=1, relief=tk.SUNKEN)
    divider.pack(fill=tk.X, padx=5, pady=5)

    # Create the list box for the chosen players
    players_list = tk.Listbox(create_squad_page)
    players_list.pack()
    players_list_data = []

    # Create the remove button for the players
    remove_button = tk.Button(create_squad_page, text="Remove", command=lambda: reset_list())
    remove_button.pack()

    # Create the save squad button
    save_button = tk.Button(create_squad_page, text="Save Squad", command=lambda: add(frame, view_frame))
    save_button.pack()

    def update_players_list(player):
        if len(players_list_data) < 11:
            if player not in players_list_data:
                players_list.insert(tk.END, player[0])
                players_list_data.append(player)
            else:
                messagebox.showinfo("violation", "player is already in your squad!")
        else:
            messagebox.showinfo("full", "your squad is full!")

    def reset_list():
        players_list.delete(0, tk.END)
        players_list_data.clear()

    def add(frame, view_frame):
        if len(players_list_data) == 11:
            add_squad_to_db(user_id, players_list_data, reset_list, frame, view_frame)


def info():
    info_page = tk.Toplevel(root)
    info_page.title("info")

    # Create the search frame
    search_frame = tk.Frame(info_page)
    search_frame.pack(pady=10)

    user_likes = ''
    squad_likes = ''

    user_label = tk.Label(search_frame, text="user with the most likes: ", font=("Arial", 14))
    user_label.grid(row=0, column=0, padx=10)

    user_button = tk.Button(search_frame, text="click here to see!", font=("Arial", 14), bg='green',
                                   command=lambda: update_user_likes())
    user_button.grid(row=0, column=1, pady=10)

    user_info_label = tk.Label(search_frame, text=user_likes, font=("Arial", 14))
    user_info_label.grid(row=1, column=0, padx=10)

    divider = tk.Frame(search_frame, bg="black", height=2, width=search_frame.winfo_width())
    divider.grid(row=2, column=0, columnspan=8, pady=10, padx=10, sticky='ew')

    squad_label = tk.Label(search_frame, text="squad with the most likes: ",
                                     font=("Arial", 14))
    squad_label.grid(row=3, column=0, padx=10)

    squad_button = tk.Button(search_frame, text="click here to see!", font=("Arial", 14), bg='green',
                                       command=lambda: update_squad_likes())
    squad_button.grid(row=3, column=1, pady=10)

    squad_info_label = tk.Label(search_frame, text=squad_likes, font=("Arial", 14))
    squad_info_label.grid(row=4, column=0, padx=10)

    def update_user_likes():
        res = myApi.user_likes()
        user_likes = f'{res[0]} has {res[1]} likes!'
        user_info_label.config(text=user_likes)
        # print(user_likes)

    def update_squad_likes():
        res = myApi.squad_likes()
        squad_likes = f'{res[1]}\'s {res[0]} has {res[2]} likes!'
        squad_info_label.config(text=squad_likes)
        # print(squad_likes)

def move_to_squad_page(user_id, flag):
    squad_page = tk.Toplevel(root)
    squad_page.title("Squad Page")
    squad_page.configure(bg='white')

    # Middle frame for displaying selected squad:
    middle_frame = tk.Frame(squad_page)
    middle_frame.grid(row=0, column=1)
    tk.Label(middle_frame, text="Selected Squad", bg="grey", relief="solid",
             font=('Arial',12,'bold')).grid(row=0, column=1)
    # Placeholder for displaying selected squad
    # tk.Label(middle_frame, bg="white", relief="solid", width=40, height=30).grid(row=1, column=0)

    # Left frame for displaying user's squads:
    name = myApi.get_username(user_id)
    left_frame = tk.Frame(squad_page)
    left_frame.grid(row=0, column=0)
    squads_list_frame = tk.Frame(left_frame)
    squads_list_frame.grid(row=4, column=0)
    if flag:
        tk.Button(left_frame, text="info", bg="blue", relief="solid", width=20, font=('Arial', 12, 'bold'),
                  command=lambda: info()).grid(row=0, column=0)
        tk.Button(left_frame, text="Add Squad", bg="green", relief="solid", width=20, font=('Arial',12,'bold'),
                  command=lambda: create_squad(user_id, squads_list_frame, middle_frame)).grid(row=1, column=0)
        tk.Button(left_frame, text="Add Squad (advanced)", bg="#4CAF50", relief="solid", width=20, font=('Arial', 12, 'bold'),
                  command=lambda: create_squad_advanced(user_id, squads_list_frame, middle_frame)).grid(row=2, column=0)
        tk.Label(left_frame, text=f"{name}'s Squads", bg="grey", relief="solid", width=20,
             font=('Arial',12,'bold')).grid(row=3, column=0)

    else:
        tk.Label(left_frame, text=f"{name}'s Squads", bg="grey", relief="solid", width=20,
                 font=('Arial', 12, 'bold')).grid(row=0, column=0)

    # Retrieve list of squads from database:
    update_squads_list(user_id, squads_list_frame, middle_frame)


    # Right frame for displaying user's friends
    if flag:
        right_frame = tk.Frame(squad_page)
        right_frame.grid(row=0, column=2)
        friends_list_frame = tk.Frame(right_frame)
        friends_list_frame.grid(row=2, column=0)
        tk.Button(right_frame, text="Add Friend", bg="green", relief="solid", width=20, font=('Arial',12,'bold'),
                  command=lambda: add_friends_window(user_id, friends_list_frame)).grid(row=0, column=0)
        tk.Label(right_frame, text="Your Friends", bg="grey", relief="solid",
                 width=20, font=('Arial',12,'bold')).grid(row=1, column=0)

        update_friends_list(user_id, friends_list_frame)


def sign_in():
    # Get the values of the username and password inputs
    username = username_input.get()
    password = password_input.get()
    results = myApi.sign(username, password, True)
    if results:
        move_to_squad_page(results[0][0], True)
    else:
        messagebox.showinfo("fail", "invalid username or password")


def register_user():
    # Get the input values from the registration page
    username = register_username_input.get()
    password = register_password_input.get()
    confirm_password = register_confirm_password_input.get()
    # Check that the passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return
    # Check that the username and password are not empty
    if not all([username, password]):
        messagebox.showerror("Error", "Username and password are required.")
        return
    results = myApi.sign(username, password, False)
    if results:
        messagebox.showinfo("fail", "username already exists")
    else:
        myApi.register(username, password)


def register(event):
    global register_username_input
    global register_password_input
    global register_confirm_password_input

    register_window = tk.Toplevel(root)
    register_window.title("Register")

    # Create the inputs for the username, password, and confirmation password
    register_username_input = tk.Entry(register_window)
    register_password_input = tk.Entry(register_window, show="*")
    register_confirm_password_input = tk.Entry(register_window, show="*")

    # Add labels for the inputs
    register_username_label = tk.Label(register_window, text="Username:")
    register_password_label = tk.Label(register_window, text="Password:")
    register_confirm_password_label = tk.Label(register_window, text="Confirm Password:")

    # Create a button to submit the registration
    register_button = tk.Button(register_window, text="Register", command=register_user)

    # Add the inputs and labels to the window and position them
    register_username_label.grid(row=0, column=0)
    register_username_input.grid(row=0, column=1)
    register_password_label.grid(row=1, column=0)
    register_password_input.grid(row=1, column=1)
    register_confirm_password_label.grid(row=2, column=0)
    register_confirm_password_input.grid(row=2, column=1)
    register_button.grid(row=3, column=1, pady=10)


# Create the main window
root = tk.Tk()
root.title("Sign up")

# Create the inputs for the username and password
username_input = tk.Entry(root, font=("Helvetica", 14))
password_input = tk.Entry(root, show="*", font=("Helvetica", 14))

# Add labels for the inputs
username_label = tk.Label(root, text="Username:", font=("Helvetica", 14))
password_label = tk.Label(root, text="Password:", font=("Helvetica", 14))

# Create a button to submit the sign up
sign_in_button = tk.Button(root, text="Sign Up", font=("Helvetica", 14), command=sign_in, bg="#2196F3", fg="white")

# Create a link to the register page
register_link = tk.Label(root, text="Don't have an account? Register here", font=("Helvetica", 14), fg="blue",
                         cursor="hand2")
register_link.bind("<Button-1>", register)

# Add the inputs and labels to the window and position them
username_label.grid(row=0, column=0, pady=20, padx=20)
username_input.grid(row=0, column=1, pady=20, padx=20)
password_label.grid(row=1, column=0, pady=20, padx=20)
password_input.grid(row=1, column=1, pady=20, padx=20)
sign_in_button.grid(row=2, column=1, pady=20, padx=20)
register_link.grid(row=3, column=1, pady=20, padx=20)

root.mainloop()
