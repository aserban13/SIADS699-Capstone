# Chat GPT API

We leveraged the chat gpt api as one of the methoods of classifying leads  as either negative, possible, or neutral. 

# Steps to get set up 

This will help get you set up with teh chat gpt API so that you can run the notebooks. 

## API Credentials 


1. Go to [https://platform.openai.com](https://platform.openai.com) and log in or create an account.
2. Once logged in, click on your profile icon in the top-right corner and go to **API Keys**.
3. Click **+ Create new secret key** and give your key a name (e.g., `lead-classifier`).
4. Copy and securely store your API key in this location `notebooks/credentials/openai_credentials.json`. Input the data in the following format: 
```json
{
    "OPENAI_API_KEY" :  INSERT_API_KEY
}
```

**Note:** To leverage the API, you might need to obtain credits to the account- this can be done by doing the following: Go to the [Billing Overview page](https://platform.openai.com/account/billing/overview), then click **"Add payment method"** or **"Add funds"**. 

**Final file loocation:** 
`notebooks/credentials/openai_credentials.json`


## Installing OpenAI Python SDK

This `openai` library is needed to connect to chat gpt. Verson leveraged in the notebooks is already in the `requirements.txt` file. 