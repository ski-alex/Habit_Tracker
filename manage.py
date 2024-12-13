from datetime import datetime, timedelta

import questionary

CATEGORIES = ["Health", "Lifestyle", "Sport", "Education", "Other"]
PERIODS = ["Daily", "Every two days", "Weekly"]
STATUS_LIST = ["Active", "Broken", "Established"]
PERIOD_MAPPING = {"Daily": 1, "Every two days": 2, "Weekly": 7, 1:"Daily", 2:"Every two days", 7:"Weekly"}

class Habit:
    def __init__(self, id, name, category, period, target, streak=0, streak_max=0, date_create=None, date_check=None, deadline=None, status="Active", date_interruptions=None): 
        """ 
        Initializes a Habit object. 

        Parameters: 
        id (int): The unique identifier for the habit. Predefined by def get_id(habits):
        name (str): The name of the habit. 
        category (str): The category of the habit. 
        period (int): The interval in days between repetitions of the habit. 
        target (int): The target number of repetitions to establish the habit. 
        streak (int): The current streak of consecutive completions. 
        streak_max (int): The maximum streak of consecutive completions. 
        date_create (str): The date the habit was created. 
        date_check (list): The list of dates the habit was checked. 
        deadline (str): The next due date for the habit. 
        status (str): The current status of the habit (Active, Broken, Established). 
        date_interruptions (list): The list of dates when the habit was interrupted. 
        """
        self.id = id 
        self.name = name 
        self.category = category 
        self.period = int(period) 
        self.target = target 
        self.streak = streak 
        self.streak_max = streak_max 
        self.date_create = date_create or datetime.now().strftime("%Y-%m-%d") 
        self.date_check = date_check or [] 
        self.deadline = deadline or (datetime.now() + timedelta(days=period)).strftime("%Y-%m-%d") 
        self.status = status 
        self.date_interruptions = date_interruptions or []

    @classmethod
    def add(cls, habits):   
        """ 
        Adds a new habit to the habits list. 

        Parameters: 
        habits (list): The list of current habits. 
        """
        id = cls.get_id(habits)
        name = cls.enter_name()
        category = cls.enter_category()
        period = cls.enter_period()
        target = cls.enter_valid_target()
    
        new_habit = cls(id, name, category, int(period), target) 

        period_word = PERIOD_MAPPING[period].lower()
        confirmation = questionary.confirm(f"\nDo you want to add '{name}' in {category} and repeat it {period_word} for {target} times?").ask() 
        if confirmation:
            habits.append(new_habit) 
            print(f"'{name}' successfully added.")

    @classmethod
    def adjust(cls, habits):
        """ 
        Adjusts attributes selected by the user, 
        as well as attributes influenced by the attribute selected by the user.

        Parameters: 
        habits (list): The list of current habits. 
        """
        if cls.check_habits_exist(habits):
            return

        habit_id = cls.check_id_exists(habits, occasion_name="adjust")
        if habit_id is None:
            return

        habit_to_adjust = next((habit for habit in habits if habit.id == habit_id), None)

        if habit_to_adjust.status == "Established":
            print(f"\nThis habit is already established. If you want to re-establish this habit, you can use the “Duplicate” function.")
            return

        choice = questionary.select(
            "Which attribute do you want to adjust?",
            choices=["Name", "Category", "Period", "Target"]
        ).ask().lower()

        if choice == "name":
            new_value = cls.enter_name()
        elif choice == "category":
            new_value = cls.enter_category()
        elif choice == "period":
            new_value = cls.enter_period()
            habit_to_adjust.deadline = (datetime.now() + timedelta(days=new_value)).strftime("%Y-%m-%d")
        elif choice == "target": 
            print(f"\nThe new target must be greater than the current streak of {habit_to_adjust.streak}.")
            while True: 
                new_value = cls.enter_valid_target() 
                if new_value > habit_to_adjust.streak: 
                    break 
                else:
                    print(f"\nInvalid input. The new target must be greater than the current streak of {habit_to_adjust.streak}.")

        if habit_to_adjust:
            setattr(habit_to_adjust, choice, new_value)
            print(f"\nHabit no. {habit_id} has been adjusted. The new value for {choice} is now {new_value}.")


    @classmethod
    def check(cls, habits):
        """ 
        Checks the status of a habit.
        
        Parameters: 
        habits (list): The list of current habits. 
        """
        if cls.check_habits_exist(habits):
            return
        
        habit_id = cls.check_id_exists(habits, occasion_name="check")
        if habit_id is None:
            return
        
        confirmation = questionary.confirm(f"\nDo you really want to check habit no. {habit_id}?").ask()
        if confirmation:
            habit_to_check = next((habit for habit in habits if habit.id == habit_id), None)

            if habit_to_check.status == "Established":
                print(f"\nThis habit is already established. If you want to re-establish this habit, you can use the “Duplicate” function.")
                return
            else:
                habit_to_check.streak += 1
                habit_to_check.streak_max = max(habit_to_check.streak_max, habit_to_check.streak)
                habit_to_check.date_check.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                habit_to_check.deadline = (datetime.now() + timedelta(days=habit_to_check.period)).strftime("%Y-%m-%d")
                
                if habit_to_check.streak == habit_to_check.target:
                    habit_to_check.status = "Established"  # Broken and Active are handled in UPDATE
                    print(f"\nYou have established this habit. Congratulations!")
                else:
                    print(f"{habit_to_check.name} has been checked. The next due date is {habit_to_check.deadline}.")

    @classmethod
    def delete(cls, habits):
        """ 
        Deletes a habit from the habits list.
        
        Parameters: 
        habits (list): The list of current habits. 
        """
        if cls.check_habits_exist(habits):
            return
        
        habit_id = cls.check_id_exists(habits, occasion_name="delete")
        if habit_id is None:
            return
        
        confirmation = questionary.confirm(f"\nDo you really want to delete habit no. {habit_id}? Deleted habits cannot be restored.").ask()
        if confirmation:
            habit_to_delete = next((habit for habit in habits if habit.id == habit_id), None)
            habits.remove(habit_to_delete)
            print(f"\nHabit no. {habit_id} has been deleted.")

    @classmethod 
    def duplicate(cls, habits):
        """ 
        Duplicates an existing habit.
        
        Parameters: 
        habits (list): The list of current habits. 
        """
        if cls.check_habits_exist(habits): 
            return
         
        habit_id = cls.check_id_exists(habits, occasion_name="duplicate") 
        if habit_id is None: 
            return 
        
        habit_to_duplicate = next((habit for habit in habits if habit.id == habit_id), None) 
        if habit_to_duplicate: 
            id = cls.get_id(habits) 
            name = cls.enter_name()
            category = habit_to_duplicate.category 
            period = habit_to_duplicate.period 
            target = habit_to_duplicate.target

            new_habit = cls(id, name, category, period, target)

            habits.append(new_habit) 
            print(f"\nHabit no. {habit_id} has been duplicated. The name of the new habits is '{name}'.")

    @classmethod
    def update(cls, habits):
        """ 
        Updates the status and streaks of all habits in the list.
        Is called once, the programm is started.
        
        Parameters: 
        habits (list): The list of current habits. 
        """
        for habit in habits:
            if habit.status != "Established":  #Establishment during CHECK.
                now = datetime.now().strftime("%Y-%m-%d")

                if habit.deadline < now:
                    habit.status = "Broken"
                    habit.streak = 0 
                    if len(habit.date_interruptions) == 0 or max(habit.date_interruptions) != now:
                        habit.date_interruptions.append(datetime.now().strftime("%Y-%m-%d"))
                else:
                    habit.status = "Active"
                    habit.deadline = (datetime.now() + timedelta(days=habit.period)).strftime("%Y-%m-%d") 

    @staticmethod
    def get_id(habits):
        """ 
        Gets a new unique ID for a habit. Was added to ensure no double IDs.
        Checks the greatest existing ID and adds +1.
        
        Parameters: 
        habits (list): The list of current habits. 
        
        Returns: 
        int: A unique ID for the new habit. 

        Used by: manage.add(), manage.duplicate()
        """
        id = 1
        if habits:
            id = max(habit.id for habit in habits) + 1
        return id

    @staticmethod
    def enter_name(): 
        """ 
        Prompts the user to enter the name of the habit with max. 30 characters.
        
        Returns: 
        str: The name of the habit. 

        Used by: manage.add(), manage.duplicate() and manage.adjust()
        """
        max_length = 30
        while True: 
            name = questionary.text(f"\nPlease enter the name of your habit:").ask()
            if len(name) <= max_length: 
                return name 
            else: 
                print(f"\nName is too long! Kindly use maximum {max_length} characters.")
                print(f"'{name}' has {len(name)} characters.")

    @staticmethod
    def enter_category():
        """ 
        Prompts the user to choose one out of four categories to asign a habit. 
        
        Returns: 
        str: The selected category.

        Used by: manage.add() and manage.adjust()
        """
        category = questionary.select(
            "Which of these categories does your new habit belong to?",
            choices=CATEGORIES
        ).ask()
        return category

    @staticmethod
    def enter_period():
        """ 
        Prompts the user to choose a period for the habit repetition. 
        
        Returns: 
        int: The period mapped to its corresponding number of days.

        Used by: manage.add() and manage.adjust()
        """
        period_word = questionary.select(
            "In which period you want to repeat your new habit?",
            choices=PERIODS
        ).ask()
        period = PERIOD_MAPPING[period_word]
        return period

    @staticmethod
    def enter_valid_target():
        """ 
        Prompts the user to enter a valid target number of repetitions for the habit.
        Prevents an error caused by wrong input.
        
        Returns: 
        int: The target number of repetitions.

        Used by: manage.add() and manage.adjust()
        """
        while True:
            try:
                target = int(questionary.text(f"\nHow many times do you want to repeat that habit?").ask())
                if target > 0:
                    return target
                else:
                    print(f"\nInvalid input. Please enter a positive integer.")
            except ValueError:
                print(f"\nInvalid input. Please enter a numeric value.")

    @staticmethod
    def check_habits_exist(habits):
        """ 
        Checks if there are any habits in the list.
        Prevents the methods which use this helper method 
        from trying to work without a database, which would lead to errors.
        
        Parameters: 
        habits (list): The list of current habits. 
        
        Returns: 
        bool: True if no habits exist, False otherwise. 

        Used by: manage.adjust(), manage.check(), manage.delete(), manage.duplicate(), diaplay.display_habits() and display.filter_habits()
        """
        if not habits:
            print(f"\nNo habits found. You can add new habits by using the “ADD“ function.")
            return True
        return False

    @staticmethod
    def check_id_exists(habits, occasion_name):
        """ 
        Prompts the user to enter a valid existing ID and checks if 
        the input was correct (positiv int) and if the entered ID exists. 
        Prevents an error caused by wrong input.
        
        Parameters: 
        habits (list): The list of current habits. 
        occasion_name (str): The occasion for which the ID is being checked. 
        
        Returns: 
        int: The habit ID if it exists, None otherwise. 

        Used by: manage.adjust(), manage.check(), manage.delete() and manage.duplicate()
        """
        try:
            habit_id = int(questionary.text(f"\nPlease enter the ID of the habit you want to {occasion_name}:").ask())
        except ValueError:
            print(f"\nInvalid input. Please enter one of the numeric IDs you can see in the list above.")
            return None
        
        if not any(habit.id == habit_id for habit in habits):
            print(f"\nNo habit found with ID {habit_id}. Please enter a numeric ID you can see in the list above.")
            return None
        return habit_id