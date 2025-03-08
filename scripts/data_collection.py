from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd 
import praw
import json 
import io

# Grab these credentials from: https://www.reddit.com/prefs/apps
# Function to load credentials from a JSON file
def load_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = json.load(file)

    # Assigning the credentials to variables
    REDDIT_USERNAME = credentials['REDDIT_USERNAME']
    REDDIT_PASSWORD = credentials['REDDIT_PASSWORD']
    APP_ID = credentials['APP_ID']
    APP_SECRET = credentials['APP_SECRET']
    APP_NAME = credentials['APP_NAME']

    # Generate your reddit instance
    reddit = praw.Reddit(
        client_id=APP_ID,
        client_secret=APP_SECRET,
        user_agent=APP_NAME,
        username=REDDIT_USERNAME, 
        password=REDDIT_PASSWORD,
        check_for_async=False # This additional parameter supresses a warning about "Asynchronous PRAW"
    )
    if reddit.user.me() is None: 
        print(f"There is an issue setting the Reddit credentionals.")
    else: 
        print(f"Logged into Reddit successfully")
        return reddit 


def create_submission_df(reddit, subredit_topic="FirstTimeHomeBuyer", n_posts=5, search_query='Rocket', include_edit = False): 
    
    """
    This function accesses a subreddit page and searches it for a given phrase. It then accesses the top-n posts, and stores the post as a record in a dataframe.

    args:
    subredit_topic (str): The name of the subreddit we want to access (ie r/subredit_topic).
    n_posts (int): The number of posts we want get from that subreddit
    search_query (str): The phrase we want to use to extract posts.
    include_edit (boolean): FALSE will not filter the post. TRUE will remove all text after the phrase "EDIT: "
    
    returns Pandas DataFrame with the text of 
    """
    subreddit = reddit.subreddit(subredit_topic)
    submissions = subreddit.search(search_query, limit=n_posts)

    # submissions = subreddit.hot(limit=n_posts)
    data = {
        'submission_id': [],
        'subredit_topic': [],
        'search_query': [],
        'title': [],
        'text': [],
        'score': [],
        'num_comments': [],
        'username': [],
        'created_at': [],
        # Added 
        # 'comment_dict': []
    }
    for submission in submissions:
        data['submission_id'].append(submission.id)
        data['subredit_topic'].append(subredit_topic)
        data['search_query'].append(search_query)
        data['title'].append(submission.title)
        data['text'].append(submission.selftext)
        data['score'].append(submission.score)
        data['num_comments'].append(submission.num_comments)
        data['username'].append(submission.author.name if submission.author else 'Deleted')
        data['created_at'].append(submission.created_utc)

        # added to get a dict of comments saved as a column
        # comment_dict = {}
        # for i, comment in enumerate(submission.comments):
        
        #     try:
        #         comment_i = comment.body
        #         comment_dict[i] = comment_i
        #     except:
        #         pass

        # data['comment_dict'].append(comment_dict)

    # Create the dataframe from our dictionary
    submission_df = pd.DataFrame(data)
    submission_df['created_at'] = pd.to_datetime(submission_df['created_at'], unit='s') 
    
    # Remove \n\n using str.replace()
    # submission_df['text'] = submission_df['text'].str.replace(r'\n\n', '', regex=True)

    # Remove part of the text that gets edited if include_edit == True
    # if include_edit == True:
    #     submission_df['text'] = submission_df['text'].str.replace(r'(?i)edit: .*', '', regex=True)

    # Specify search term at end of dataset creation
    submission_df['search_query'] = search_query
    
    return submission_df


# Code to hit mulitple subreddit and companies
def combine_subreddits(reddit, n_posts, brand_subreddits_dict):

    """
    This function combines data from multiple sub-reddits and search terms to create one large dataframe for analysis. 

    args:
    n_posts (int): The number of posts that we want to access for each subreddit / search combination
    sub_reddits (list): A list of sub reddits we want to access
    search_terms (list): A list of terms we want to search on each subreddit (usually the name of a company). 

    returns:
    a pandas DataFrame with all the data about the posts in one big dataframe.
    """
    

    dfs = []
    for company, sub_reddits in brand_subreddits_dict.items():
        for sr in sub_reddits: 
            sr_data = create_submission_df(reddit, subredit_topic = sr, n_posts = n_posts, search_query = company)
            size_df = sr_data.shape[0]
            sr_data = dfs.append(sr_data)
            print(f"Done pulling {sr} subreddit for search term {company}! Size: {size_df}")
        
    # Union all dataframes together
    df_final = pd.concat(dfs)
    print('====DONE!====')
    print(df_final.shape)

    return df_final

