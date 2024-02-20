# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    reformatted_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        reformatted_dates.append(date_obj.strftime('%d %b %Y'))
    return reformatted_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError
    if not isinstance(n, int):
        raise TypeError
    start_date = datetime.strptime(start, '%Y-%m-%d')
    def next_date():
        current_date = start_date
        for _ in range(n):
            yield current_date
            current_date += timedelta(days=1)
    date_gen = next_date()
    return [next(date_gen) for _ in range(n)]


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    if not isinstance(start_date, str):
        raise TypeError("start_date must be a string in the format yyyy-mm-dd")
    dr = date_range(start_date, len(values))
    return list(zip(dr, values))


def fees_report(infile, outfile):
	"""Calculates late fees per patron id and writes a summary report to
	outfile."""
	with open(infile, newline='') as csvfile:
		reader = DictReader(csvfile)
		late_fees = defaultdict(float)
		for row in reader:
			date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
			date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
			days_late = (date_returned - date_due).days
			if days_late > 0:
				late_fee = days_late * 0.25
			else:
				late_fee = 0
			late_fees[row['patron_id']] += late_fee
	with open(outfile, 'w', newline='') as csvfile:
		writer = DictWriter(csvfile, fieldnames=['patron_id', 'late_fees'])
		writer.writeheader()
		for patron_id, fee in late_fees.items():
			writer.writerow({'patron_id': patron_id, 'late_fees': f'{fee:.2f}'})


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
