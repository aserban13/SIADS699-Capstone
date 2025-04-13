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