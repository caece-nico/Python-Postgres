from  database_con_listas import add_entry, get_entry


def prompt_new_entry():

    entry_content = input("Whats have you learned today?")
    entry_date = input("Enter date")

    add_entry(entry_content, entry_date)

def view_entry(entries):

    for entry in entries:
        print(f"{entry['date']}\n {entry['content']}\n\n")



menu = """Please select one of the following options:
1) Add new entry for today.
2) View entries.
3) Exit.


Your selection: """


welcome = "Welcome to the programming diary!"

user_input = input(menu)

while user_input != "3":
    # Ingreso un valor distinto de tres.

    if user_input == "1":
        print('Adding')
        prompt_new_entry()

    elif user_input == "2":
        print('Viewing..')
        view_entry(get_entry())

    else:
        print('Invalid option, please try again!')

    user_input = input(menu)