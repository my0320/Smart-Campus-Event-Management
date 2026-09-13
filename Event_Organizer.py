# Event status constants
EVENT_STATUS = {
    "PENDING": "Pending",  # Event awaiting approval
    "APPROVED": "Approved",  # Event approved by admin
    "REJECTED": "Rejected",  # Event rejected by admin
    "CANCELLED": "Cancelled"  # Event cancelled by organizer
}

# Venue status constants
VENUE_STATUS = {
    "AVAILABLE": "Available",  # Venue is free
    "UNAVAILABLE": "Unavailable",  # Venue not in use
    "BOOKED": "Booked"  # Venue has been booked
}

# ====== Main Menu ======
def organizer_menu():
    """Organizer main menu system"""
    organizer_id = organizer_login()

    while True:
        print("\n--- Event Organizer Menu ---")
        print("1. Create a new campus event")
        print("2. Update event details")
        print("3. Cancel an existing event")
        print("4. View list of registered participants")
        print("5. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            create_event(organizer_id)
        elif choice == "2":
            update_event(organizer_id)
        elif choice == "3":
            cancel_event(organizer_id)
        elif choice == "4":
            view_participants(organizer_id)
        elif choice == "5":
            print("Exiting organizer menu...")
            break
        else:
            print("Invalid option. Please enter 1-5.")




def create_event(organizer_id):
    print("\n--- Create New Event ---")

    # Get event title
    title = input("Event Title: ").strip()
    while not title:
        print("Title cannot be empty")
        title = input("Event Title: ").strip()

    # Get and validate date
    from datetime import datetime, date
    while True:
        date_str = input("Date (YYYY-MM-DD): ").strip()
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if event_date < date.today():
                print("Error: Date cannot be in the past.")
                continue
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Check venue availability
    available_venues = get_available_venues(str(event_date))
    if not available_venues:
        print("No venues available for the selected date.")
        return

    # Display available venues
    print("\nAvailable Venues:")
    for i, venue in enumerate(available_venues, 1):
        print(f"{i}. {venue['name']} (ID: {venue['venue_id']})")

    # Select venue
    try:
        choice = int(input("Select venue (number): "))
        if choice < 1 or choice > len(available_venues):
            print("Invalid selection.")
            return
        selected_venue = available_venues[choice - 1]
    except ValueError:
        print("Please enter a valid number.")
        return

    # Get description
    description = input("Description: ").strip()
    while not description:
        print("Description cannot be empty")
        description = input("Description: ").strip()

    # Validate capacity
    capacity = input("Capacity: ").strip()
    while not capacity.isdigit() or int(capacity) <= 0:
        print("Capacity cannot be empty and must be a positive integer")
        capacity = input("Capacity: ").strip()

    # Generate event ID
    event_id = generate_event_id()

    # Create event record
    event_record = [
        event_id,
        title,
        str(event_date),
        selected_venue['venue_id'],
        description,
        capacity,
        organizer_id,
        EVENT_STATUS["PENDING"],
        "Requested"
    ]

    # Create venue request record
    venue_request = [
        event_id,
        selected_venue['venue_id'],
        selected_venue['name'],
        str(event_date),
        organizer_id,
        "Pending"
    ]

    # Save records
    try:
        with open("event.txt", 'a') as f:
            f.write(','.join(event_record) + '\n')

        with open("venue_requests.txt", 'a') as f:
            f.write(','.join(venue_request) + '\n')

        print(f"\nEvent created successfully! Event ID: {event_id}")
        print(f"Venue requested: {selected_venue['name']} (ID: {selected_venue['venue_id']})")
        print("Note: This event is pending admin approval and venue booking confirmation.")
    except IOError:
        print("Error: Could not save event to file.")


def update_event(organizer_id):
    print("\n--- Update Event ---")

    # Get organizer's events
    events = get_organizer_events(organizer_id)
    if not events:
        print("You have no events to update.")
        return

    # Display events
    print("\nYour Events:")
    for i, event in enumerate(events, 1):
        status = f"{event['status']}/{event['venue_status']}"
        print(f"{i}. {event['title']} (ID: {event['event_id']}, Status: {status})")

    # Select event
    try:
        choice = int(input("Select event to update: "))
        if choice < 1 or choice > len(events):
            print("Invalid selection.")
            return
        selected_event = events[choice - 1]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Check approval status
    if (selected_event['status'] != EVENT_STATUS["APPROVED"] or
            selected_event['venue_status'] != "Approved"):
        print("Only fully approved events can be updated.")
        return

    # Display current details
    print("\nCurrent Event Details:")
    print(f"1. Title: {selected_event['title']}")
    print(f"2. Date: {selected_event['date']}")
    print(f"3. Venue: {selected_event['venue_id']}")
    print(f"4. Description: {selected_event['description']}")
    print(f"5. Capacity: {selected_event['capacity']}")

    # Select field to update
    field = input("\nSelect field to update (1-5, 0 to cancel): ")
    if field == "0":
        return

    # Update title
    if field == "1":
        new_title = input("New title: ").strip()
        while not new_title:
            print("Title cannot be empty")
            new_title = input("New title: ").strip()
        selected_event['title'] = new_title

    # Update date
    elif field == "2":
        from datetime import datetime, date
        while True:
            new_date = input("New date (YYYY-MM-DD): ").strip()
            try:
                event_date = datetime.strptime(new_date, "%Y-%m-%d").date()
                if event_date < date.today():
                    print("Date cannot be in the past.")
                    continue

                # Check venue availability for new date
                if not get_available_venues(new_date):
                    print("No venues available on this date.")
                    continue

                selected_event['date'] = new_date
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")

    # Update venue
    elif field == "3":
        new_date = selected_event['date']
        available_venues = get_available_venues(new_date)

        if not available_venues:
            print("No venues available for this date.")
            return

        print("\nAvailable Venues for the new date:")
        for i, venue in enumerate(available_venues, 1):
            print(f"{i}. {venue['name']} (ID: {venue['venue_id']})")

        try:
            choice = int(input("Select new venue: "))
            if choice < 1 or choice > len(available_venues):
                print("Invalid selection.")
                return
            selected_event['venue_id'] = available_venues[choice - 1]['venue_id']
        except ValueError:
            print("Please enter a valid number.")
            return

    # Update description
    elif field == "4":
        new_desc = input("New description: ").strip()
        while not new_desc:
            print("Description cannot be empty")
            new_desc = input("New description: ").strip()
        selected_event['description'] = new_desc

    # Update capacity
    elif field == "5":
        # Get current registration count
        current_registrations = 0
        try:
            with open("registrations.txt", 'r') as f:
                registrations = [line.strip().split(',') for line in f]
            current_registrations = sum(1 for reg in registrations
                                        if len(reg) >= 4 and reg[1] == selected_event['event_id'] and reg[
                                            3] == "Registered")
        except FileNotFoundError:
            pass

        while True:
            new_cap = input(f"New capacity (current registrations: {current_registrations}): ")
            if new_cap.isdigit():
                new_cap_int = int(new_cap)
                if new_cap_int <= 0:
                    print("Capacity must be positive.")
                elif new_cap_int < current_registrations:
                    print("Capacity cannot be less than current registrations.")
                else:
                    selected_event['capacity'] = new_cap
                    break
            else:
                print("Please enter a valid number.")

    # Save updates
    if update_event_record(selected_event):
        print("Event updated successfully!")
    else:
        print("Failed to update event.")


def cancel_event(organizer_id):
    print("\n--- Cancel Event ---")

    # Get organizer's events
    events = get_organizer_events(organizer_id)
    if not events:
        print("You have no events to cancel.")
        return

    # Display events
    print("\nYour Events:")
    for i, event in enumerate(events, 1):
        print(f"{i}. {event['title']} (ID: {event['event_id']}, Status: {event['status']})")

    # Select event
    try:
        choice = int(input("Select event to cancel: "))
        if choice < 1 or choice > len(events):
            print("Invalid selection.")
            return
        selected_event = events[choice - 1]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Check current status
    if selected_event['status'] == EVENT_STATUS["CANCELLED"]:
        print("Event is already cancelled.")
        return
    if selected_event['status'] == EVENT_STATUS["REJECTED"]:
        print("Cannot cancel a rejected event.")
        return

    # Confirmation
    confirm = input(f"Confirm cancel '{selected_event['title']}'? (yes/no): ").lower()
    if confirm != "yes":
        print("Cancellation aborted.")
        return

    # Update event status
    selected_event['status'] = EVENT_STATUS["CANCELLED"]

    # Update registrations
    updated_registrations = []
    try:
        with open("registrations.txt", 'r') as f:
            registrations = [line.strip().split(',') for line in f]
        for reg in registrations:
            if len(reg) >= 4 and reg[1] == selected_event['event_id'] and reg[3] == "Registered":
                reg[3] = "Cancelled"
            updated_registrations.append(reg)

        with open("registrations.txt", 'w') as f:
            for reg in updated_registrations:
                f.write(','.join(reg) + '\n')
    except FileNotFoundError:
        pass

    # Save changes
    if update_event_record(selected_event):
        print("Event cancelled successfully.")
    else:
        print("Failed to cancel event.")


def view_participants(organizer_id):
    print("\n--- View Participants ---")

    # Get approved events
    events = [e for e in get_organizer_events(organizer_id)
              if e['status'] == EVENT_STATUS["APPROVED"] and
              e['venue_status'] == "Approved"]

    if not events:
        print("No approved events available.")
        return

    # Display events with registration counts
    print("\nYour Approved Events:")
    for i, event in enumerate(events, 1):
        reg_count = 0
        try:
            with open("registrations.txt", 'r') as f:
                registrations = [line.strip().split(',') for line in f]
            reg_count = sum(1 for reg in registrations
                            if len(reg) >= 4 and reg[1] == event['event_id'] and reg[3] == "Registered")
        except FileNotFoundError:
            pass

        print(f"{i}. {event['title']} (ID: {event['event_id']}) - {reg_count}/{event['capacity']} participants")

    # Select event
    try:
        choice = int(input("Select event to view participants: "))
        if choice < 1 or choice > len(events):
            print("Invalid selection.")
            return
        selected_event = events[choice - 1]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Get participants
    participants = []
    participant_details = []

    # Read participants data
    try:
        with open("participants.txt", 'r') as f:
            participant_details = [line.strip().split(',') for line in f]
    except FileNotFoundError:
        pass

    # Find registered participants
    try:
        with open("registrations.txt", 'r') as f:
            registrations = [line.strip().split(',') for line in f]
        for reg in registrations:
            if len(reg) >= 4 and reg[1] == selected_event['event_id'] and reg[3] == "Registered":
                # Find participant details
                for part in participant_details:
                    if part and part[0] == reg[2]:
                        participants.append({
                            'id': part[0],
                            'name': part[1]
                        })
                        break
    except FileNotFoundError:
        pass

    # Display participants
    if not participants:
        print("\nNo participants registered for this event.")
        return

    print(f"\nParticipants for '{selected_event['title']}':")
    for i, part in enumerate(participants, 1):
        print(f"{i}. {part['name']} (ID: {part['id']})")


# ====== Organizer Features ======
def organizer_login():
    # Get organizer ID input and remove any leading/trailing whitespace
    organizer_id = input("Enter your Organizer ID (e.g. O001): ").strip()
    name = input("Enter your name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter your name: ").strip()

    # Flag to track if organizer is found in the file
    found = False

    try:
        # Try to open the organizers.txt file in read mode
        with open("organizers.txt", "r") as file:
            # Check each line in the file
            for line in file:
                # Split the line by comma and compare the first part (ID) with the input ID
                if line.strip().split(",")[0] == organizer_id:
                    found = True  # Organizer exists in file
                    break
    except FileNotFoundError:
        pass

    # If organizer wasn't found in the file
    if not found:
        try:
            # Open file in append mode to add new organizer
            with open("organizers.txt", "a") as file:
                # Write the new organizer's ID and name to the file
                file.write(f"{organizer_id},{name}\n")
            print(f"Welcome, {name}! You are now registered as an organizer.")
        except IOError:
            print("Error saving organizer information.")

    # Return the organizer ID (whether it was new or existing)
    return organizer_id

def generate_event_id():
    max_id = 0      # Create a variable max_id to store the maximum number (digital part) found so far, which is used to generate the next number
    try:
        with open("event.txt","r") as f:                 # 'r' indicates read mode
            for line in f:                               # Read file contents line by line
                event_id = line.strip().split(',')[0]    # line.strip() removes leading and trailing spaces or line breaks, .split(',')[0] separates the line by commas and extracts the first field (usually the activity ID)
                if event_id.startswith('EVT'):           # id start with EVT
                    number = event_id[3:]                # Starting from the 4th character, cut off the following part (number)
                    if number.isdigit():
                        max_id = max(max_id, int(number))        # Compare the current digital number with the existing maximum number max_id and take the larger value
    except FileNotFoundError:
        pass

    return f"EVT{max_id + 1 :04d}"                         # max_id + 1 indicates the next available number. :04d indicates that this number always takes up 4 digits, and the missing digits are padded with 0s, for example 1 → 0001. f"EVT{...}" is string formatting, spelling out an ID like EVT0004

# ====== Helper Functions ======
def get_organizer_events(organizer_id):
    """Get all events for a specific organizer"""
    events = []     # Create an empty list events, and then add the events that meet the conditions.
    try:
        with open("event.txt", 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                # Ensure valid record and match organizer ID
                if len(parts) >= 8 and parts[6] == organizer_id:        # len(parts) >= 8: Ensure that the row has at least 8 fields, and organizer_id is at index 6
                    event = {
                        'event_id': parts[0],
                        'title': parts[1],
                        'date': parts[2],
                        'venue_id': parts[3],
                        'description': parts[4],
                        'capacity': parts[5],
                        'organizer_id': parts[6],
                        'status': parts[7],
                        'venue_status': parts[8] if len(parts) > 8 else "Requested",
                        'participants': parts[9:] if len(parts) > 9 else []  # Participants from index 9 onwards
                    }
                    events.append(event)
    except FileNotFoundError:
        print("event.txt not found. Returning empty event list.")
    except IOError:
        print("Error reading event.txt file.")
    return events


def update_event_record(updated_event):
    """Update event record in events file"""
    try:
        # Read all events
        with open("event.txt", 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("event.txt not found. Update failed.")
        return False

    updated = False
    new_lines = []
    for line in lines:
        parts = line.strip().split(',')
        if parts and parts[0] == updated_event['event_id']:
            # Update the event record
            new_record = [
                updated_event['event_id'],
                updated_event['title'],
                updated_event['date'],
                updated_event['venue_id'],
                updated_event['description'],
                updated_event['capacity'],
                updated_event['organizer_id'],
                updated_event['status'],
                updated_event['venue_status']
            ]
            # Preserve participants if they exist
            if len(parts) > 9:
                new_record.extend(parts[9:])
            new_line = ','.join(new_record) + '\n'
            new_lines.append(new_line)
            updated = True
        else:
            new_lines.append(line)

    if updated:
        try:
            with open("event.txt", 'w') as f:
                f.writelines(new_lines)
            return True
        except IOError:
            print("Error writing to event.txt")
            return False
    return False

def get_available_venues(date):
    """Returns a list of venues that are available on the given date"""
    available_venues = []

    # First get all venues from venues file (format: venue_id, venue, venue_status)
    try:
        with open("venues.txt", 'r') as f:
            all_venues = []
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 3:  # New format: venue_id, venue, venue_status
                    all_venues.append({
                        'venue_id': parts[0].strip(),
                        'name': parts[1].strip(),  # venue name
                        'status': parts[2].strip()
                    })
    except FileNotFoundError:
        print("Venues data not found. Please contact administrator.")
        return []

    # Then get all booked venues for the selected date
    booked_venue_ids = set()
    try:
        with open("event.txt", 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 4 and parts[2] == date and parts[7] != "Cancelled":
                    # If event is on same date and not cancelled, venue is booked
                    booked_venue_ids.add(parts[3])  # parts[3] is venue_id
    except FileNotFoundError:
        pass  # No events exist yet

    # Filter venues that are available (not booked and not under maintenance)
    for venue in all_venues:
        if (venue['venue_id'] not in booked_venue_ids and
            venue['status'].lower() != 'unavailable'):
            available_venues.append(venue)

    return available_venues

# ====== Program Entry Point ======
organizer_menu()
