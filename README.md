# Adobe Emerge Project

This project is built for the Adobe Emerge Hackathon and focuses on generating and correcting SQL queries based on natural language input using the Groq API.

## Features

- **SQL Generation**: Converts natural language inputs into SQL queries.
- **SQL Correction**: Fixes incorrect SQL queries to ensure syntactic and semantic correctness.
- **Rate Limiting**: Handles API request limits efficiently.

## Requirements

- Python 3.7+
- `requests` library
- PostgreSQL

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure the Database**
   Update the PostgreSQL database configuration in `main.py`:
    ```python
    db = PGManager(
        dbname="adobe_hackathon",
        user="root",
        password="root",
        host="localhost"
    )
    ```

4. **Set Up API Key**
   Replace `your_api_key_here` with your actual Groq API key in `main.py`:
    ```python
    api_key = "your_api_key_here"
    ```

## Usage

1. **Load Input Data**
    ```python
    input_file_path_1 = 'data/train_generate_task.json'
    input_file_path_2 = 'data/train_query_correction_task.json'
    data_1 = load_input_file(input_file_path_1)
    data_2 = load_input_file(input_file_path_2)
    ```

2. **Generate SQL Statements**
    ```python
    sql_statement = generate_sql(data_1[0], api_key, schema)
    ```

3. **Correct SQL Statements**
    ```python
    corrected_sql = correct_sql(data_2[0], api_key, schema)
    ```

4. **Save Output Results**
    ```python
    with open('outputs/output_sql_generation_task.json', 'w') as f:
        json.dump([sql_statement], f)    
    
    with open('outputs/output_sql_correction_task.json', 'w') as f:
        json.dump([corrected_sql], f)
    ```

5. **Run the Application**
    ```bash
    python main.py
    ```

## Folder Structure
```
YOUR_REPOSITORY_NAME/
├── data/
│   ├── train_generate_task.json
│   ├── train_query_correction_task.json
├── outputs/
│   ├── output_sql_generation_task.json
│   ├── output_sql_correction_task.json
├── src/
│   ├── database.py
│   ├── utils.py
├── main.py
├── requirements.txt
├── README.md
```

## License

This project is licensed under the MIT License.
