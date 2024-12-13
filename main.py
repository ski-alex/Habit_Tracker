import questionary

from analyse import Analyse
import display
from manage import Habit
from store import HabitsStore

habits_store = HabitsStore()
habits = habits_store.load()
Habit.update(habits)

print ("\nWELCOME to HABIT TRACKER 2024.\n")
if not Habit.check_habits_exist(habits):
    display.display_habits(habits, status_request = "Established", length = "short", filter_period = [1, 2, 7], 
                           headline ="Here is a quick overview of your currently tracked habits (active and broken):")
  
def cli_main(): 
    """ 
    Main function that runs the Habit Tracker CLI. 
    Displays the main menu and handles user choices. 
    """
    while True:
        print(f"\n \\\ MAIN MENU // ")
        choice = questionary.select(
            "\n What do you want to do?",
            choices=["Quick Check a habit", "Add a new habit", "Manage your habits", "Analyse your habits", "Save and Exit"]
        ).ask()

        if choice == "Quick Check a habit":
            if not Habit.check_habits_exist(habits):
                check()                
        elif choice == "Add a new habit":
            Habit.add(habits)
            habits_store.save(habits)
        elif choice == "Manage your habits":
            if not Habit.check_habits_exist(habits): 
                cli_sub_1()        
        elif choice == "Analyse your habits":
            if not Habit.check_habits_exist(habits):
                cli_sub_2()
        else: #"Save and Exit" was chosen
            habits_store.save(habits)
            print("Thanks for using Habit Tracker. Keep on tracking and see you soon!")
            break

def cli_sub_1():
    """ 
    Sub menu for managing habits. 
    Displays options to filter, check, delete, duplicate, adjust habits or return to the main menu. 
    """
    while True:
        print(f"\n \\\ SUB MENU - MANAGE // ")
        choice = questionary.select(
            "What do you want to do?",
            choices=["Filter habits", "Check a habit", "Delete a habit", "Duplicate a habit", "Adjust a habit", "Go back to Main Menu"]
        ).ask()

        if choice == "Filter habits":
            display.filter_habits(habits)
        elif choice == "Check a habit":
            check()
        elif choice == "Delete a habit":
            display.display_habits(habits, status_request = None,  length = "full", filter_period = [1, 2, 7], headline = "Here are all habits which can be deleted:")
            Habit.delete(habits)
            habits_store.save(habits)
        elif choice == "Duplicate a habit":
            display.display_habits(habits, status_request = None,  length = "full", filter_period = [1, 2, 7], headline = "Here are all habits which can be duplicated:")
            Habit.duplicate(habits)
            habits_store.save(habits)
        elif choice == "Adjust a habit":
            display.display_habits(habits, status_request = "Established",  length = "full", filter_period = [1, 2, 7], headline = "Here are all habits which can be adjusted:")
            Habit.adjust(habits)
            habits_store.save(habits)
        else: # "back" was chosen
            print("Back to Main Menu")
            break

def cli_sub_2():
    """ 
    Sub menu for analysing habits. 
    Displays options to analyse the habits with predefined analysefunctions, which are stored in "analyse.py", 
    or return to the main menu. 
    """
    while True:
        print(f"\n \\\ SUB MENU - ANALYSE //")
        choice = questionary.select(
            "What do you want to analyse?",
            choices=["All currently tracked habits", "All habits with the same periodicity", "Longest run streak of all defined habits", 
                     "Longest run streak for a given habit",
                     "Longest active streaks", "Most interruptions since creation (Top 3)","Most checks since creation (Top 3)", 
                     "Longest expired (Top 3)","Group by category","Go back to Main Menu"]
            ).ask()
        if choice == "All currently tracked habits":
            display.display_habits(habits, status_request = "Established", length = "short", filter_period = [1, 2, 7], 
                                   headline = "Here is an overview of all currently tracked habits (not established now):")
        elif choice == "All habits with the same periodicity":
            Analyse.get_habits_by_period(habits)
        elif choice == "Longest run streak of all defined habits":
            Analyse.get_top_main(habits, attribute = "streak_max", designation = "Max Streak")
        elif choice == "Longest run streak for a given habit":
            Analyse.get_habit_streak_max(habits)

        elif choice == "Longest active streaks":
            Analyse.get_top_main(habits, attribute = "streak", designation = "Streak")
        elif choice == "Most interruptions since creation (Top 3)":
            Analyse.get_top_most(habits, attribute="date_interruptions", designation = "interruptions")
        elif choice == "Most checks since creation (Top 3)":
            Analyse.get_top_most(habits, attribute="date_check", designation = "checks")
        elif choice == "Longest expired (Top 3)":
            Analyse.get_top_longest_expired(habits)
        elif choice == "Group by category":
            Analyse.get_group_habits_by_category(habits)

        else: # "back" was chosen
            print("Back to Main Menu")
            break

def check():
    """ 
    Function to check the status of active and broken habits. 
    Displays the respective habits and allows the user to check them. 
    """
    print(f"\nHere are all active and broken habits which can be checked:")
    display.display_habits(habits, status_request = "Established", length = "short", filter_period = [1, 2, 7], 
                           headline = "Here are all active and broken habits which can be checked:")
    Habit.check(habits)
    habits_store.save(habits)

if __name__ == "__main__":
    cli_main()