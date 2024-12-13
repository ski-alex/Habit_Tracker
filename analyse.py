from datetime import datetime

from tabulate import tabulate
import questionary

import display
import manage

class Analyse:
    """ 
    A class to analyse and display habit-related data. 
    """
    @classmethod
    def get_top_main(cls, habits, attribute, designation):
        """ 
        Sorts and displays habits based on a specified attribute in ascending or descending order. 
        
        Parameters: 
        habits (list): The list of habit objects to analyse. 
        attribute (str): The attribute of the habit to sort by. 
        designation (str): A descriptive name for the attribute being sorted. 
        """
        order = cls.choose_order()
        sorted_habits = sorted(habits, key=lambda habit: getattr(habit, attribute), reverse=order)
        top = sorted_habits

        table_data = []
        for habit in top:
            if getattr(habit, attribute) > 0:
                table_data.append([habit.id, habit.name, getattr(habit, attribute), habit.status])
        if not table_data:
            print(f"\nNo results found for this filter.")
        else:
            order_text = "descending" if order else "ascending"
            print(f"\nHere is a {order_text} list of all habits that have a {designation} > 0:")
            print(tabulate(table_data, headers=["ID", "Name", f"{designation.capitalize()}", "Status"], tablefmt="github"))

    @classmethod
    def get_top_most(cls, habits, attribute, designation):
        """ 
        Finds and displays the top 3 habits based on the length of a specified attribute. 
        
        Parameters: 
        habits (list): The list of habit objects to analyse. 
        attribute (str): The attribute of the habit to sort by length. 
        designation (str): A descriptive name for the attribute being sorted. 
        """
        sorted_habits = sorted(habits, key=lambda habit: len(getattr(habit, attribute)), reverse=True)
        top_3_habits = sorted_habits[:3]

        table_data = []
        for habit in top_3_habits:
            if len(getattr(habit, attribute)) > 0:
                table_data.append([habit.id, habit.name, len(getattr(habit, attribute)), habit.status])
        if not table_data:
            print(f"\nNo results found for this filter.")
        else:
            print(f"\nHere are the top 3 of your habits with the most {designation} since creation:")
            print(tabulate(table_data, headers=["ID", "Name", f"{designation.capitalize()}", "Status"], tablefmt="github"))

    @classmethod
    def get_top_longest_expired(cls, habits):
        """ 
        Finds and displays the top 3 habits that have not been worked on for the longest time. 
        
        Parameters: 
        habits (list): The list of habit objects to analyse. 
        """
        now = datetime.now().strftime("%Y-%m-%d")

        habit_deadline_dates = [(habit, datetime.strptime(habit.deadline, "%Y-%m-%d")) for habit in habits]
        sorted_habits = sorted(habit_deadline_dates, key=lambda item: item[1], reverse=False)
        top_3_habits = sorted_habits[:3]

        table_data = []
        for habit, deadline_date in top_3_habits:
            if habit.deadline < now and habit.status == "Broken":
                table_data.append([habit.id, habit.name, habit.deadline, habit.status])

        if not table_data:
            print(f"\nNo results found for this filter.")
        else:
            print(f"\nHere are the top 3 of your habits that have not been worked on for the longest time:")
            print(tabulate(table_data, headers=["ID", "Name", "Deadline", "Status"], tablefmt="github"))


    @classmethod
    def get_group_habits_by_category(cls, habits):
        """ 
        Groups and displays all habits by their categories. 
        
        Parameters: 
        habits (list): The list of habit objects to analyze. 
        """
        all_categories = manage.CATEGORIES

        category_count = {category: {'total': 0, 'active': 0, 'broken': 0, 'established': 0} for category in all_categories}

        for habit in habits:
            if habit.category in category_count:
                category_count[habit.category]['total'] += 1
                if habit.status == "Active":
                    category_count[habit.category]['active'] += 1
                elif habit.status == "Broken":
                    category_count[habit.category]['broken'] += 1
                elif habit.status == "Established":
                    category_count[habit.category]['established'] += 1

        table_data = []
        for category, counts in category_count.items():
            table_data.append([category, counts['total'], counts['active'], counts['broken'], counts['established']])
        if not table_data:
            print(f"\nNo results found for this filter.")
        else:
            print(f"\nHere is a grouping of all habits by category:")
            print(tabulate(table_data, headers=["Category", "Total", "Active", "Broken", "Established"], tablefmt="github"))

    @classmethod
    def get_habit_streak_max(cls, habits):
        """ 
        Displays the maximum streak ("Longest Streak per Habit") of a specific habit selected by the user. 
        
        Parameters: 
        habits (list): The list of habit objects to analyze. 
        """
        display.display_habits(habits, status_request = None,  length = "short", filter_period= [1,2,7], headline = "")
        try:
            habit_id = int(questionary.text(f"\nPlease enter the ID of the habit you want to see:").ask())
        except ValueError:
            print(f"\nInvalid input. Please enter one of the numeric IDs you can see in the list above.")
            return
        if not any(habit.id == habit_id for habit in habits):
            print(f"\nNo habit found with ID {habit_id}. Please enter a numeric ID you can see in the list above.")
            return

        habit = None
        for h in habits:
            if h.id == habit_id:
                habit = h
                break

        table_data = [[habit.id, habit.name, habit.streak_max, habit.status]]
        print(tabulate(table_data, headers=["ID", "Name", "Streak Max", "Status"], tablefmt="github"))

    @classmethod
    def get_habits_by_period(cls, habits):
        """ 
        Displays all habits that have the same period. 
        
        Parameters: 
        habits (list): The list of habit objects to analyze. 
        """
        period_word = questionary.select("Select the period for which you want to display habits:", choices = manage.PERIODS ).ask()
        period = manage.PERIOD_MAPPING[period_word]
        
        display.display_habits(habits, status_request = None, length = "short", filter_period = [period], 
                               headline =f"\nHere are all habits with a period of '{period_word}'.")
    
    @staticmethod
    def choose_order():
        """ 
        Allows the user to choose the order (ascending or descending) for sorting. 
        
        Returns: 
        bool: True if descending, False if ascending. 

        Used by:
        analyse.get_top_main()
        """
        choice = questionary.select(f"\nShould the list be in ascending or descending order?",choices=["ascending", "descending"]).ask()
        order = {"descending": True ,"ascending" : False}[choice]
        return order