# MADS Capstone Project: Reddit Sentiment Analysis

### Authors: 
##### Andreea Serban and Chris McAllister

This repository contains the codebase for our University of Michigan School of Information Capstone project. The goal of this project is to analyze Reddit data to understand brand sentiment across multiple companies by leveraging some data science methods. 

## Project Overview

We built a notebook pipeline to:
- Collect and preprocess Reddit posts
- Manually label posts
- Tested methods: Semantic Text Embeddings (STS) , created XGBoost models , Chat GPT AI 
- Evaluation 
- Analysis

## Repository Structure

```bash
SIADS699-Capstone/
│
├── credentials_setup/      # Processed and raw data (not tracked by git)
├── notebooks/              # Notebooks used to run the images in report
├── scripts/                # Python scripts for accessing the data 
├── images/                 # Images that were created or used 
├── requirements.txt        # Python dependencies
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Tools Used

- **Reddit API (PRAW)** – [PRAW License](https://github.com/praw-dev/praw/blob/main/LICENSE.txt)
- **Hugging Face Transformers** – [Apache 2.0 License](https://github.com/huggingface/transformers/blob/main/LICENSE)
- **OpenAI GPT (ChatGPT API)** – Usage governed by [OpenAI Terms of Use](https://openai.com/policies/terms-of-use)

This project uses these tools via their respective APIs and libraries, without redistributing or modifying proprietary models.

## Data Access

This project uses publicly available data collected from Reddit via the [PRAW API](https://praw.readthedocs.io/). All data access complies with Reddit's [API Terms of Service](https://www.redditinc.com/policies/data-api-terms) and [User Agreement](https://www.redditinc.com/policies/user-agreement).

- **Data Ownership**: Reddit content is owned by the users who create it and hosted by Reddit Inc.
- **Redistribution**: We do not redistribute raw data in this repository. If you wish to access the data, you must obtain your own API credentials and follow the data collection steps outlined in the [credentials_setup/0_reddit_api_instructions](credentials_setup/0_reddit_api_instructions).md.
- **Licensing**: This project does not claim any ownership over the Reddit data used. Use of the data is subject to Reddit’s policies and the rights of individual users.

For academic or reproducibility purposes, metadata and processed output summaries (e.g., sentiment scores, visualizations) may be shared upon request, in accordance with Reddit’s content usage policies.