## Reddit API 

To grab the data from reddit, follow the steps below 

1. Create a script app on reddit: ```https://www.reddit.com/prefs/apps```
2. Create a reddit_credentials.json file within the notebooks/credentials directory
3. Input the following with completed informatioon into that json file 
    ```json
    {
        "REDDIT_USERNAME": "", 
        "REDDIT_PASSWORD": "", 
        "APP_ID": "", 
        "APP_SECRET": "" ,
        "APP_NAME": ""
    }
    ```

**Final file loocation:** 
notebooks/credentials/reddit_credentials.json

For more informatioon about the reddit PRAW API, these are the documenation for it: https://praw.readthedocs.io/en/stable/getting_started/quick_start.html