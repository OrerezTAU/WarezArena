import datetime
from urllib.parse import urlparse
import praw
import pandas as pd
import re
from cracken.models import Game, Store, WarezGroup
from prettytable import from_db_cursor
import mysql.connector
from mysql.connector import Error
import redditcleaner


# -----------------  Auxiliary functions -------------------

def create_db_connection():
    """
    Creates a connection to the database.
    @return: a connection to the database
    @rtype: mysql.connector.connection.MySQLConnection
    @raise Error: if the connection to the database fails
    """
    con_db = {
        'host': 'localhost',
        'database': 'crackedgamesDB',
        'user': 'root',
        'password': '82736455oe'
    }
    try:
        db = mysql.connector.connect(**con_db)
    except Error as error:
        raise error
    return db


def create_validate_vars(dataframe):
    """
    Creates lists of the data to be added to the database, and validates the data.
    @param dataframe: the dataframe containing the data to be added to the database
    @type dataframe: pandas.DataFrame
    @return: a tuple containing the data to be added to the database
    @rtype: tuple
    """

    store_names = dataframe['Store'].str.split(', ').explode().unique()
    store_links = dataframe['Store Link'].str.split(', ').explode().unique()
    group_names = dataframe['Group'].explode().unique()
    game_names = dataframe['Game'].explode()
    game_links = dataframe['Game Link'].explode()

    game_reviews, game_scores = process_score_reviews_cols(dataframe)
    curr_store_names = Store.objects.values_list('name', flat=True)
    curr_group_names = WarezGroup.objects.values_list('name', flat=True)

    # check if the store, group names already exist in the database
    store_names = [name for name in store_names if name not in curr_store_names]
    group_names = [name for name in group_names if name not in curr_group_names]
    return game_links, game_names, group_names, store_links, store_names, game_scores, game_reviews


def process_score_reviews_cols(dataframe):
    """
    Processes the Score (Reviews) column of the dataframe.
    In general, separates the scores and reviews into two lists.
    Then, makes sure that the scores are in the correct format to be added to the database.
    @param dataframe: the dataframe containing the data to be added to the database
    @type dataframe: pandas.DataFrame
    @return: a tuple containing the scores and reviews
    @rtype: tuple
    """
    game_scores_reviews = dataframe['Score (Reviews)'].explode()
    game_scores = [score.split('% ')[0] for score in game_scores_reviews]
    game_reviews = [review.split(' ')[1] for review in game_scores_reviews if len(review.split(' ')) > 1]
    for i in range(len(game_scores)):
        if game_scores[i] == '-':
            game_scores[i] = '-1'
            game_reviews.insert(i, '-1')  # replace '-' with -1
        else:
            game_reviews[i] = game_reviews[i][1:-1]  # remove parentheses
            if game_reviews[i].find('k') != -1:

                game_reviews[i] = str(int(float(game_reviews[i][:-1]) * 1000))  # convert k to 1000

    return game_reviews, game_scores


def handle_many_to_x(dataframe):
    """
    Handles the many-to-many and many-to-one relationships between the models.
    Adds the available stores to each game, the games cracked to each store, and the games cracked
    by each WarezGroup to the group.
    @param dataframe: the dataframe containing the data to be added to the database
    @type dataframe: pandas.DataFrame
    """
    for index, row in dataframe.iterrows():

        # Access values of individual columns using column names
        store_list_str = row['Store'].split(', ')
        store_list_df = [Store.objects.get(name=store) for store in store_list_str]
        group_name_df = row['Group']
        group = WarezGroup.objects.get(name=group_name_df)
        game_name_df = row['Game']
        game = Game.objects.get(name=game_name_df)

        game.available_on_stores.add(*store_list_df)  # add stores to game

        for store in store_list_df:
            store.games.add(game)  # add game to stores

        group.games_cracked.add(game)  # add game to group


# -----------------  Data extraction functions -------------------


def find_reddit_thread():
    """
    Finds the reddit thread containing the daily releases table.
    @return: the reddit thread (submission) containing the daily releases table
    @rtype: praw.models.Submission
    @raise Exception: if the subreddit is not found or if no threads are found this week
    """
    reddit = praw.Reddit(
        client_id="dk3990BeRf2SHUD8omrOJQ",
        client_secret="Qf0oesji7FZOtSDxIYw8hErqogBH5Q",
        user_agent="crackwatch scraper bot 1.0 by /u/Th3-3rr0r",
    )

    subreddit = reddit.subreddit("CrackWatch")  # subreddit to scrape

    if not subreddit:
        raise Exception("Subreddit not found")

    search_results = subreddit.search('Daily Releases', time_filter='week',
                                      sort='new')  # search for the daily releases thread
    if not search_results:
        raise Exception("No threads found this week")

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
            cells[0] = redditcleaner.clean(game_name_str)
            cells[1] = redditcleaner.clean(cells[1])  # make sure to clean the text before adding it to the database
            cells[2] = ', '.join(store_names_tuple)
            cells[3] = redditcleaner.clean(cells[3])  # make sure to clean the text before adding it to the database
            cells.append(game_link_str)
            store_links_tuple = [urlparse(link).netloc for link in store_links_tuple]
            cells.append(', '.join(store_links_tuple))
            data_rows.append(cells)

    return column_names, data_rows


