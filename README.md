# MADS Capstone Project: Reddit Brand Sentiment Analysis

### Authors:
**Andreea Serban** and **Chris McAllister**

This repository contains the code for our Capstone project in the University of Michigan School of Information’s MADS program. Our goal is to analyze Reddit data to understand brand sentiment across multiple companies using a variety of data science methods.

---

## Setup 

We developed a notebook-based pipeline to:

- Collect and preprocess Reddit posts
- Manually label a subset of posts for supervised learning
- Experiment with multiple methods:
  - Semantic Textual Similarity (STS) using embeddings
  - XGBoost classification models
  - OpenAI’s ChatGPT for post classification
- Evaluate model performance
- Analyze insights across brands

### How to Run the Code

### 1. Clone the Repository

```bash
git clone https://github.com/aserban13/SIADS699-Capstone.git
cd SIADS699-Capstone
```

### 2. Set up APIs

Follow the files in the credentials_setup notebook to set up the: 
- [Reddit API](0_reddit_api_instructions.md)
- [Google Drive API](1_google_drive_api_instructions.md)
- [Chat GPT API](2_chat_gpt_api_instructions.md)

### 3. Run Notebooks and get the results

Run the notebooks within the `notebooks/` folder in order to replicate the results.   

---

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

---

##  Data Access

This project uses publicly available data collected from Reddit via the [PRAW API](https://praw.readthedocs.io/). All data access adheres to Reddit's [API Terms of Service](https://www.redditinc.com/policies/data-api-terms) and [User Agreement](https://www.redditinc.com/policies/user-agreement).

- **Data Ownership**: Reddit content is created by users and owned by Reddit Inc.
- **Redistribution**: We do not redistribute any raw Reddit data in this repository. To access the data, you must obtain your own API credentials and follow the instructions in [`credentials_setup/0_reddit_api_instructions.md`](credentials_setup/0_reddit_api_instructions.md).
- **Licensing**: This project does not claim ownership over Reddit data. Use of the data is governed by Reddit’s policies and the rights of individual users.

For academic or reproducibility purposes, we may be able to share derived metadata or aggregate outputs (e.g., sentiment scores or visualizations), in accordance with Reddit’s content usage guidelines.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Tools Used

- **Reddit API (PRAW)** – [PRAW License](https://github.com/praw-dev/praw/blob/main/LICENSE.txt)
- **Hugging Face Transformers** – [Apache 2.0 License](https://github.com/huggingface/transformers/blob/main/LICENSE)
- **OpenAI GPT (ChatGPT API)** – Governed by [OpenAI Terms of Use](https://openai.com/policies/terms-of-use)

We use these tools via their official APIs and libraries. This project does not redistribute or modify proprietary models or content.

---
