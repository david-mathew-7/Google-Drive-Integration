# Google Drive Integration Application

## Overview

This application integrates with Google Drive using OAuth 2.0 to provide a set of functionalities:
- Authenticate users with their Google account.
- List files in the user's Google Drive.
- Upload files to the user's Google Drive.
- Download files from the user's Google Drive.
- Delete files from the user's Google Drive.

The application is built using **FastAPI** for the backend and **Jinja2** for templating.

## Requirements

To run this application locally, you'll need:

- Python 3.10 or higher
- `pip` (Python package installer)
- A Google Cloud Platform project with OAuth 2.0 credentials
- pip install -r requirements.txt 


## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/david-mathew-7/Google-Drive-Integration.git



2. **How to Run**
   ```
   cd Google-drive-integration
   uvicorn app.main:app --reload

   Note: You must need to add CLIENT_SECRETS_FILE to run the Oauth2 in auth.py.
         You have to create this by using GoogleCloudPlatform.

   To Run: UnitTestCases
   pytest app/tests/test_main.py
