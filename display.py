from datetime import datetime, timedelta
from tabulate import tabulate

import manage
from manage import Habit
import questionary

def display_habits(habits, status_request, length, filter_period):
    """ 
    Displays habits in a formatted table. 
    
    Parameters: 
    habits (list): The list of habit objects to display. 
    status_request (str): The status of habits NOT to display. Displays habits with different statuses if None. 
    length (str): The level of detail for the table. Options are "full" or any other string for a shorter version.
    filter_period (list): List of periods which shall be displayed
    """
    if Habit.check_habits_exist(habits):
        return
    
    header = ["ID", "Name", "Category", "Period", "Target", "Streak", "Max Streak", "Created On", "Last Checked",  "Deadline", "Status", "Interruptions"]

    if length != "full":
        header = ["ID", "Name", "Category", "Period", "Target", "Streak", "Last Checked", "Deadline", "Status"]
    
    table_data = []

    for habit in habits:
        latest_check_date = max(habit.date_check, default="N/A")
        no_interruptions = len(habit.date_interruptions)
        period_word = manage.period_mapping[habit.period]

        if habit.status != status_request and habit.period in filter_period:
            
            row = [habit.id, habit.name, habit.category, period_word, habit.target, habit.streak, habit.streak_max, habit.date_create, latest_check_date, habit.deadline, habit.status, no_interruptions]
            if length != "full":
                row = [habit.id, habit.name, habit.category, period_word, habit.target, habit.streak, latest_check_date, habit.deadline, habit.status]
         
            table_data.append(row)

    print(tabulate(table_data, headers=header, tablefmt="github"))

def enter_filter (choices, attribute):
    """ 
    Prompts user to select filter values for a specified attribute. 
    
    Parameters: 
    choices (list): A list of choices to filter by. 
    attribute (str): The attribute to filter. 
    
    Returns: 
    list: The selected filter values. 
    """
    value = questionary.checkbox("Select at least one value you want to filter for:",choices).ask()
    print(f"You have chosen {' and '.join(value)}")
    print(f"Here are the results for all habits with {attribute} {' or '.join(value)}:")
    return value

def enter_comparison():
    """ 
    Prompts user to select a comparison type for numerical filtering. 
    
    Returns: 
    str: The selected comparison symbol ("=", ">", "<"). 
    """
    comp_word = questionary.select("For what do you want to filter?",choices=["exact value", "greater values", "smaller values"]).ask() 
    comp_symbol = {"exact value": "=", "greater values": ">", "smaller values": "<"}[comp_word] 
    return comp_symbol

def get_match(comp_symbol, value_compare, value): 
    """ 
    Determines if a value matches the comparison criteria. 
    
    Parameters: 
    comp_symbol (str): The comparison symbol ("=", ">", "<"). 
    value_compare (int/float/datetime): The value to compare. 
    value (int/float/datetime): The target value for comparison. 
    
    Returns: 
    bool: True if the value matches the comparison criteria, otherwise False. 
    """
    match = False 
    if comp_symbol == "=":
        match = value_compare == value 
    elif comp_symbol == ">": 
        match = value_compare > value 
    elif comp_symbol == "<": 
        match = value_compare < value 
    return match 

def filter_habits(habits):
    """ 
    Filters and displays habits based on user-selected criteria. 

    Parameters: 
    habits (list): The list of habit objects to filter and display. 
    """
    if Habit.check_habits_exist(habits):
        return
    
    attribute = questionary.select(
        "Which attribute do you want to filter?",
        choices=["ID", "Name", "Category", "Period", "Target", "Streak", "Max Streak", "Created On", "Deadline", "Status"]).ask().lower()
    
    if attribute in ["id", "target", "streak", "max streak"]: 
        wording = attribute
        if attribute == "max streak": 
            attribute = "streak_max"
        comp_symbol = enter_comparison() 
        while True: 
            try: 
                value = int(questionary.text(f"The values should be {comp_symbol} ...").ask()) 
                if value >= 0:
                    break
                else: 
                    print("Invalid input. Please enter a positive integer.") 
            except ValueError: 
                print("Invalid input. Please enter a positive integer.")

        print(f"Here are the results for all habits with {wording} {comp_symbol} {value}:")

    elif attribute == "name":
        value = questionary.text("What should the attribute name contain?").ask().lower()
        print(f"Here are the results for all habits with a name containing {value}:")

    elif attribute == "status":
        value = enter_filter (choices=manage.status_list, attribute = attribute)

    elif attribute == "category":
        value = enter_filter (choices=manage.categories, attribute = attribute)

    elif attribute == "period":
        value = enter_filter (choices=manage.periods, attribute = attribute)
        value = [manage.period_mapping[p] for p in value]

    elif attribute in ["created on", "deadline"]:
        wording = attribute 
        if attribute == "created on":
            attribute = "date_create" 
        comp_symbol = enter_comparison() 
        while True: 
            date_str = questionary.text(f"The values should be {comp_symbol}...(Enter a date in the format YYYY-MM-DD):").ask() 
            try: 
                value = datetime.strptime(date_str, '%Y-%m-%d') 
                break 
            except ValueError: 
                print("Incorrect format. Please enter the date in YYYY-MM-DD format.")
        print(f"Here are the results for all habits with a {wording} value {comp_symbol} {value}:")

    header = ["ID", "Name", "Category", "Period", "Target", "Streak", "Max Streak", "Created On", "Last Checked", "Deadline", "Status", "Interruptions"]
    table_data = []
    
    for habit in habits:
  
        match = False
        if attribute in ["id", "target", "streak", "streak_max"]:
            value_compare = getattr(habit, attribute)
            match = get_match(comp_symbol, value_compare, value)

        elif attribute in ["date_create", "deadline"]: 
            value_compare = datetime.strptime(getattr(habit, attribute), '%Y-%m-%d')
            match = get_match(comp_symbol, value_compare, value)

        elif attribute == "name":
            if value in str(getattr(habit, attribute)).lower():
                match = True

        elif attribute in ["category", "status"]:
            if getattr(habit, attribute).lower() in [v.lower() for v in value]:
                match = True

        elif attribute == "period": 
            if getattr(habit, attribute) in value:
                match = True

        if match: 
            latest_check_date = max(habit.date_check, default="N/A")
            no_interruptions = len(habit.date_interruptions)
            period_word = manage.period_mapping[habit.period]
            
            row = [habit.id, habit.name, habit.category, period_word, habit.target, habit.streak, habit.streak_max, habit.date_create, latest_check_date, habit.deadline, habit.status, no_interruptions]
            table_data.append(row)
    
    print(tabulate(table_data, headers=header, tablefmt="github"))

