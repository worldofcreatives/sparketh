from app import db
import isodate

# -------------HELPER FUNCTIONS----------------

# Utility function to convert ISO 8601 duration to timedelta
def parse_duration(duration):
    try:
        return isodate.parse_duration(duration)
    except isodate.ISO8601Error:
        return None

# Award points
def award_points(student, points):
    student.points += points
    db.session.commit()
