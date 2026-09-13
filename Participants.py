def participant_login():
    participant_id = input("Enter your Participant ID (e.g. P001): ").strip()
    name = input("Enter your name: ").strip()

    found = False
    try:
        with open("participants.txt", "r") as file:
            for line in file:
                if line.strip().split(",")[0] == participant_id:
                    found = True
                    break
    except FileNotFoundError:
        pass

    if not found:
        try:
            with open("participants.txt", "a") as file:
                file.write(f"{participant_id},{name}\n")
            print(f" Welcome, {name} you are now registered as a participant.")
        except:
            print(" invalid saving participant.")
    return participant_id

def participant_menu():
    participant_id = participant_login()

    while True:
        print("\n---Participant Menu---\n")
        print("1.Browse/Search Upcoming Events")
        print("2.Register for an event")
        print("3.Cancel Registration")
        print("4.View Personal Event Calendar")
        print("5.Log out")


        choice = input("Please select your choice:")
        if choice == "1":
            print("1.Browse all upcoming events\n")
            print("2.Search all upcoming events")
            choice = input("Please select your choice: ")
            if choice == "1":
                browse_upcoming_events()
            elif choice == "2":
                search_upcoming_events()
            else:
                print("Not available choice,please try again")
        elif choice == "2":
            register_for_event(participant_id)
        elif choice == "3":
            cancel_registration(participant_id)
        elif choice == "4":
            view_personal_calendar(participant_id)
        elif choice == "5":
            print("Log out")
            break
        else:
            print("Invalid choice, please write a correct option.")

def browse_upcoming_events():
    # Build a map from Location ID to Location Name
    location_dict = {}
    try:
        with open("venues.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    venue_id = parts[0].strip()
                    venue= parts[1].strip()
                    location_dict[venue_id] = venue
    except FileNotFoundError:
        print("VENUES FILE NOT EXISTING! ")
        return

    # read event.txt then display Approved events
    try:
        with open("event.txt", "r") as f:
            print("\nUpcoming Events\n")
            print("{:<10} {:<20} {:<12} {:<15} {:<30} {:<10}".format(
                "Event_id", "Event_title", "Date", "Location", "Description", "Capacity"
            ))
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 8 and parts[7] == "Approved":
                    event_id = parts[0]
                    title = parts[1]
                    date = parts[2]
                    location_id = parts[3]
                    description = parts[4]
                    capacity = parts[5]

                    #Replace location ID with corresponding location name from location_dict
                    location = location_dict.get(location_id, location_id)

                    print("{:<10} {:<20} {:<12} {:<15} {:<30} {:<10}".format(
                        event_id, title, date, location, description, capacity
                    ))
    except FileNotFoundError:
        print("EVENT FILE NOT EXISTING!")


def search_upcoming_events():
    search = input("Enter a keyword to search: ").strip().lower()
    found = False  # Define in advance
    try:
        with open("event.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 8 and parts[7].strip().lower() == "approved":
                    # Check if the keyword is in the first 5 parts
                    if (search.lower() in parts[0].lower() or
                            search.lower() in parts[1].lower() or
                            search.lower() in parts[2].lower() or
                            search.lower() in parts[3].lower() or
                            search.lower() in parts[4].lower()):
                        found = True
                        print(f"{parts[0]}\t{parts[1]}\t{parts[2]}\t{parts[3]}\t{parts[4]}")

        if not found:
             print("No events found.")

    except FileNotFoundError:
         print("EVENT FILE NOT EXISTING!")


def register_for_event(participant_id):
    # Display all upcoming events
    browse_upcoming_events()

    event_id = input("\nEnter the Event ID to register for: ").strip()

    # Check if the event exists and is approved
    event_exists = False
    try:
        with open("event.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 8 and parts[0] == event_id and parts[7].lower() == "approved":
                    event_exists = True
                    break
    except FileNotFoundError:
        print("Event file not found!")
        return

    if not event_exists:
        print("The event ID you entered does not exist or has not been approved.")
        return

    # Check if already registered
    try:
        with open("registrations.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2 and parts[0] == participant_id and parts[1] == event_id:
                    print("You have already registered for this event.")
                    return
    except FileNotFoundError:
        pass  # File doesn't exist yet, so no registrations recorded

    # Register for the event
    try:
        with open("registrations.txt", "a") as f:
            f.write(f"{participant_id},{event_id},{participant_id},Registered\n")
        print("Registration successful!")
    except IOError:
        print("Registration failed! Please try again.")



def cancel_registration(participant_id):
    registered = []#store the event_id that participant has registered
    try:    #read the event_id that had registered
        with open("registrations.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2 and parts[0] == participant_id:
                    registered.append(parts[1])
    except FileNotFoundError:
        print("Cannot find the records")
        return
    if not registered:
        print("No register any event")
        return

    print("\n---Your Registered Details---")
    try:    #print the form to display registered events
        with open("event.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if parts[0] in registered:
                    print(f"{parts[0]}\t{parts[1]}\t{parts[2]}\t{parts[3]}\t{parts[4]}")
    except FileNotFoundError:
        print("No information")
        return

    event_id = input("Enter the event ID you want to cancel: ").strip()

    if event_id not in registered:
        print("You are not registered for this event.")
        return

    try:#cancel registration
        with open("registrations.txt", "r") as file:
            lines = file.readlines()
        with open("registrations.txt", "w") as file:
            for line in lines:
                if not line.startswith(f"{participant_id},{event_id}"):
                    file.write(line)
        print("Registration cancel successfully.")
    except IOError:
        print("Failed to cancel registration.")


def view_personal_calendar(participant_id):
    registered = []
    location_dict = {}
    try:
        with open("venues.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    venue_id = parts[0].strip()
                    venue_name = parts[1].strip()
                    location_dict[venue_id] = venue_name
    except FileNotFoundError:
        print("VENUES FILE NOT EXISTING!")
        return
    try:#read the event_id that had registered
        with open("registrations.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2 and parts[0] == participant_id:
                    registered.append(parts[1])
    except FileNotFoundError:
        print("Cannot find the records")
        return
    if not registered:
        print("No registration any event")
        return
    print("\nYour Personal Calendar:")
    print("{:<10} {:<20} {:<12} {:<15} {:<30} {:<10}".format(
    "Event_id", "Event_title", "Date", "Location", "Description", "Capacity"))

    try:#print the calendar
        with open("event.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if parts[0] in registered:
                    location_id = parts[3]
                    location = location_dict.get(location_id, location_id)

                    print("{:<10} {:<20} {:<12} {:<15} {:<30} {:<10}".format(
            parts[0], parts[1], parts[2],location, parts[4], parts[5]))
    except FileNotFoundError:
        print("Cannot find your personal calendar")


participant_menu()