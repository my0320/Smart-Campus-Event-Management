###-------administrator-------###
from os import linesep


## fuction for approval proposal
def proposal_event():
    print("\n--- Event Proposal ---")
    found_pending = False  # search for pending event
    updated_lines = []  # update the event

    try:
        # read all events from the event.txt file
        with open("event.txt", "r") as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split(',')

            if len(parts) >= 8 and parts[7].lower() == "pending":
                found_pending = True
                print(f"ID: {parts[0]}, Title: {parts[1]}, Status: {parts[7]}")
                choice = input("Approve (A) / Reject (R) / Skip (Enter): ").upper()

                if choice == "A":
                    parts[7] = "Approved"
                    print("Approved event")
                elif choice == "R":
                    parts[7] = "Rejected"
                    print("Rejected event")
                else:
                    print("Skip")

            # save latest version of data (whether changed or not)
            updated_lines.append(','.join(parts) + '\n')
        if found_pending:
            # write back to the file
            with open("event.txt", "w") as file:
                file.writelines(updated_lines)
            print("all changed are saved")
        else:
            print("no pending proposals found")
        return
    except FileNotFoundError:
        print("File 'event.txt' not found.")


## statistic fuction
def statistics():
    total_events = 0
    pending_events = 0
    approved_events = 0
    rejected_events = 0
    participants = 0
    total_participants = 0
    event_participants = {}

    try:
        ##calculated participants from registrations.txt
        with open("registrations.txt", "r") as reg_file:
            for line in reg_file:
                parts = line.strip().split(',')
                if len(parts) >= 4 and parts[3].lower() == "registered":
                    total_participants += 1

        with open("event.txt", "r") as file:  # OPEN THE FILE FROM EVENT.TXT
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 8:
                    total_events += 1
                    status = parts[7].lower()
                    if status == "pending":  ##find the total of pending event
                        pending_events += 1
                    elif status == "approved":  ## find the total of approved event
                        approved_events += 1
                    elif status == "rejected":
                        rejected_events += 1


     ### print the statistics
        print("\n--- EVENT STATISTICS ---")
        print(f"Total events: {total_events}")
        print(f"Total pending events: {pending_events}")
        print(f"Total approved events: {approved_events}")
        print(f"Total rejected events: {rejected_events}")
        print(f"Total participant events: {total_participants}")

        ## find the most popular event
        if event_participants:  ## have to take data from participant to get the most popular event
            popular_event = max(event_participants, key=event_participants.get)  # we find the popular event based on the most number of participants
            print(f"The most popular event is: {popular_event}")
        else:
            print("no popular events")

    except FileNotFoundError:
        print("file doesn't exist")


### report function
def report():
    try:
        ##calculated participants from registrations.txt
        event_participants = {}
        with open("registrations.txt", "r") as reg_file:
            for line in reg_file:
                parts = line.strip().split(',')
                if len(parts) >= 2:  # asumsi: format = participant_id, event_id, ...
                    event_id = parts[1]
                    if event_id in event_participants:
                        event_participants[event_id] += 1
                    else:
                        event_participants[event_id] = 1

            ## create administrator report
        with open("administrator.txt", "w") as file:  # 'w' in here means write in order to write the report
            file.write("--- REPORT ---\n\n")
            try:
                with open("event.txt", "r") as event_file:
                    for line in event_file:
                        parts = line.strip().split(',')
                        event_id = parts[0] if len(parts) > 0 else 'invalid'  # len parts is fo
                        title = parts[1] if len(parts) > 1 else 'invalid'
                        status = parts[7] if len(parts) > 7 else 'invalid'
                        participant_count = event_participants.get(event_id, 0)

                        # Write to report file
                        file.write(f"ID       : {event_id}\n")
                        file.write(f"Title    : {title}\n")
                        file.write(f"Status   : {status}\n")
                        file.write(f"Participants: {participant_count}\n")  # this code for count all participant
                        file.write("-" * 40 + "\n")
                print("Event report generated: administrator.txt")
            except FileNotFoundError:
                print("Event file not found.")
    except Exception as e:
        print(f"An error occurred while generating the report: {e}")


#### manage roles
def manage_roles():
    while True:
        print("\n---MANAGE USER ROLES ---")
        print("changed participants  → organizer (P)")
        print("changed organizer  → participants (O)")
        print("exit (E)")
        choice = input("choose P/O/E: ").strip().upper()
        if choice == "P":
            changed_participant()
        elif choice == "O":
            changed_organizer()
        elif choice == "E":
            break
        else:
            print("invalid")

def changed_participant():  # this function is for changed the participant become organizers
    try:
        with open("participants.txt", "r") as file:  ### "r" is for read the participants.txt file to find the name of them
            lines = file.readlines()

        ##to show list of participants
        print("\n---participants list ---")  ##to show list of participant
        for line in lines:
            print(line.strip())
        ## input the name
        participant_name = input("Enter the name or ID of the participant to change: ")
        found = False
        new_participants = []

        with open("organizers.txt", "a") as org_file:  ##read organizers.txt "a" indicate to open the file for writing
            for line in lines:
                if participant_name in line.lower():
                    with open("organizers.txt", "a") as organizers_file:
                        organizers_file.write(line)
                    found = True
                    print(f"{line.strip()} has been changed to organizer")
                else:
                    new_participants.append(line)

        ## update participants.txt
        with open("participants.txt", "w") as file:
            file.writelines(new_participants)
        if not found:
            print("participant not found")

            # for print the participants list:
        print("\n--- List of Participants ---")
        for line in lines:
            print(line.strip())

        if not found:
            print("participant not found")
    except FileNotFoundError:
        print("participants file not found")

def changed_organizer():

    try:
        with open("organizers.txt", "r") as file:
            lines = file.readlines()

            ## to show list of organizers
            print("\n--- List of Organizers ---")
            for line in lines:
                print(line.strip())

        organizer_name = input("Enter the name or ID of the organizer to change: ").strip().lower()
        changed = False
        new_organizers = []
        with open("organizers.txt", "w") as file:
            for line in lines:
                if organizer_name in line.lower():
                    with open("participants.txt", "a") as part_file:
                        part_file.write(line)
                    changed = True
                    print(f"{line.strip()} has been changed to participant.")
                else:
                    new_organizers.append(line)

                # update the data in organizers.txt
            with open("organizers.txt", "w") as file:
                file.writelines(new_organizers)

            if not changed:
                print("organizer not found")
        if not changed:
            print("organizer not found")
    except FileNotFoundError:
        print("organizers.txt not found")


def admin_menu():
    admin_id = input("Enter your admin ID (e.g. Admin1): ").strip()
    name = input("Enter your name: ").strip()
    while True:
        print("\n[Admin Menu]")
        print("1. approve or reject proposal")
        print("2. view statistic")
        print("3. generate report")
        print("4. manage roles")
        print("5. EXIT")
        choice = input("enter your choice: ")
        if choice == "1":
            proposal_event()
        elif choice == "2":
            statistics()
        elif choice == "3":
            report()
        elif choice == "4":
            manage_roles()
        elif choice == "5":
            print("Logging out \n")
            break
        else:
            print("invalid")
admin_menu() ### call the main program