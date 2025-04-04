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


def authenticate_google_drive(credentials_path="credentials/google_drive_client_secret.json"): 

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

def save_google_drive_data(drive, credential_file="credentials/google_drive_folder_id.json", dataframe=pd.DataFrame(), filename="reddit_data_test.csv"): 
    # Grab the Folder Id of the google drive where the data will be saved
    with open(credential_file, 'r') as file:
        google_drive_credentials = json.load(file)
    folder_id = google_drive_credentials["folder_id"]
    
    # file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    # existing_file_id = None

    # for file in file_list:
    #     if file['title'] == filename:
    #         existing_file_id = file['id']
    #         break

    csv_buffer = io.StringIO()
    dataframe.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # If file exists, delete it first
    # if existing_file_id:
    #     print(existing_file_id)
    #     file_to_delete = drive.CreateFile({'id': existing_file_id})
    #     file_to_delete.Delete()
    #     print(f"Existing file '{filename}' deleted.")

    file = drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})
    file.SetContentString(csv_buffer.getvalue())  # Set content from memory buffer
    file.Upload()
    print(f"File '{filename}' uploaded successfully to folder {folder_id}!")


def grab_google_drive_folder_data(drive, credential_file = "credentials/google_drive_folder_id.json", filename="reddit_data.csv"): 
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