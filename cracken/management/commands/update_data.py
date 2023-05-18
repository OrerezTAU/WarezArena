import praw
import pandas as pd

reddit = praw.Reddit(
    client_id="dk3990BeRf2SHUD8omrOJQ",
    client_secret="Qf0oesji7FZOtSDxIYw8hErqogBH5Q",
    user_agent="crackwatch scraper bot 1.0 by /u/Th3-3rr0r",
)

subreddit = reddit.subreddit("CrackWatch")  # subreddit to scrape

search_results = subreddit.search('Daily Releases', time_filter='day',
                                  sort='new')  # search for the daily releases thread

thread = next(search_results)  # get the first result (today's thread)


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
    data_rows = []

    for row in rows[2:]:  # skip the column names row and the text directions row
        cells = [cell.strip() for cell in row.split('|') if cell.strip()]
        if len(cells) == len(column_names):
            data_rows.append(cells)

    return column_names, data_rows


def extract_table_from_thread(submission):
    """
    Extracts the table from the submission's selftext.
    @param submission: the reddit post to extract the table from
    @type submission: praw.reddit.Submission
    @return: a pandas dataframe containing the table data
    @rtype: pandas.DataFrame
    """
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


# Check if the submission has a table-like structure
DataFrame = extract_table_from_thread(thread)
print(DataFrame)
