from urllib.parse import urlparse
import praw
import pandas as pd
import re
from django.db import IntegrityError
from .models import Game, Store, WarezGroup


def find_reddit_thread():
    """
    Finds the reddit thread containing the daily releases table.
    @return: the reddit thread (submission) containing the daily releases table
    @rtype: praw.models.Submission
    """
    reddit = praw.Reddit(
        client_id="dk3990BeRf2SHUD8omrOJQ",
        client_secret="Qf0oesji7FZOtSDxIYw8hErqogBH5Q",
        user_agent="crackwatch scraper bot 1.0 by /u/Th3-3rr0r",
    )

    subreddit = reddit.subreddit("CrackWatch")  # subreddit to scrape

    if not subreddit:
        raise Exception("Subreddit not found")

    search_results = subreddit.search('Daily Releases', time_filter='month',
                                      sort='new')  # search for the daily releases thread
    if not search_results:
        raise Exception("No threads found this month")

    thread = next(search_results)  # get the first result (today's thread)

    if not thread:
        raise Exception("No threads found today")

    return thread


def extract_table_contents(table_text):
    """
    Extracts the column names and data rows from the table text.
    @param table_text: A string containing the table text
    @type table_text: str
    @return: a tuple containing the column names and data rows
    @rtype: tuple
    """
    rows = table_text.strip().split('\n')
    column_names = [col.strip() for col in rows[0].split('|') if col.strip()]
    column_names.append('Game Link')
    column_names.append('Store Link')
    data_rows = []

    for row in rows[2:]:  # skip the column names row and the text directions row
        cells = [cell.strip() for cell in row.split('|') if cell.strip()]

        if len(cells) + 2 == len(column_names):
            pattern_name = r'\[(.*?)\]'  # Regular expression pattern to match expressions inside square brackets
            pattern_link = r'\((.*?)\)'  # Regular expression pattern to match expressions inside parentheses
            game_name_str = re.search(pattern_name, cells[0]).group(1)  # find the game name inside square brackets
            game_link_str = re.search(pattern_link, cells[0]).group(1)  # find the game link inside parentheses
            store_names_tuple = re.findall(pattern_name, cells[2])  # find all the stores in the cell
            store_links_tuple = re.findall(pattern_link, cells[2])  # find all the store links in the cell
            # TODO - find a scalable way to access the store and game columns (not hardcoded)
            cells[0] = game_name_str
            cells[2] = ', '.join(store_names_tuple)
            cells.append(game_link_str)
            store_links_tuple = [urlparse(link).netloc for link in store_links_tuple]
            cells.append(', '.join(store_links_tuple))
            data_rows.append(cells)

    return column_names, data_rows


def extract_table_from_thread():
    """
    Extracts the table from the submission's selftext.
    @return: a pandas dataframe containing the table data
    @rtype: pandas.DataFrame
    """

    submission = find_reddit_thread()  # find the daily releases thread

    # Set pandas options to display columns properly
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    if '|' in submission.selftext:
        # Extract the table section from selftext
        start_index = submission.selftext.find('|')
        end_index = submission.selftext.find('&nbsp;', start_index)  # the table ends with '&nbsp;' (non-breaking space)
        table_text = submission.selftext[start_index:end_index]

        column_names, data_rows = extract_table_contents(table_text)

        if column_names and data_rows:
            df = pd.DataFrame(data_rows, columns=column_names)  # create a pandas dataframe from the table data
            return df
        else:
            print("No table found in the submission.")
    else:
        print("No table-like structure found in the submission.")
    print("---")


def update_database(dataframe):
    """
    Updates the database with the data from the dataframe.
    @param dataframe: a pandas dataframe containing the table data
    @type dataframe: pandas.DataFrame
    """
    # get unique store, game and group names and links
    store_names = dataframe['Store'].str.split(', ').explode().unique()
    store_links = dataframe['Store Link'].str.split(', ').explode().unique()
    group_names = dataframe['Group'].explode().unique()
    game_names = dataframe['Game'].explode().unique()
    game_links = dataframe['Game Link'].explode().unique()

    curr_store_names = Store.objects.values_list('name', flat=True)
    curr_group_names = WarezGroup.objects.values_list('name', flat=True)

    # check if the store, group names already exist in the database
    store_names = [name for name in store_names if name not in curr_store_names]
    group_names = [name for name in group_names if name not in curr_group_names]



    data_store = [
        Store(
            name=store_names[row],
            url=store_links[row]
        )
        for row in range(len(store_names))
    ]
    Store.objects.bulk_create(data_store)  # bulk create stores

    data_group = [
        WarezGroup(
            name=group_names[row]
        )
        for row in range(len(group_names))
    ]
    WarezGroup.objects.bulk_create(data_group) # bulk create groups
    # or update them if they already exist

    data_game = [
        Game(
            cracking_group=WarezGroup.objects.get(name=dataframe['Group'].explode()[row]),
            name=game_names[row],
            nfo_link=game_links[row]
        )
        for row in range(len(game_names))
    ]
    Game.objects.bulk_create(data_game) # bulk create games
