import json
import logging
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def validate_nl_query(nl_query: str) -> bool:
    """
    Validate a natural language query.
    :param nl_query: The natural language query to validate.
    :return: True if valid, False otherwise.
    """
    if not isinstance(nl_query, str) or len(nl_query.strip()) == 0:
        logger.warning("Invalid natural language query: Query is empty or not a string.")
        return False
    return True

def validate_sql_query(sql_query: str) -> bool:
    """
    Validate a SQL query.
    :param sql_query: The SQL query to validate.
    :return: True if valid, False otherwise.
    """
    if not isinstance(sql_query, str) or len(sql_query.strip()) == 0:
        logger.warning("Invalid SQL query: Query is empty or not a string.")
        return False
    # Add more validation rules if needed (e.g., check for SQL keywords)
    return True

def read_json_file(file_path: str) -> Optional[List[Dict]]:
    """
    Read a JSON file and return its content as a list of dictionaries.
    :param file_path: Path to the JSON file.
    :return: List of dictionaries or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Failed to read JSON file: {e}")
        return None

def write_json_file(file_path: str, data: List[Dict]) -> bool:
    """
    Write a list of dictionaries to a JSON file.
    :param file_path: Path to the JSON file.
    :param data: List of dictionaries to write.
    :return: True if successful, False otherwise.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        logger.error(f"Failed to write JSON file: {e}")
        return False

def format_sql_query(sql_query: str) -> str:
    """
    Format a SQL query for better readability.
    :param sql_query: The SQL query to format.
    :return: Formatted SQL query.
    """
    # Add basic formatting (e.g., uppercase keywords, newlines)
    keywords = ["SELECT", "FROM", "WHERE", "JOIN", "GROUP BY", "ORDER BY", "LIMIT", "OFFSET"]
    for keyword in keywords:
        sql_query = sql_query.replace(keyword, f"\n{keyword}")
    return sql_query.strip()

def log_error(error: str) -> None:
    """
    Log an error message.
    :param error: The error message to log.
    """
    logger.error(error)

def log_info(info: str) -> None:
    """
    Log an informational message.
    :param info: The message to log.
    """
    logger.info(info)