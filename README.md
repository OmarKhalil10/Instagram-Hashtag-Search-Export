# Instagram-Hashtag-Search-Export

## To run the scrapper script

### 1. Clone the repository

```bash
git clone https://github.com/OmarKhalil10/Instagram-Hashtag-Search-Export.git
```

### 2. Download virtualenv module
    
```bash
pip install virtualenv
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

```bash
source venv/Scripts/activate
```

### 5. Install the requirements

```bash
pip install -r requirements.txt
```

### 6. Run the app

inside `account-posts-scrapper-updated.py` file do the following:

1. Update `username_to_download = 'PUBLIC_IG_ACCOUNT_USERNAME'` with your desired public IG account username.
2. Update `start_date = datetime(2021, 1, 1)` with your desired start date.
3. Update `end_date = datetime(2023, 1, 31)` with your desired end date.
4. Update `output_csv_filename = 'downloaded_posts.csv'` with your desired output csv filename.

then run the following command:

```bash
python account-posts-scrapper-updated.py
```

### 7. Deactivate the virtual environment

```bash
deactivate
```

## To run the flask app

### 1. Activate the virtual environment

```bash
source venv/Scripts/activate
```

### 2. Run the flask app

```bash
Flask_APP=app.py 
Flask_ENV=development
FLASK_DEBUG=True
flask run --reload
```

### 3. Deactivate the virtual environment

```bash
deactivate
```
