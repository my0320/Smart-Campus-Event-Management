#-----------------Venue Manager-------------------------
import datetime
import time

#-----------------Function 1-------------------------
def view_upcoming_events():
    while True:
        print("\n-------------------------------------------")
        print("\t\tWelcome to event schedule.")

        today = datetime.date.today()
        events_by_venue = {}
        venue_id_to_name = {}

        try:
            with open("venues.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) >= 2:
                        venue_id = parts[0].strip()
                        venue_name = parts[1].strip().title()
                        venue_id_to_name[venue_id] = venue_name
        except FileNotFoundError:
            print("venues.txt not found. Cannot resolve venue names.")

        try:
            with open('event.txt','r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("Error! No File Found.")
            return

        for line in lines:
            parts = line.strip().split(",")
            if len(parts) < 8:
                continue

            eventID = parts[0].strip()
            event_name = parts[1].strip()
            event_date_str = parts[2].strip()
            venue_id = parts[3].strip().lower()
            event_status = parts[7].strip().lower()
            venue_status = parts[8].strip().lower()
            venue = venue_id_to_name.get(venue_id, venue_id)  # fallback to venue ID if not found

            if event_status != "approved" or venue_status != "approved":
                continue
            try:
                event_date = datetime.datetime.strptime(event_date_str, "%Y-%m-%d").date()
            except ValueError:
                continue
            if event_date < today:
                continue
            if venue not in events_by_venue:
                events_by_venue[venue] = []
            events_by_venue[venue].append((event_name, event_date))
        if not events_by_venue:
            print("No Approved Upcoming Events Available.\nPlease Check Again Later.")
            return

        for venue in sorted(events_by_venue):
            print(f"\n{venue}:")
            sorted_events = sorted(events_by_venue[venue], key=lambda x: x[1])
            for i, (name, date) in enumerate(sorted_events, start=1):
                print(f"{i}. {name}, {date.strftime('%Y-%m-%d')}")

        while True:
            print("\nDo you want to exit?")
            choice = input("yes/no:").lower()
            if choice == "yes":
                print("Exiting... Please be patient.")
                time.sleep(2)
                return
            elif choice == "no":
                time.sleep(1)
            else:
                print("Invalid choice. Please type again.")


#-----------------Function 2-------------------------

def mark_venue_status():
    while True:
        print("\n-------------------------------------------")
        print("\t\tWelcome to venue status.")
        print("1. Update Venue Details.")
        print("2. Mark Venue Status.")
        print("3. View Venue Status")
        print("4. Exit.")

        choice = input("Enter your choice (1-4) :")

        if choice == "1":
            Update_Venue_Details()
        elif choice == "2":
            Mark_Venue_Status()
        elif choice == "3":
            View_Venue_Status()
        elif choice == "4":
            print("Exiting...Please be patient.")
            time.sleep(3)
            return
        else:
            print("Invalid choice. Please try again.")

def Update_Venue_Details():
    print("\n-------------------------------------------")
    venueID = input("Enter Venue ID:").strip().lower()
    venue = input("Enter new venue:").strip().lower()
    venue_status = input("Enter venue's status:(available/unavailable):").strip().lower()

    if venue_status not in ["available", "unavailable"]:
        print("Invalid status. Only 'available' or 'unavailable' are allowed.")
        return
    #Check is that repeat
    try:
        with open('venues.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == "":
                    continue
                parts = line.strip().split(",")
                if len(parts) < 3:
                    continue
                existing_id = parts[0].strip().lower()
                existing_venue = parts[1].strip().lower()
                if venueID == existing_id or venue == existing_venue:
                    print("Error: Venue ID or venue name already exists.")
                    return
    except FileNotFoundError:
        pass #Continue if the file not found

    #get unavailable reason
    if venue_status == "unavailable":
        reason = input("Enter the reason for being unavailable: ").strip()
    else:
        reason = "N/A"

    #write file
    try:
        with open('venues.txt', 'a') as file:
            file.write(f"{venueID},{venue},{venue_status},{reason}\n")
        print(f"\nVenue created successfully! VenueID: {venueID}")
    except IOError:
        print("Error: Could not save event to file.")

def Mark_Venue_Status():
    print("\n-------------------------------------------")
    try:
        with open('venues.txt','r')as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found.")
        return

    updated_lines = []
    location = input("Enter venue you want to update status:").strip().lower()
    found = False
    status_changed = False

    for line in lines:
        if line.strip() == "":
            updated_lines.append(line)
            continue
        content = line.strip().split(",")
        if len(content) < 3:
            updated_lines.append(line)
            continue
        venueid = content[0].strip()
        venue = content[1].strip().lower()
        status = content[2].strip().lower()

        if location == venue:
            found = True
            print(f"{venue} found.Current status:{status}.")
            reason = "N/A"

            if status == "available":
                print("Update status to Unavailable?")
                status_update_confirm = input("yes/no:").lower()
                if status_update_confirm == "yes":
                    status = "unavailable"
                    reason = input("Enter reason for unavailability:").strip()
                    print(f"Status updated successfully! Status:{status}")
                    status_changed = True
                elif status_update_confirm == "no":
                    print("Status not changed.")
                else:
                    print("Invalid choice. Please try again.")
            elif status == "unavailable":
                print("Update status to Available?")
                status_update_confirm = input("yes/no:").lower()
                if status_update_confirm == "yes":
                    status = "available"
                    reason = "N/A"
                    print(f"Status updated successfully! Status:{status}")
                    status_changed = True
                elif status_update_confirm == "no":
                    print("Status not changed.")
                else:
                    print("Invalid choice. Please try again.")
                #替换这一行
            updated_line = f"{venueid},{venue},{status},{reason}\n"
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    if not found:
        print(f"{location} not found.")

        choice = input("Create a new venue? (yes/no):")

        if choice == "yes":
            newID = input("Enter Venue ID:").strip()
            new_status = input("Enter venue's status (available/unavailable):")
            if new_status =="unavailable":
                new_reason = input("Enter reason for unavailablity:").strip().lower()
            else:
                new_reason = "N/A"
            updated_lines.append(f"{newID},{location},{new_status},{new_reason}\n")
            print(f"New venue {location} added successfully.")
        elif choice == 'no':
            print("Nothing changed.")
        else:
            print("Invalid choice. Please try again.")
        #写回文件
    if found and status_changed or not found:
        with open('venues.txt','w') as file:
            for line in updated_lines:
                file.write(line)
    return

def View_Venue_Status():
    print("\n-------------------------------------------")
    no = 0
    try:
        with open('venues.txt', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found.")
        return
    if not lines:
        print("No venues data.")
    for line in lines:
        no+=1
        print(no,".",line)


#-----------------Function 3-------------------------
def venue_requestment():
    while True:
        print("\n-------------------------------------------")
        print("\t\tWelcome to venue requestment.")
        print("1. View Venue Booking Request.")
        print("2. Approve or Reject Venue Booking Request.")
        print("3. Exit.")

        choice = input("Enter your choice (1-3) :")

        if choice == "1":
            View_Venue_Request()
        elif choice == "2":
            Approve_Deny_Booking_Reqeust()
        elif choice == "3":
            print("Exiting...Please be patient.")
            time.sleep(3)
            return
        else:
            print("Invalid choice. Please try again.")

def View_Venue_Request():
    print("\n-------------------------------------------")
    no = 0
    try:
        with open('venue_requests.txt','r') as file:
            requests = file.readlines()
    except FileNotFoundError:
        print("No booking requests found.")
        return
    if not requests:
        print("No venues requests available.")

    print("\t\tVenue Booking Request")
    for line in requests:
        no += 1
        print(f"{no}.{line}")

def Approve_Deny_Booking_Reqeust():
    try:
        with open('venue_requests.txt','r') as file:
            requests = file.readlines()
    except FileNotFoundError:
        print("No booking requests found.")
        return
    if not requests:
        print("No venues requests available.")

    View_Venue_Request()
    try:
        request_id = int(input("Enter the request ID（eg: 1,2,3):"))-1
        if request_id <0 or request_id >= len(requests):
            print("Invalid request ID.")
            return

    except ValueError:
        print("Invalid input. Please enter number(ex:1).")
        return

    content = requests[request_id].strip().split(",")
    if len(content) <6:
        print("Invalid request format. Cannot process.")
        return

    eventid = content[0].strip()
    venueid = content[1].strip()
    venue = content[2].strip().lower()
    request_date = content[3].strip()
    organizer_id = content[4].strip()
    status = content[5].strip().lower()

    print(f"Request found.\nEvent ID:{eventid}\nVenue:{venue}\nRequest Date:{request_date}\nCurrent Status:{status}\n")

    choice = input("Approve or deny this request?(approved/denied):").strip().lower()
    if choice not in ["approved","denied"]:
        print("Invalid choice. Please try again.")
        return
    updated_line = f"{eventid},{venueid},{venue},{request_date},{organizer_id},{choice}\n"
    requests[request_id] = updated_line

    try:
        with open('event.txt','r')as file:
            event_lines = file.readlines()
        new_event_lines = []
        for line in event_lines:
            parts = line.strip().split(",")
            if len(parts) >= 9 and parts[0] == eventid:
                parts[8] = choice.capitalize() #capital Approved/Denied
                new_line = ','.join(parts)+'\n'
                new_event_lines.append(new_line)
            else:
                new_event_lines.append(line)
        with open('event.txt','w')as file:
            file.writelines(new_event_lines)
        print(f"Venue status of event record in 'event.txt' has been updated")
    except FileNotFoundError:
        print("Error:File not found.")
    except IOError:
        print("Failed to update event venue status.")

    with open('venue_requests.txt','w') as file:
        for line in requests:
            file.write(line)
    print(f"Request has been {choice}d successfully.")

    # === Automatically mark venue as unavailable and write reason ===
    if choice == "approved":
        try:
            with open('venues.txt', 'r') as file:
                venue_lines = file.readlines()
        except FileNotFoundError:
            print("venues.txt not found. Cannot update venue status.")
            return

        updated_venue_lines = []
        venue_found = False

        reason = input(f"Please enter the reason why '{venue}' is now unavailable: ").strip()

        for v_line in venue_lines:
            if v_line.strip() == "":
                updated_venue_lines.append(v_line)
                continue

            v_parts = v_line.strip().split(",")
            if len(v_parts) < 3:
                updated_venue_lines.append(v_line)
                continue

            vid = v_parts[0].strip()
            vname = v_parts[1].strip().lower()

            if vname == venue:
                venue_found = True
                updated_line = f"{vid},{vname},unavailable,{reason}\n"
                updated_venue_lines.append(updated_line)
            else:
                updated_venue_lines.append(v_line)

        if venue_found:
            with open('venues.txt', 'w') as file:
                file.writelines(updated_venue_lines)
            print(f"Venue '{venue}' marked as unavailable with reason: {reason}")
        else:
            print(f"Warning: Venue '{venue}' not found in venues.txt. Cannot update its status.")

#-----------------Function 4-------------------------
def suggest_venue():
    while True:
        print("\n-------------------------------------------")
        no = 0

        try:
            with open('venues.txt','r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("No file found.")
            return

        found = False

        print("\t\tWelcome to Venue Suggestion Area.\n")
        print("\tHere are the suggested available venue:\n")
        for line in lines:
            if line.strip() =="":
                continue
            content = line.strip().split(",")
            if len(content) < 3:
                continue
            venueid = content[0].strip()
            venue = content[1].strip().lower()
            status = content[2].strip().lower()

            if status == "available":
                found = True
                no += 1
                print(f"{no}.VenueID:{venueid},Venue:{venue},Status:{status}")
            else:
                pass

        if not found:
            print("No available venue now. Please try again later.")

        while True:
            print("Do you want to exit?")
            choice = input("yes/no:").lower()
            if choice == "yes":
                print("Exiting... Please be patient.")
                time.sleep(2)
                return
            elif choice == "no":
                time.sleep(1)
            else:
                print("Invalid choice. Please type again.")

#-----------------Venue Manager Menu-------------------------
def venue_manager_menu():
    while True:
        print("\n-------------------------------------------")
        print("\t\tWelcome to Venue Manager Menu.")
        print("1. View Upcoming Events Scheduled For Each Venue. ")
        print("2. Mark Venue's Unavailable Status.")
        print("3. Approve or Reject Venue Requests.")
        print("4. Suggest Alternative Venues.")
        print("5. Return to Main Menu.")

        choice = input("Enter your choice by selecting number:")
        if choice == "1":
            view_upcoming_events()
        elif choice == "2":
            mark_venue_status()
        elif choice == "3":
            venue_requestment()
        elif choice == "4":
            suggest_venue()
        elif choice == "5":
            print("Returning to Main Menu......")
            return
        else:
            print("Invalid choice. Please enter 1-5.")

venue_manager_menu()