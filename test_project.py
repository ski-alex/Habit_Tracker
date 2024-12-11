from datetime import datetime, timedelta
import json
import os
import pytest
from unittest.mock import patch, MagicMock

from analyse import Analyse
from manage import Habit, period_mapping
from store import HabitsStore
from display import display_habits, filter_habits

def create_test_file(file_path):
    """ 
    Creates a test JSON file with sample habit data. 
    Parameters: 
    file_path (str): The path where the test file will be created. 
    
    The function generates sample habit data for testing purposes, including all Habit attributes.
    The generated data is written to a JSON file specified by the file_path parameter. 
    """
    now = datetime.now()
    test_data = [
        {"id": 1, "name": "Exercise", "category": "Health", "period": 1, "target": 10, "streak": 7, "streak_max": 7, 
         "date_create": (now - timedelta(days=10)).strftime("%Y-%m-%d"), 
         "date_check": [(now - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(1, 8)], 
         "deadline": (now - timedelta(days=1)).strftime("%Y-%m-%d"), "status": "Active", "date_interruptions": []},
        {"id": 2, "name": "Read Book", "category": "Education", "period": 2, "target": 5, "streak": 5, "streak_max": 5, 
         "date_create": (now - timedelta(days=15)).strftime("%Y-%m-%d"), 
         "date_check": [(now - timedelta(days=i*2)).strftime("%Y-%m-%d %H:%M:%S") for i in range(1, 6)], 
         "deadline": now.strftime("%Y-%m-%d"), "status": "Active", "date_interruptions": []},
        {"id": 3, "name": "Meditation", "category": "Wellness", "period": 7, "target": 8, "streak": 3, "streak_max": 4, 
         "date_create": (now - timedelta(days=20)).strftime("%Y-%m-%d"), 
         "date_check": [(now - timedelta(days=i*7)).strftime("%Y-%m-%d %H:%M:%S") for i in range(1, 4)], 
         "deadline": (now + timedelta(days=1)).strftime("%Y-%m-%d"), "status": "Active", "date_interruptions": []},
        {"id": 4, "name": "Cooking", "category": "Lifestyle", "period": 2, "target": 6, "streak": 2, "streak_max": 2, 
         "date_create": (now - timedelta(days=5)).strftime("%Y-%m-%d"), 
         "date_check": [(now - timedelta(days=i*2)).strftime("%Y-%m-%d %H:%M:%S") for i in range(1, 3)], 
         "deadline": (now + timedelta(days=2)).strftime("%Y-%m-%d"), "status": "Active", "date_interruptions": []},
        {"id": 5, "name": "Yoga", "category": "Fitness", "period": 1, "target": 7, "streak": 3, "streak_max": 3, 
         "date_create": (now - timedelta(days=6)).strftime("%Y-%m-%d"), 
         "date_check": [(now - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(1, 4)], 
         "deadline": (now + timedelta(days=3)).strftime("%Y-%m-%d"), "status": "Active", "date_interruptions": []}
    ] 
    with open(file_path, 'w') as file: 
        json.dump(test_data, file, indent=4)
   
@pytest.fixture
def sample_habits():
    """
    Fixture to create and load sample habits from a test JSON file.

    This fixture creates a test file with sample habit data, loads the habits using
    the HabitsStore class, yields the loaded habits for testing, and removes the
    test file after the test is completed.

    Returns:
    list: A list of Habit objects loaded from the test file.
    """
    create_test_file('test_habits.json')
    store = HabitsStore()
    habits = store.load('test_habits.json')
    yield habits
    os.remove('test_habits.json')

def test_save_habits(sample_habits, test_file_path="test_habits_save.json"):
    """
    Tests the save function by saving the current state of habits to a test file
    and verifying the saved data.

    Parameters:
    sample_habits (list): A list of Habit objects to be saved.
    test_file_path (str): The path to the test file where the habits will be saved.
                          Defaults to "test_habits_save.json".

    The function saves the habits to the specified test file, loads the saved data 
    and asserts that the loaded data matches the original sample habits. The test file will be deleted after use.
    """
    store = HabitsStore()
    store.save(sample_habits, test_file_path)
    with open(test_file_path, 'r') as file:
        loaded_data = json.load(file)
    assert len(loaded_data) == 5
    assert loaded_data[0]['name'] == "Exercise"
    assert loaded_data[1]['name'] == "Read Book"
    assert loaded_data[2]['name'] == "Meditation"
    assert loaded_data[3]['name'] == "Cooking"
    assert loaded_data[4]['name'] == "Yoga"
    os.remove('test_habits_save.json')

def test_load_habits(sample_habits):
    """
    Tests the load function by verifying the loaded sample habits.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function asserts that the loaded sample habits match the expected habit data.
    """
    assert len(sample_habits) == 5
    assert sample_habits[0].name == "Exercise"
    assert sample_habits[1].name == "Read Book"
    assert sample_habits[2].name == "Meditation"
    assert sample_habits[3].name == "Cooking"
    assert sample_habits[4].name == "Yoga"

def test_update_habit_status(sample_habits):
    """
    Tests the update function by verifying the status and streak updates of sample habits.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function asserts that the status and streak of the sample habits are correctly updated
    based on their deadlines. It verifies if the statuses are set to "Broken" or "Active" and
    if the streaks and interruptions are correctly updated.
    """
    habit1 = sample_habits[0]
    habit2 = sample_habits[1]
    habit3 = sample_habits[2]

    Habit.update(sample_habits)

    now = datetime.now().strftime("%Y-%m-%d")

    assert habit1.status == "Broken"
    assert habit1.streak == 0
    assert now in habit1.date_interruptions

    assert habit2.status == "Active"
    assert habit2.streak == 5
    assert now not in habit2.date_interruptions

    assert habit3.status == "Active"
    assert habit3.streak == 3
    assert now not in habit3.date_interruptions

@patch('questionary.text')
@patch('questionary.select')
@patch('questionary.confirm')
def test_add_habit(mock_confirm, mock_select, mock_text, sample_habits):
    """
    Tests the add function by mocking user inputs and verifying the addition of a new habit.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function simulates user inputs to add a new habit and asserts that the new habit
    is correctly added to the sample habits list with the expected attributes.
    """
    mock_text.return_value.ask.side_effect = ["New Habit Name", 5]
    mock_select.return_value.ask.side_effect = ["Health", "Daily"]
    mock_confirm.return_value.ask.return_value = True

    initial_count = len(sample_habits)
    Habit.add(sample_habits)
    
    assert len(sample_habits) == initial_count + 1
    assert sample_habits[-1].name == "New Habit Name"
    assert sample_habits[-1].category == "Health"
    assert sample_habits[-1].period == period_mapping["Daily"]
    assert sample_habits[-1].target == 5

@patch('questionary.text')
@patch('questionary.select')
@patch('questionary.confirm')
def test_adjust_habit(mock_confirm, mock_select, mock_text, sample_habits):
    """
    Tests the adjust function by mocking user inputs and verifying the adjustment of an existing habit.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function simulates user inputs to adjust an existing habit's name and asserts that
    the habit's name is correctly updated in the sample habits list.
    """
    mock_text.return_value.ask.side_effect = [str(sample_habits[0].id), "Adjusted Name"]
    mock_select.return_value.ask.side_effect = ["Name"]
    mock_confirm.return_value.ask.return_value = True

    habit_to_adjust = sample_habits[0]
    initial_name = habit_to_adjust.name

    Habit.adjust(sample_habits)

    assert habit_to_adjust.name != initial_name
    assert habit_to_adjust.name == "Adjusted Name"


@patch('questionary.confirm')
@patch('questionary.text')
def test_check_habit(mock_text, mock_confirm, sample_habits):
    """
    Tests the check function by mocking user inputs and verifying the habit check-in process.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function simulates user inputs to check a habit and asserts that the habit's streak is incremented
    and the date of the check-in is correctly recorded.
    """
    habit_to_check = sample_habits[0]
    initial_streak = habit_to_check.streak

    mock_text.return_value.ask.return_value = str(habit_to_check.id)
    mock_confirm.return_value.ask.return_value = True

    Habit.check(sample_habits)

    assert habit_to_check.streak == initial_streak + 1
    assert habit_to_check.date_check[-1].split()[0] == datetime.now().strftime("%Y-%m-%d")

def test_check_habit_already_established(sample_habits):
    """
    Tests the check function for an already established habit.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function asserts that the streak and status of an already established habit remain unchanged
    after attempting to check it again.
    """
    habit_to_check = sample_habits[0]
    habit_to_check.status = "Established"
    initial_streak = habit_to_check.streak

    with patch('questionary.confirm') as mock_confirm, patch('questionary.text') as mock_text:
        mock_text.return_value.ask.return_value = str(habit_to_check.id)
        mock_confirm.return_value.ask.return_value = True

        Habit.check(sample_habits)
    
    assert habit_to_check.streak == initial_streak
    assert habit_to_check.status == "Established"

@patch('questionary.confirm')
@patch('questionary.text')
def test_delete_habit(mock_text, mock_confirm, sample_habits):
    """
    Tests the delete function by mocking user inputs and verifying the deletion of a habit.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function simulates user inputs to delete a habit and asserts that the habit is correctly
    removed from the sample habits list.
    """
    habit_to_delete = sample_habits[0]
    initial_count = len(sample_habits)

    mock_text.return_value.ask.return_value = str(habit_to_delete.id)
    mock_confirm.return_value.ask.return_value = True

    Habit.delete(sample_habits)
    
    assert len(sample_habits) == initial_count - 1
    assert habit_to_delete not in sample_habits

@patch('questionary.text')
def test_duplicate_habit(mock_text, sample_habits):
    """
    Tests the duplicate function by mocking user inputs and verifying the duplication of a habit.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function simulates user inputs to duplicate a habit and asserts that the new habit is correctly
    added to the sample habits list with the expected attributes.
    """
    habit_to_duplicate = sample_habits[0]
    initial_count = len(sample_habits)

    mock_text.return_value.ask.side_effect = [str(habit_to_duplicate.id), "Name of Dublicate"]

    Habit.duplicate(sample_habits)
    
    assert len(sample_habits) == initial_count + 1
    assert sample_habits[-1].name == "Name of Dublicate"
    assert sample_habits[-1].category == habit_to_duplicate.category
    assert sample_habits[-1].period == habit_to_duplicate.period
    assert sample_habits[-1].target == habit_to_duplicate.target

@patch('tabulate.tabulate', return_value="Mocked Table")
@patch('questionary.select')
def test_get_top_main(mock_select, mock_tabulate, sample_habits, capsys):
    """
    Tests the get_top_main function by mocking user input and verifying the output.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.
    capsys (CaptureFixture): Pytest fixture to capture stdout and stderr output.

    The function simulates user input to select the order of habits and asserts that the
    output contains the expected text indicating the sorted list of habits by streak.
    """
    mock_select.return_value.ask.return_value = 'descending'
    Analyse.get_top_main(sample_habits, 'streak', 'streak')
    captured = capsys.readouterr()
    assert "Here is a descending list of all habits that have a streak > 0:" in captured.out

@patch('tabulate.tabulate', return_value="Mocked Table")
def test_get_top_most(mock_tabulate, sample_habits, capsys):
    """
    Tests the get_top_most function by verifying the output.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.
    capsys (CaptureFixture): Pytest fixture to capture stdout and stderr output.

    The function asserts that the output contains the expected text indicating the
    top 3 habits with the most check-ins.
    """
    Analyse.get_top_most(sample_habits, 'date_check', 'check-ins')
    captured = capsys.readouterr()
    assert "Here are the top 3 of your habits with the most check-ins since creation:" in captured.out

@patch('tabulate.tabulate', return_value="Mocked Table")
def test_get_top_longest_expired(mock_tabulate, sample_habits, capsys):
    """
    Tests the get_top_longest_expired function by verifying the output.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.
    capsys (CaptureFixture): Pytest fixture to capture stdout and stderr output.

    The function asserts that the output contains the expected text indicating the
    top 3 habits that have not been worked on for the longest time.
    """
    Analyse.get_top_longest_expired(sample_habits)
    captured = capsys.readouterr()
    assert "Here are the top 3 of your habits that have not been worked on for the longest time:" in captured.out

@patch('tabulate.tabulate', return_value="Mocked Table")
def test_get_group_habits_by_category(mock_tabulate, sample_habits, capsys):
    """
    Tests the get_group_habits_by_category function by verifying the output.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.
    capsys (CaptureFixture): Pytest fixture to capture stdout and stderr output.

    The function asserts that the output contains the expected text indicating the
    grouping of all habits by category.
    """
    Analyse.get_group_habits_by_category(sample_habits)
    captured = capsys.readouterr()
    assert "Here is a grouping of all habits by category:" in captured.out

@patch('questionary.text')
@patch('tabulate.tabulate', return_value="Mocked Table")
def test_get_habit_streak_max(mock_tabulate, mock_text, sample_habits, capsys):
    """
    Tests the get_habit_streak_max function by mocking user input and verifying the output.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.
    capsys (CaptureFixture): Pytest fixture to capture stdout and stderr output.

    The function simulates user input to select a habit and asserts that the output contains
    the expected text indicating the maximum streak for the selected habit.
    """
    mock_text.return_value.ask.return_value = "1"
    Analyse.get_habit_streak_max(sample_habits)
    captured = capsys.readouterr()
    assert "Streak Max" in captured.out

@patch('questionary.select')
def test_get_habits_by_period(mock_select, sample_habits, capsys):
    """
    Tests the get_habits_by_period function by mocking user input and verifying the output.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.
    capsys (CaptureFixture): Pytest fixture to capture stdout and stderr output.

    The function simulates user input to select a period and asserts that the output contains
    the expected text indicating the habits with the selected period.
    """
    mock_select.return_value.ask.return_value = "Daily"
    Analyse.get_habits_by_period(sample_habits)
    captured = capsys.readouterr()
    assert "Here are all habits with a period of 'Daily'." in captured.out



@patch('builtins.print')
def test_display_habits(mock_print, sample_habits):
    """
    Tests the display_habits function by verifying the displayed habits table.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function calls display_habits with specified parameters to display habits
    and asserts that the printed output contains the expected table headers and habit names.
    """
    display_habits(sample_habits, status_request="Broken", length="full", filter_period=[1, 2, 7])
    mock_print.assert_called()
    output = mock_print.call_args[0][0]
    assert "ID" in output
    assert "Exercise" in output
    assert "Read Book" in output
    assert "Meditation" in output
    assert "Cooking" in output
    assert "Yoga" in output

@patch('questionary.select')
@patch('builtins.print')
def test_filter_habits(mock_print, mock_select, sample_habits):
    """
    Tests the filter_habits function by mocking user input and verifying the filtered habits table.

    Parameters:
    sample_habits (list): A list of Habit objects loaded from the test file.

    The function simulates user input to filter habits by "id > 1" and asserts that the printed
    output contains the expected table headers and habit names, excluding the habit with id=1.
    """
    mock_select.return_value.ask.side_effect = ["id", "greater values"]
    with patch('questionary.text') as mock_text:
        mock_text.return_value.ask.return_value = "1"
        filter_habits(sample_habits)

    mock_print.assert_called()
    output = mock_print.call_args[0][0]
    assert "ID" in output
    assert "Exercise" not in output
    assert "Read Book" in output
    assert "Meditation" in output
    assert "Cooking" in output
    assert "Yoga" in output