import json

from manage import Habit 

class HabitsStore():
    """ 
    A class to handle saving and loading habits to and from a JSON file. 
    """
    DEFAULT_FILENAME = "habits.json"
    
    def save(self, habits, filename = DEFAULT_FILENAME):
        """ 
        Saves the current list of habits to a JSON file. 
        
        Parameters: 
        habits (list): A list of Habit objects to be saved. 
        filename (str): The name of the file to save the habits to. Defaults to "habits.json". 
        """
        with open(filename, 'w') as file:
            json.dump([habit.__dict__ for habit in habits], file, indent=4)

    def load(self, filename = DEFAULT_FILENAME):
        """ 
        Loads habits from a JSON file. 
        
        Parameters: 
        filename (str): The name of the file to load the habits from. Defaults to "habits.json". 
        
        Returns: 
        list: A list of Habit objects. 
        """
        try:
            with open(filename, 'r') as file:
                habits_data = json.load(file) 
                return [Habit(**habit) for habit in habits_data]
        except FileNotFoundError:
            return []