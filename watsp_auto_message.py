# wa auto reminder

import sys
import csv
import pywhatkit as pwa
import pyautogui as pgui
from datetime import datetime

def send_group_message(groupid, message):
    # using Exception Handling to avoid unexpected errors
    try:
        # "Group name" must be the group ID of the WhatsApp group. The admin has that data.
        # You can get the data from the link used to become part of the group.
        pwa.sendwhatmsg_to_group_instantly(groupid, message)
        pgui.click(1500,990, button='left', clicks=1)
        print("Message Sent!")
    except:
        print("Error in sending the message")


def prepare_message(message, event_list):
    for event_data in event_list:
        print(f"  {event_data['name']}'s birthday is on {event_data['date'].strftime('%Y-%m-%d')}")
        message +=  "`" + event_data['name'] + "`(" + event_data['date'].strftime('%Y-%m-%d') + "); "
    return message


def get_events_by_month(events, target_month):
    bdays_by_month = []
    annivs_by_month = []

    count = 0
    for event_data in events:
        friend_name = event_data['name']
        event_type = event_data['type']
        event_date_str = event_data['date']

        count = count + 1

        print(f"Processing {friend_name}'s {event_type} on {event_date_str}")

        try:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d')
            month = event_date.month

            # Check if the event is in the target month
            if month == target_month:
                if(event_type == "Birthday"):
                    bdays_by_month.append({'name': friend_name, 'date': event_date})
                elif(event_type == "Anniversary"):
                    annivs_by_month.append({'name': friend_name, 'date': event_date})
                else:
                    raise ValueError(
                        f"Unknown event type {event_type}")
                print(f"Adding {friend_name}'s {event_type} on {event_date_str} to list")

        except ValueError:
            print(f"Invalid date format: {event_date_str}")
    print("Count = ", count)
    return bdays_by_month, annivs_by_month


def main():
    """ Main function to support extraction of birthdays and anniversaries
        from a CSV file and sending them to a WhatsApp group
    """

    argc = len(sys.argv)
    if argc != 2:
        print("Usage: python3.8 watsp_auto_message.py month_number")
        sys.exit(1)

    target_month       = int(sys.argv[1])
    groupid = "C2YVXcRt3pF4Xean9GhIVE" #Local Reference
    groupid = "BuicS8SQYx415Z1dnrWVg8" #Game Plan

    events = []
    with open('events.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            events.append(row)
    print(events)

    bdays_by_month, annivs_by_month = get_events_by_month(events, target_month)
    print()
    print(bdays_by_month)
    print(annivs_by_month)
    print()

    message_header = "*Birthdays:* "
    message = prepare_message(message_header, bdays_by_month)
    print(message)
    send_group_message(groupid, message)

    message_header = "*Anniversary:* "
    message = prepare_message(message_header, annivs_by_month)
    print(message)
    send_group_message(groupid, message)


if __name__ == '__main__':
    # at least the CLI program name: (CLI) execution
    main()
