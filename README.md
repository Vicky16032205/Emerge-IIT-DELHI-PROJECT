# Adobe Emerge Project

This project is designed to generate and correct SQL queries based on natural language input using the Groq API.

## Features

- Generate SQL queries from natural language input
- Correct SQL queries to ensure they are syntactically and semantically accurate
- Rate limiting to handle API request limits

## Requirements

- Python 3.7+
- Requests library
- PostgreSQL

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your PostgreSQL database and update the database configuration in the `main.py` file:

    ```python
    db = PGManager(
        dbname="adobe_hackathon",
        user="root",
        password="root",
        host="localhost"
    )
    ```

4. Replace the Groq API key in the `main.py` file with your actual API key:

    ```python
    api_key = "your_api_key_here"
    ```

## Usage

1. Load data from input files:

    ```python
    input_file_path_1 = 'data/train_generate_task.json'
    input_file_path_2 = 'data/train_query_correction_task.json'
    data_1 = load_input_file(input_file_path_1)
    data_2 = load_input_file(input_file_path_2)
    ```

2. Generate SQL statements:

    ```python
    sql_statement = generate_sql(data_1[0], api_key, schema)
    ```

3. Correct SQL statements:

    ```python
    corrected_sql = correct_sql(data_2[0], api_key, schema)
    ```

4. Save outputs:

    ```python
    with open('outputs/output_sql_generation_task.json', 'w') as f:
        json.dump([sql_statement], f)    
    
    with open('outputs/output_sql_correction_task.json', 'w') as f:
        json.dump([corrected_sql], f)
    ```

5. Run the main function:

    ```bash
    python main.py
    ```

## License

This project is licensed under the MIT License.
