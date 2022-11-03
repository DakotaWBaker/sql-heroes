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


def select_all():
    num = 1
    query = """
        SELECT * FROM heroes 
        """

    list_of_heroes = execute_query(query).fetchall()
    print(list_of_heroes)
    for record in list_of_heroes:
        print(record[num])


## INITIAL MENU OPTIONS
def menu_options():
    function_dict = {
        "create_hero": create_input,
        "remove_hero": remove_hero,
        "find_hero": find_hero,
        'update_hero': update_hero
    }
    prompt = input(
        "\n HELLO, WHAT WOULD YOU LIKE TO DO?\n"
        "1 = Create a new hero \n"
        "2 = Find a hero \n"
        "3 = Update an existing hero \n"
        "4 = Remove a hero \n"
    )
    user_choice = int(prompt) - 1
    print(user_choice)
    if 0 <= user_choice <= 3:
        crud_functions = ["create_hero", "find_hero", "update_hero", "remove_hero"]
        function_caller = function_dict[crud_functions[user_choice]]
        function_caller()

    else:
        print("Choose a valid option")
        menu_options()


## CHARACTER CREATION INPUT
def create_input():
    name = input("Hello, what is your name? ")
    about_me = input("Tell us about yourself. ")
    biography = input("What's your story? ")
    query = """ 
    INSERT INTO heroes (name, about_me, biography) VALUES (%s, %s, %s)
    """
    execute_query(query, (name, about_me, biography))
    print(f"{name} CREATED!")
    menu_options()

## FIND HERO FUNCTION
def find_hero():
    hero_name_list = []
    hero_name = input("ENTER THE NAME OF THE HERO YOU WOULD LIKE TO FIND\n"
    "OR TYPE ENTER TO RETURN TO MAIN MENU \n"
    )
    query = """
        SELECT * FROM heroes 
        WHERE lower(%s) = lower(heroes.name)
        """
    query2 = """
        SELECT * FROM heroes 
        """
    list_of_heroes = execute_query(query2)
    for hero in list_of_heroes:
        hero_name_list.append(hero[1].lower())
    print(hero_name_list)
    find_hero_row = execute_query(query, (hero_name,)).fetchall()

    if hero_name.lower() in hero_name_list:
        print(
            f"\nName: {find_hero_row[0][1]} \nAbout: {find_hero_row[0][2]} \nBio: {find_hero_row[0][3]}"
        )
        menu_options()
    elif hero_name.lower() == 'return':
        menu_options()
    else:
        print("\n ENTER VALID HERO NAME")
        find_hero()

def update_hero():
    updateDict = {
        '1': update_about_me,
        '2': update_bio
    }
    hero_to_update = input("\n ENTER NAME OF THE HERO YOU WANT TO UPDATE\n")
    what_to_update = input("\n CHOOSE WHAT TO UPDATE\n"
    "1 = About Me \n"
    "2 = Biography\n"
    )
    if what_to_update.lower() == '1':
        updateDict[what_to_update](hero_to_update)
    
    elif what_to_update.lower() == '2':
        updateDict[what_to_update](hero_to_update)

def update_about_me(hero):
    new_about = input('\n ENTER NEW ABOUT ME \n')
    query = """
    UPDATE heroes
    SET about_me = %s
    WHERE LOWER(%s) = LOWER(heroes.name)
    """
    execute_query(query,(new_about, hero))
    print(f"\n ABOUT ME FOR {hero} UPDATED")

def update_bio(hero):
    new_bio = input('\n ENTER NEW BIOGRAPHY \n')
    query = """
    UPDATE heroes
    SET biography = %s
    WHERE LOWER(%s) = LOWER(heroes.name)
    """
    execute_query(query,(new_bio, hero))
    print(f"\n BIOGRAPHY {hero} UPDATED")
    



## REMOVE HERO FUNCTION
def remove_hero():
    hero_ids = []
    prompt = ""
    query = """
        SELECT * FROM heroes 
        """

    list_of_heroes = execute_query(query).fetchall()
    for hero in list_of_heroes:
        prompt += f"{hero[0]} = {hero[1]}. \n"

    deleteprompt = input(
        "CHOOSE THE ID NUMBER OF THE HERO YOU WANT TO DELETE \n"
        f"{prompt}"
        "OR TYPE RETURN TO RETURN TO MAIN MENU \n"
    )

    for i in list_of_heroes:
        hero_ids.append(i[0])

    if deleteprompt in str(hero_ids):
        query = """
            DELETE FROM heroes WHERE %s = heroes.id
            """
        execute_query(query, (deleteprompt,))
        menu_options()
    elif deleteprompt.lower() == "return":
        menu_options()
    else:
        handle_remove_error()


## ERROR HANDLING FOR REMOVING HEROES
def handle_remove_error():
    hero_ids = []
    prompt = ""
    query = """
        SELECT * FROM heroes 
        """

    list_of_heroes = execute_query(query).fetchall()
    for hero in list_of_heroes:
        prompt += f"{hero[0]} = {hero[1]}. \n"

    deleteprompt = input(
        "PLEASE ENTER A VALID HERO ID\n"
        f"{prompt}"
        "OR TYPE RETURN TO GO BACK TO MAIN MENU \n"
    )

    for i in list_of_heroes:
        hero_ids.append(i[0])

    if deleteprompt in str(hero_ids):
        query = """
            DELETE FROM heroes WHERE %s = heroes.id
            """
        execute_query(query, (deleteprompt,))
        menu_options()
    elif deleteprompt.lower() == "return":
        menu_options()
    else:
        remove_hero()


menu_options()