# Extract comments as a df
def posts_to_comments(data):

    """
    The goal of this data is to extract the comments from a post. In our last function combine_subreddits() we created a columns
    saved as a dictioanry of comments.

    This function takes that dataset as input, and converts it into a df comprised of commments. We will have 1 row for each commment in this new df.

    args:
    data (Pandas DataFrame): A dataset of reddit posts. The output of combine_subreddits()

    returns:
    a Pandas DataFrame of comments. 

    """

    dfs_list = []
    for index, row in data.iterrows():
        df_i = pd.DataFrame([row['comment_dict']]).T.reset_index()
        df_i = df_i.rename({'index':'comment_index', 0: 'comment_text'}, axis = 1)
        df_i['post_id'] = row['submission_id']
        df_i['sub_reddit'] = row['subredit_topic']
        df_i['post_time'] = row['created_at']
        df_i['post_comment_count'] = row['num_comments']
        df_i['poster_username'] = row['username']
    
        dfs_list.append(df_i)
    
    comment_df = pd.concat(dfs_list)
    
    # Remove \n\n using str.replace()
    comment_df['comment_text'] = comment_df['comment_text'].str.replace(r'\n\n', '', regex=True)
    comment_df['comment_text'] = comment_df['comment_text'].str.replace(r'\*. \n\*', '', regex=True)

    # join comments to original posts datset to get some more info 
    comments_combined = pd.merge(left = comment_df,
                                right = data,
                                how = 'left',
                                left_on = 'post_id',
                                right_on = 'submission_id'
                                )

    comments_combined = comments_combined[['comment_index', 'comment_text', 'post_id', 'sub_reddit', 'post_time', 'post_comment_count',
                                        'poster_username', 'subredit_topic', 'search_query', 'title']]

    return comments_combined


def authenticate_google_drive(credentials_path="credentials/client_secrets.json"): 

    # Authenticate with Google
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(credentials_path)

    # gauth.LocalWebserverAuth()  # Opens a browser for authentication
    
    # Try to authenticate using a saved token file
    gauth.LoadCredentialsFile("google_drive_authentication_cookie.txt")

    if gauth.credentials is None:  
        gauth.LocalWebserverAuth()  # Fall back to manual login (if necessary)
    elif gauth.access_token_expired:  
        gauth.Refresh()  # Refresh the token
    else:  
        gauth.Authorize()  # Authenticate silently

    # Save the credentials for future use (so no browser is needed next time)
    gauth.SaveCredentialsFile("google_drive_authentication_cookie.txt")

    # Create GoogleDrive instance
    drive = GoogleDrive(gauth)
    return drive 

def save_google_drive_data(drive, credential_file="credentials/google_drive_credentials.json", dataframe=pd.DataFrame(), filename="reddit_data_test.csv"): 
    # Grab the Folder Id of the google drive where the data will be saved
    with open(credential_file, 'r') as file:
        google_drive_credentials = json.load(file)
    folder_id = google_drive_credentials["folder_id"]
    
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    existing_file_id = None

    for file in file_list:
        if file['title'] == filename:
            existing_file_id = file['id']
            break

    csv_buffer = io.StringIO()
    dataframe.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # If file exists, delete it first
    if existing_file_id:
        file_to_delete = drive.CreateFile({'id': existing_file_id})
        file_to_delete.Delete()
        print(f"Existing file '{filename}' deleted.")

    file = drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})
    file.SetContentString(csv_buffer.getvalue())  # Set content from memory buffer
    file.Upload()
    print(f"File '{filename}' uploaded successfully to folder {folder_id}!")


def grab_google_drive_folder_data(drive, credential_file = "credentials/google_drive_credentials.json", filename="reddit_data.csv"): 
    # Grab the Folder Id of the google drive where the data will be saved
    with open(credential_file, 'r') as file:
        google_drive_credentials = json.load(file)
    folder_id = google_drive_credentials["folder_id"]

    # Search for the file in the folder
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

    # Find the specific file by name
    file_id = None
    for file in file_list:
        if file['title'] == filename:
            file_id = file['id']
            break

    if file_id:
        # Download file content into memory
        file = drive.CreateFile({'id': file_id})
        file_content = io.StringIO(file.GetContentString())

        # Load into a Pandas DataFrame
        df = pd.read_csv(file_content)

        print(f"Successfully loaded '{filename}' into a DataFrame!")
        # print(df.head())  # Print first few rows
        return df
    else:
        print(f"File '{filename}' not found in folder {folder_id}.")