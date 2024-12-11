# Habit Tracker 2024

With this application, you will never fail to track your habits anymore.

## What is it?

Habit Tracker is a simple and effective application designed to help you track and maintain your habits effortlessly. Whether you want to build new habits or break old ones, this tool is here to support you.

## Features

- **Track multiple habits:** Monitor and track the progress of various habits simultaneously.
- **Detailed statistics:** Visualize your progress with charts and graphs.
- **Customization:** Customize habit categories, frequencies, and reminders to suit your needs.

## Requirements 
**Python V.3.7 or later** (made with 3.11.9) and respective liarbaries. For details see "requirements.txt".

## Installation

To install the necessary dependencies, use follow these steps:

1. Save the following files in the same path / folder: `main.py`, `manage.py`, `analyse.py`, `display.py` and `store.py`.
2. Make sure that the latest version of Python is installed on your system; at least version 3.7.
3. Open a terminal or command prompt and navigate to the directory where you downloaded the files.

    To install the necessary dependencies, use the following command:

    ```shell
    pip install -r requirements.txt
    ```

## Usage
Start the application by running the main script and follow the instructions provided:
```shell
python main.py
```
**Navigation**

Navigation is exclusively via the Comand Line interface. The up and down arrow keys are mainly used for this purpose. To confirm a selection, use the enter button. If several options can be selected (indicated by the small circle in front of the options), these are first selected or deselected with the space bar and the final selection is confirmed with Enter.


**Main Menu**

Right after the start, the main menu is displayed.

- **Quick Check:** Check the status of a specific habit.
- **Add:** Add a new habit to track.
- **Manage:** Manage your existing habits with options to filter, check, delete, duplicate, or adjust them.
- **Analyse:** Analyse your habits with various metrics such as longest active streaks, most interruptions, etc.
- **Exit:** Save your progress and exit the application.

**Submenu "Manage"**
- **Filter habits:** Displays habits based on user-defined criteria.
- **Check a habit:** Check the status of a specific habit.
- **Delete a habit:** Delete a habit. 
- **Duplicate a habit:** Duplicate an existing habit.
- **Adjust a habit:** Adjust an existing habit.
- **Go back to Main Menu:** Return to the main menu.

**Submenu "Analyse"**
- **All currently tracked habits:** Display all habits that are currently tracked and not established.
- **All habits with the same periodicity:** Show all habits that have the same period.
- **Longest run streak of all defined habits:** Show the habits with the longest maximum streak ever achieved.
- **Longest run streak for a given habit:** Display the maximum streak of a specific habit selected by the user.
- **Longest active streaks:** Show the habits with the longest current streak.
- **Most interruptions since creation (Top 3):** Display the top 3 habits with the most interruptions.
- **Most checks since creation (Top 3):** Display the top 3 habits with the most checks.
- **Longest expired (Top 3):** Show the top 3 habits that have not been worked on for the longest time.
- **Group by category:** Group all habits by their categories.
- **Go back to Main Menu:** Return to the main menu.

## Examples for usage
All of the following steps have to be confirmed with "Enter".

**Check an existing habit**
1. In the main menu, navigate to **"Quick Check"** or alternatively to **"Manage habits"** and then to **"Check a habit"**.
2. Enter the **ID** of the habit you want to check.
3. If your choice was correct, **confirm with "Y" or "Enter"**. Else, reject with "N" and you can start again. 

**Add a new habit**
1. In the main menu, navigate to **Add**.
2. Enter the **name** of your new habit (max. 30 characters).
3. Navigate to a **category** to which you would like to assign the new habit.
4. Select the **period** at which you want to repeat the new habit.
5. Enter the **target** number of repetitions you want to complete without interruption in order to establish the habit.
6. You will see summary of your choices. If they are correct, **confirm with "Y" or "Enter"**. Else, reject with "N" and you can start again. 

**Filter habits**
1. In the main menu, navigate to **"Manage habits"** and then to **"Filter habits"**.
2. Choose the attribute you want to filter.
3. Depending on your choice...
    - For ID, Target, Streak, Max Streak, Created On and Deadline 
        -   choose the comparison you want to make (=,< or >)
        - Enter the value you want to compare with
    - For Name enter the character string the results should contain
    - For Category, Period and Status choose one or several characteristic you want to include into yout filter.

**Delete an existing habit**
1. In the main menu, navigate to **"Manage habits"** and then to **"Delete a habit"**.
2. Enter the **ID** of the habit you want to duplicate.
3. If your choice was correct, **confirm with "Y" or "Enter"**. Else, reject with "N" and you can start again. 

**Duplicate an existing habit**
1. In the main menu, navigate to **"Manage habits"** and then to **"Duplicate a habit"**.
2. Enter the **ID** of the habit you want to duplicate.
3. Enter the **name** of the new habit.

**Adjust an existing habit**
1. In the main menu, navigate to **"Manage habits"** and then to **"Adjust a habit"**.
2. Enter the **ID** of the habit you want to adjust.
3. Choose the attribute you want to adjust.
4. Depending on the attribute **enter or choose the new value**.

**Filter**

In the main menu, navigate to **"Analyse habits"** and choose the analysis you want to see.
- For **All habits with the same periodicity** choose the periodicity you want to see.
- For **Longest run streak of all defined habits** choose if you want to see an descending or ascending order. 
- For **Longest run streak for a given habit** and **Longest active streaks**  enter the ID of the habit you want to see.
- For **All currently tracked habits, Most interruptions since creation (Top 3), Most checks since creation (Top 3), Longest expired (Top 3)** and **Group by category** No more action is needed.

## Tests
To run tests, `pytest` must be installed. If it is not installed, it can be done by using:
```shell
pytest .
```

## Code Structure
- **`main.py`** Contains the main logic of the application including the command-line interface.
- **`manage.py`** Contains the Habit class and associated methods for habit management.
- **`display.py`** Functions to display and filter habits using tabulate.
- **`analyse.py`** Functions to analyze habits and provide detailed statistics.
- **`store.py`** Functions to load and save habits data.
- **`test.py`** Tests all key functions of the Habit Tracker.

## Current Version
10/12/2024

*All bugs found can be kept for free and will be fixed with the Season Pass.*