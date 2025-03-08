import json
import requests
import time
from typing import List, Dict, Optional
from src.database import PGManager
import re
from collections import deque

from src.utils import (
    validate_nl_query,
    validate_sql_query,
    read_json_file,
    write_json_file,
    format_sql_query,
    log_error,
    log_info
)

total_tokens = 0

REQUEST_LIMIT = 30
TIME_WINDOW = 60
task_times = deque()

def load_input_file(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def generate_sql(data: Dict, api_key: str, schema: str) -> Dict:
    nl_query = data.get('NL', '')
    if not nl_query:
        return {'NL': nl_query, 'Query': ''}

    prompt = f"""
    Database Schema:
    {schema}

    Task: Convert the following natural language query into a valid SQL query.

    Natural Language Query:
    "{nl_query}"

    Rules:
    1. Use only the tables and columns mentioned in the schema.
    2. Ensure the SQL query is syntactically correct.
    3. Do not include any explanations or comments in the output.
    4. Add 'LIMIT 10' to the query to fetch only the first 10 rows.
    5. If the query is ambiguous, make reasonable assumptions.

    Respond ONLY with the SQL query.
    """

    response, tokens = call_groq_api(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=256
    )

    if 'choices' in response and response['choices']:
        sql_query = response['choices'][0]['message']['content'].strip()
        return {'NL': nl_query, 'Query': sql_query}
    else:
        log_error(f"API response does not contain 'choices': {response}")
        return {'NL': nl_query, 'Query': ''}

def correct_sql(data: Dict, api_key: str, schema: str) -> Dict:
    incorrect_sql = data.get('IncorrectQuery', '')
    if not incorrect_sql:
        return {'IncorrectQuery': incorrect_sql, 'CorrectQuery': ''}

    prompt = f"""
    Database Schema:
    {schema}

    Task: Fix the following SQL query to make it syntactically correct and semantically accurate.

    Incorrect SQL Query:
    {incorrect_sql}

    Rules:
    1. Ensure the query adheres to the database schema.
    2. Fix syntax errors, if any.
    3. Optimize the query for better performance.
    4. Add 'LIMIT 10' to the query to fetch only the first 10 rows.
    5. Do not include any explanations or comments in the output.

    Respond ONLY with the corrected SQL query.
    """

    response, tokens = call_groq_api(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512
    )

    if 'choices' in response and response['choices']:
        corrected_sql = response['choices'][0]['message']['content'].strip()
        return {'IncorrectQuery': incorrect_sql, 'CorrectQuery': corrected_sql}
    else:
        log_error(f"API response does not contain 'choices': {response}")
        return {'IncorrectQuery': incorrect_sql, 'CorrectQuery': ''}

def call_groq_api(api_key: str, model: str, messages: List[Dict], temperature: float = 0.0, max_tokens: int = 1000, n: int = 1) -> Optional[Dict]:
    global total_tokens, task_times

    current_time = time.time()
    while task_times and current_time - task_times[0] > TIME_WINDOW:
        task_times.popleft()

    if len(task_times) >= REQUEST_LIMIT:
        wait_time = TIME_WINDOW - (current_time - task_times[0])
        log_info(f"Rate limit reached. Waiting for {wait_time:.2f} seconds.")
        time.sleep(wait_time)
        current_time = time.time()

    task_times.append(current_time)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": model,
        "messages": messages,
        'temperature': temperature,
        'max_tokens': max_tokens,
        'n': n
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if 'error' in response_json:
        error_message = response_json['error']['message']
        if response_json['error']['code'] == 'rate_limit_exceeded':
            retry_time_match = re.search(r'in (\d+\.\d+)s', error_message)
            if retry_time_match:
                retry_after = float(retry_time_match.group(1))
                log_error(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                return call_groq_api(api_key, model, messages, temperature, max_tokens, n)
            else:
                log_error(f"Unexpected rate limit error message format: {error_message}")
                return None
        else:
            log_error(f"API error: {error_message}")
            return None

    total_tokens += response_json.get('usage', {}).get('completion_tokens', 0)
    return response_json, total_tokens

def main():
    input_file_path_1 = 'data/train_generate_task.json'
    input_file_path_2 = 'data/train_query_correction_task.json'
    data_1 = load_input_file(input_file_path_1)
    data_2 = load_input_file(input_file_path_2)
    
    db = PGManager(
        dbname="adobe_hackathon",
        user="root",
        password="root",
        host="localhost"
    )
    schema = db.get_schema()

    api_key = "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"

    start = time.time()
    sql_statement = generate_sql(data_1[0], api_key, schema)
    generate_sqls_time = time.time() - start
    
    start = time.time()
    corrected_sql = correct_sql(data_2[0], api_key, schema)
    correct_sqls_time = time.time() - start
    
    with open('outputs/output_sql_generation_task.json', 'w') as f:
        json.dump([sql_statement], f)    
    
    with open('outputs/output_sql_correction_task.json', 'w') as f:
        json.dump([corrected_sql], f)
    
    return generate_sqls_time, correct_sqls_time

if __name__ == "__main__":
    generate_sqls_time, correct_sqls_time = main()
    print(f"Time taken to generate SQL: {generate_sqls_time} seconds")
    print(f"Time taken to correct SQL: {correct_sqls_time} seconds")
    print(f"Total tokens: {total_tokens}")
