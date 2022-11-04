import psycopg
from psycopg import OperationalError


def create_connection(
    db_name, db_user, db_password, db_host="localhost", db_port="5432"
):
    connection = None
    try:
        connection = psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(query, params=None):
    connection = create_connection("postgres", "postgres", "postgres")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Query executed successfully")
        connection.close()
        return cursor
    except OSError as e:
        print(f"The error '{e}' occurred or the hero name is already taken")


# ============================================================================== DONT EDIT ABOVE


# def select_all():
#     num = 1
#     query = """
#         SELECT * FROM heroes 
#         """

#     list_of_heroes = execute_query(query).fetchall()
#     print(list_of_heroes)
#     for record in list_of_heroes:
#         print(record[num])


## INITIAL MENU OPTIONS
def menu_options():
    function_dict = {
        "create_hero": create_input,
        "remove_hero": remove_hero,    #Dictionary for calling function based on user selection
        "find_hero": find_hero,
        "update_hero": update_hero,
    }
    prompt = input(
        "\n HELLO, WHAT WOULD YOU LIKE TO DO?\n"
        "1 = Create a new hero \n"
        "2 = Find a hero \n"                    #Input for main menu
        "3 = Update an existing hero \n"
        "4 = Remove a hero \n"
    )
    user_choice = int(prompt) - 1
    print(user_choice)
    if 0 <= user_choice <= 3:       # Defensive programming checking if user choice is an index of list
        crud_functions = ["create_hero", "find_hero", "update_hero", "remove_hero"] #List that refers to dictionary keys
        function_caller = function_dict[crud_functions[user_choice]]    #Setting variable to function dict index. refers to index of dict by index of functions list
        function_caller()       # Calls function by function dictionary value

    else:
        print("Choose a valid option")      # Defensive programming informs user to choose valid option and recalls menu options function
        menu_options()

## CHARACTER CREATION INPUT
def create_input():
    name = input("Hello, what is your name? ")
    about_me = input("Tell us about yourself. ")        #Inputs
    biography = input("What's your story? ")
    query = """ 
    INSERT INTO heroes (name, about_me, biography) VALUES (%s, %s, %s) 
    """
    execute_query(query, (name, about_me, biography))
    print(f"{name} CREATED!")
    menu_options()


## FIND HERO FUNCTION
def find_hero():
    hero_name_list = []     #Empty list for pushing hero names to for defensive programming
    hero_name = input(
        "ENTER THE NAME OF THE HERO YOU WOULD LIKE TO FIND\n"
        "OR TYPE ENTER TO RETURN TO MAIN MENU \n"
    )
    
    #Query for finding hero
    query = """
        SELECT * FROM heroes 
        WHERE lower(%s) = lower(heroes.name)
        """

    #Query for defensive programming
    query2 = """
        SELECT * FROM heroes 
        """
    list_of_heroes = execute_query(query2)  

    #Looping through all heroes appending the name to empty list 
    for hero in list_of_heroes:
        hero_name_list.append(hero[1].lower())  
    print(hero_name_list)
    find_hero_row = execute_query(query, (hero_name,)).fetchall()

    #Checking if hero name entered by input is in the list of hero names
    if hero_name.lower() in hero_name_list:
        print(
            f"\nName: {find_hero_row[0][1]} \nAbout: {find_hero_row[0][2]} \nBio: {find_hero_row[0][3]}"
        )
        menu_options()

        # Elif statement for returning to main menu if user enters return
    elif hero_name.lower() == "return":
        menu_options()

        #if user enters invalid name informs them and recalls function
    else:
        print("\n ENTER VALID HERO NAME")
        find_hero()


## UPDATE HERO FUNCTION
def update_hero():
    hero_name_list = []     #Empty list for defensive programming
    updateDict = {
        "1": update_name, 
        "2": update_about_me,   #Dictionary for calling functions based on which column user wants to update
        "3": update_bio}
    hero_to_update = input(
        "\n -ENTER NAME OF THE HERO YOU WANT TO UPDATE\n - OR TYPE RETURN TO RETURN TO MAIN MENU \n"
    )

    #Defensive programing query
    query2 = """
            SELECT * FROM heroes 
            """
    list_of_heroes = execute_query(query2)

    #Looping through all heroes appending the name to empty list 
    for hero in list_of_heroes:
        hero_name_list.append(hero[1].lower())
    print(hero_name_list)

    # Return to main menu if return is entered
    if hero_to_update.lower() == "return":
        menu_options()

    #Checking if hero name entered is in hero name list
    elif not hero_to_update.lower() in hero_name_list:
        print("PLEASE ENTER A VALID HERO")
        update_hero()
    what_to_update = input(
        "\n CHOOSE WHAT TO UPDATE\n"
        "1 = New Name\n"
        "2 = About Me \n"
        "3 = Biography\n"
    )

    #Checking if option chosen is within the length of dictionary
    if int(what_to_update) <= len(updateDict):
        updateDict[what_to_update](hero_to_update)
    else:
        print("\n PLEASE ENTER A VALID ITEM TO UPDATE")
        update_hero()

