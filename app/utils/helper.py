from app.models import db
from nltk.tokenize import word_tokenize
from datetime import datetime
import math
from dateutil.relativedelta import relativedelta
from sqlalchemy import func

def get_next_id(table, prefix):
    last_entry = db.session.query(table).order_by(table.id.desc()).first()
    if last_entry:
        last_id = last_entry.id.replace(prefix, '')
        if last_id.isdigit():
            new_id = f"{prefix}{int(last_id) + 1:03d}"
        else:
            new_id = f"{prefix}001"
    else:
        new_id = f"{prefix}001"
    return new_id


def get_next_id_secondary_function(table, prefix):
    # Fetch the current maximum ID, strip the prefix and convert to an integer
    max_id = db.session.query(table.authentication_id).order_by(table.authentication_id.desc()).first()
    next_id_num = 1
    if max_id:
        # Extract the numeric part of the ID
        current_num = int(max_id[0][len(prefix):])
        next_id_num = current_num + 1
    # Format the new ID
    return f"{prefix}{str(next_id_num).zfill(3)}"

def replace_none(text):
    words = word_tokenize(text.lower())
    replaced_words = ['none' if word in ['none','-',"no","nill","nan","na"] else word for word in words]
    return ' '.join(replaced_words)

def is_nan(value):
    return isinstance(value,float) and math.isnan(value)

def convert_to_date(date_strings):
    date_objects = []
    for date in date_strings:
        if is_nan(date):
            date_objects.append(None)
        else:
            date_objects.append(datetime.strptime(date, '%Y-%m-%d').date())
    return date_objects

def is_donor_active(last_donated_dates):
    donor_blood_status = []
    current_date = datetime.now().date()
    for last_donated_date in last_donated_dates:
        if last_donated_date is None:
            donor_blood_status.append(1)
        elif current_date >= last_donated_date + relativedelta(months=3):
            donor_blood_status.append(1)
        else:
            donor_blood_status.append(0)
    return donor_blood_status

        
    