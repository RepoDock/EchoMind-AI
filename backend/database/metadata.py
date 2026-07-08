from database.crud import get_file_hash
from utils.hashing import calculate_hash


def should_index(file):

    current_hash = calculate_hash(file["path"])

    saved_hash = get_file_hash(file["path"])

    if saved_hash is None:
        return True

    return current_hash != saved_hash