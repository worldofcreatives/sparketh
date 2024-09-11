from app import db
import isodate
import os
import re
from .banned_words import BANNED_WORDS

# Utility function to convert ISO 8601 duration to timedelta
def parse_duration(duration):
    try:
        return isodate.parse_duration(duration)
    except isodate.ISO8601Error:
        return None

# ---------------POINTS----------------

# Award points
def award_points(student, points):
    student.points += points
    db.session.commit()

# ---------------FILE UPLOADS----------------

# Check if file is allowed
def is_allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes

def file_size_under_limit(file):
    file.seek(0, os.SEEK_END)  # Go to the end of the file
    file_size = file.tell()  # Get the position of EOF
    file.seek(0)  # Reset the file position to the beginning
    return file_size <= MAX_FILE_SIZE

# ---------------INAPPROPRIATE CONTENT----------------

# Check if text contains inappropriate content
def contains_inappropriate_content(text):
    text = text.lower()
    for word in BANNED_WORDS:
        if re.search(rf"\b{word}\b", text):
            return True
    return False

