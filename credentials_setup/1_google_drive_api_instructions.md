# Google Drive API

We leverage the google drive API to prevent us from saving data locally, and save it in a google drive folder location 

# Steps to get set up 

This will help you get set up so that you can run the notebooks that pull, save, and download the data. 

## Google Drive API Credentials

1. Go to the Google Cloud Console.
2. Create a new project (or select an existing one).
3. Navigate to API & Services > Library.
4. Search for Google Drive API and enable it.
5. Go to API & Services > Credentials and create OAuth 2.0 credentials:
6. Select "OAuth Client ID".
    - Choose Desktop App or Web Application.
    - Download the client_secret.json file.
    - Rename to `google_drive_client_secret.json`
7. Move the file in this location in the repo: `notebooks/credentials/`

**Final file loocation:** 
`notebooks/credentials/google_drive_client_secrets.json`

## 2. Folder ID location 

1. Navigate to the Google Drive folder where the data will be saved
2. Copy the last section of the URL after the '/'- this is your folder id
3. Create a json file under notebooks/credentials/ named `google_drive_folder_id.json`
4. Input the data in the following format: 
```json
{
    "folder_id" :  INSERT_FOLDER_ID
}
```

**Final file loocation:** 
`notebooks/credentials/google_drive_folder_id.json`

## Caching Auhentication - Cookie

When running the notebook, to help reduce time to connect to google drive there is a cookie file that will be created within the directory that the notebook was run called `google_drive_authentication_cookie.txt`