from datetime import datetime
import pytz


def utcMakassar():
    UTC = pytz.timezone('Asia/Makassar')
    datetime_utc = datetime.now(UTC)

    return datetime_utc