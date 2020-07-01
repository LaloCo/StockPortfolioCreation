# Setup

## For the Financial Modeling Prep Service
1. Create an account over at [financialmodelingprep.com](https://financialmodelingprep.com/) (you will receive an API key)
2. Create a new keys.py file in the root directory
3. create an `financialmodelingprep_api_key` variable in the new file and assign it to your API key as a string

## For Firebase
1. Create a new project in the firebase console
2. Get the Web API Key from the project settings
3. Assign that key to a new `firebase_api_key` variable in the same keys.py file as above
4. Enable authentication in the firebase project and create a new user
5. Paste the UID from the user into a new `user_id` in the keys file
6. Generate new Private Key from the Service accounts (under firebase project settings)
7. Add the JSON file that gets generated with the name 'serviceAccountKey.json'
