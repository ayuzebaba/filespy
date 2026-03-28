import os
from filespy.logger import get_logger

logger = get_logger(__name__)


def count_lines(filepath):
    """Count the number of lines in a file."""
    logger.debug(f"Counting lines in {filepath}")
    with open(filepath, 'r') as f:
        lines = len(f.readlines())
        logger.info(f"Found {lines} lines in {filepath}")
        return lines


def count_words(filepath):
    """Count the number of words in a file."""
    logger.debug(f"Counting words in {filepath}")
    with open(filepath, 'r') as f:
        content = f.read()
        words = len(content.split())
        logger.info(f"Found {words} words in {filepath}")
        return words


def get_file_size(filepath):
    """Get the file size in KB."""
    logger.debug(f"Getting file size for {filepath}")
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return None
    size_bytes = os.path.getsize(filepath)
    size_kb = round(size_bytes / 1024, 2)
    if size_kb < 1:
        logger.warning(f"{filepath} is very small: {size_kb} KB")
    return size_kb


def get_extension(filepath):
    """Get the file extension."""
    logger.debug(f"Getting extension for {filepath}")
    _, ext = os.path.splitext(filepath)
    return ext if ext else "no extension"