#Update hero name function
def update_name(hero):
    new_name = input("\n ENTER NEW NAME \n")
    query = """
    UPDATE heroes
    SET name = %s
    WHERE LOWER(%s) = LOWER(heroes.name);
    """
    execute_query(query, (new_name, hero))
    menu_options()


## UPDATE ABOUT ME SECTION OF HEROES ##UPDATE DEFENSIVE TO MAKE SURE NAME IS VALID
def update_about_me(hero):
    new_about = input("\n ENTER NEW ABOUT ME \n")
    query = """
    UPDATE heroes
    SET about_me = %s
    WHERE LOWER(%s) = LOWER(heroes.name);
    """
    execute_query(query, (new_about, hero))
    print(f"\n ABOUT ME FOR {hero} UPDATED")
    menu_options()


## UPDATE BIO OF HEROES
def update_bio(hero):
    new_bio = input("\n ENTER NEW BIOGRAPHY \n")
    query = """
    UPDATE heroes
    SET biography = %s
    WHERE LOWER(%s) = LOWER(heroes.name)
    """
    execute_query(query, (new_bio, hero))
    print(f"\n BIOGRAPHY {hero} UPDATED")
    menu_options()


## REMOVE HERO FUNCTION
def remove_hero():
    hero_ids = [] #Defensive programming list for appending hero ids
    prompt = ""   #Empty string to concat hero id and name to for selection prompt
    query = """
        SELECT * FROM heroes 
        """
    list_of_heroes = execute_query(query).fetchall()

    #Looping through heroes printing name and concatenating hero id and hero name to prompt string
    for hero in list_of_heroes:
        prompt += f"{hero[0]} = {hero[1]}. \n"

    deleteprompt = input(
        "CHOOSE THE ID NUMBER OF THE HERO YOU WANT TO DELETE \n"
        f"{prompt}"
        "OR TYPE RETURN TO RETURN TO MAIN MENU \n"
    )

    # Defensive programming loop appending id to empty list
    for i in list_of_heroes:
        hero_ids.append(i[0])

    # Checking if input entered is in hero id list
    if deleteprompt in str(hero_ids):
        query = """
            DELETE FROM heroes WHERE %s = heroes.id
            """
        execute_query(query, (deleteprompt,))
        menu_options()

    #Returning to main menu if return is entered
    elif deleteprompt.lower() == "return":
        menu_options()

    #If invalid id is entered call remove error function
    else:
        handle_remove_error()


## ERROR HANDLING FOR REMOVING HEROES
def handle_remove_error():
    hero_ids = []  #Defensive programming list for appending hero ids
    prompt = ""   #Empty string to concat hero id and name to for selection prompt
    query = """
        SELECT * FROM heroes 
        """
    list_of_heroes = execute_query(query).fetchall()
    # Defensive programming loop appending id to empty list
    for hero in list_of_heroes:
        prompt += f"{hero[0]} = {hero[1]}. \n"
    
    deleteprompt = input(
        "PLEASE ENTER A VALID HERO ID\n"
        f"{prompt}"
        "OR TYPE RETURN TO GO BACK TO MAIN MENU \n"
    )
    # Checking if input entered is in hero id list
    for i in list_of_heroes:
        hero_ids.append(i[0])

    # Checking if input entered is in hero id list
    if deleteprompt in str(hero_ids):
        query = """
            DELETE FROM heroes WHERE %s = heroes.id
            """
        execute_query(query, (deleteprompt,))
        menu_options()

    #Returning to main menu if return is entered
    elif deleteprompt.lower() == "return":
        menu_options()

    #If invalid hero id is entered recalls remove hero function
    else:
        remove_hero()


# Calling main menu function initially
menu_options()
