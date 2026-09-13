def user_register():
    print("\n=== Event User Registration ===")
    username = input("Create username: ").strip()
    password = input("Create password: ").strip()
    user_id = input("Create ID (ex:admin1): ").strip()
    role = input("Enter role (admin/organizer/participant/venue): ").strip().lower()

    if role not in ["admin", "organizer", "participant", "venue"]:
        print("Invalid role! Must be: admin, organizer, participant, or venue.")
        return

    if not username or not password or not user_id:
        print("Username, password, and ID cannot be empty.")
        return

    try:
        with open("users.txt", "a") as file:
            file.write(f"{username},{password},{user_id},{role}\n")
        print(f"User account '{username}' registered successfully!")
        print("Please login after registration\n")
    except Exception as e:
        print("Failed to save user:", e)


def login(username, password, user_id):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) != 4:
                    continue  # skip incomplete lines
                stored_user, stored_pass, stored_id, role = parts
                if username == stored_user and password == stored_pass and user_id == stored_id:
                    return role  # return role if matched
        return None
    except FileNotFoundError:
        print("User file not found.")
        return None


def user_login():
    while True:
        print("=== EVENT LOGIN SYSTEM ===")
        new_user = input("Are you a new user? (Y/N): ").strip().upper()

        if new_user == "Y":
            user_register()
            return user_login()  # Loop back to login after registration

        print("=== LOGIN ===")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        user_id = input("ID (ex:admin1): ").strip()


        role = login(username, password, user_id)

        if role:
            print(f"\nWelcome, {username}! You are logged in as {role}.")
            if role == "admin":
                import Adminstrator
                Adminstrator.admin_menu()
            elif role == "organizer":
                import Event_Organizer
                Event_Organizer.organizer_menu()
            elif role == "participant":
                import Participants
                Participants.participant_menu()
            elif role == "venue":
                import venue_manager
                venue_manager.venue_manager_menu()
            else:
                print("Unknown role.")
                break
        else:
            print("Invalid login credentials.")


user_login()