def extract_date(submission):
    """
    Extracts the date from the thread title.
    @param submission: the reddit thread containing the daily releases table.
    @type submission: praw.models.Submission
    @return: the date of the thread in datetime format as a datetime object and as a string
    @rtype: tuple of datetime.datetime and str
    """
    thread_title = submission.title
    date_list = thread_title.split(' ')
    date_list[2] = date_list[2][1:]  # remove the parentheses from the month
    date_list[3] = date_list[3][:-1]  # remove the comma from the day
    date_list[4] = date_list[4][:-1]  # remove the parentheses from the year
    parameter = date_list[2]  # the month
    match parameter:

        case "January":
            date_list[2] = '01'
        case "February":
            date_list[2] = '02'
        case "March":
            date_list[2] = '03'
        case "April":
            date_list[2] = '04'
        case "May":
            date_list[2] = '05'
        case "June":
            date_list[2] = '06'
        case "July":
            date_list[2] = '07'
        case "August":
            date_list[2] = '08'
        case "September":
            date_list[2] = '09'
        case "October":
            date_list[2] = '10'
        case "November":
            date_list[2] = '11'
        case "December":
            date_list[2] = '12'
        case _:
            raise Exception("Invalid month")
    parameter = date_list[3]  # the day
    match parameter:

        case "1":
            date_list[3] = '01'
        case "2":
            date_list[3] = '02'
        case "3":
            date_list[3] = '03'
        case "4":
            date_list[3] = '04'
        case "5":
            date_list[3] = '05'
        case "6":
            date_list[3] = '06'
        case "7":
            date_list[3] = '07'
        case "8":
            date_list[3] = '08'
        case "9":
            date_list[3] = '09'
        case _:
            pass
    formatted_time = date_list[4] + '-' + date_list[2] + '-' + date_list[3]  # format the date as YYYY-MM-DD
    date_object = datetime.datetime.strptime(formatted_time, '%Y-%m-%d').date()
    return date_object, formatted_time


def extract_table_from_thread():
    """
    Extracts the table and thread's creation date from the submission's selftext.
    @return: a pandas dataframe containing the table data and a string containing the thread's creation date
    @rtype: tuple(pandas.DataFrame, str)
    """

    submission = find_reddit_thread()  # find the daily releases thread

    date_object, formatted_time = extract_date(submission)

    # Check if the thread has already been processed
    if Game.objects.filter(crack_date=date_object).exists():
        return None, datetime.datetime.fromisocalendar(2001, 1, 1).strftime('%Y-%m-%d')

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
            return df, formatted_time
        else:
            print("No table found in the submission.")
    else:
        print("No table-like structure found in the submission.")
    print("---")


# -----------------  Database functions -------------------


def update_database(dataframe, date):
    """
    Updates the database with the data from the dataframe.
    @param dataframe: a pandas dataframe containing the table data
    @type dataframe: pandas.DataFrame
    @param date: a string containing the thread's creation date
    @type date: str
    """
    # get unique store, game and group fields values
    (game_links, game_names, group_names, store_links, store_names,
     game_scores, game_reviews) = create_validate_vars(dataframe)

    data_store = [
        Store(
            name=store_names[row],
            url=store_links[row]
        )
        for row in range(len(store_names))
    ]
    Store.objects.bulk_create(data_store)  # bulk create stores
    # or update them if they already exist

    data_group = [
        WarezGroup(
            name=group_names[row]
        )
        for row in range(len(group_names))
    ]
    WarezGroup.objects.bulk_create(data_group)  # bulk create groups
    # or update them if they already exist

    data_game = [
        Game(
            cracking_group=WarezGroup.objects.get(name=dataframe['Group'].explode()[row]),
            name=game_names[row],
            nfo_link=game_links[row],
            crack_date=date,
            score=game_scores[row],
            num_reviews=game_reviews[row]
        )
        for row in range(len(game_names))
    ]
    Game.objects.bulk_create(data_game)  # bulk create games

    handle_many_to_x(dataframe)  # handle many-to-many and many-to-one relationships


# -----------------  HTML functions -------------------

def create_html_table():
    """
    Creates a prettyTable from the database and writes it to a file.
    """
    # Create a connection to the database
    db = create_db_connection()
    if db is None:
        return
    # Initiate cursor
    cursor = db.cursor()
    # Execute SQL query
    cursor.execute("SELECT name,cracking_group_id,score,num_reviews,nfo_link,crack_date FROM cracken_game")
    # Convert "gameRecords" table to a prettyTable
    my_table = from_db_cursor(cursor)
    my_table.field_names = ["Game Name", "Cracking Group", "Score(%)", "Reviews", "NFO Link", "Date Cracked"]
    # Generate the HTML code of the prettyTable using "get_html_string"
    html_code = my_table.get_html_string(attributes={"class": "table"},
                                         format=True, sortby="Date Cracked", reversesort=True)
    # Open prettyTable.html file
    fo = open("cracken/templates/index.html", "w")
    # Write "htmlCode" to index.html
    fo.write(html_code)
    # Close prettyTable.html
    fo.close()
    return
