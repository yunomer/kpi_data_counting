import sys
import csv
from math import floor
from prettytable import PrettyTable
from dateutil import parser


def main():
    try:
        filename = sys.argv[1]
        with open(filename) as f:
            data = [{k: str(v) for k, v in row.items()} 
                    for row in csv.DictReader(f, skipinitialspace=True)]
    except Exception as e:
        print(e)
        print('No file input found or Wrong file format')

    resolved_done = 0
    closed_not_do = 0
    pending_external = 0
    canceled = 0
    pending_internal = 0
    waiting_support = 0
    other = 0

    new_subs = 0

    sub_internal = 0
    sub_external = 0

    sub_incomplete = 0

    # Done and closed records
    total_time = 0
    num_resolved_closed = 0
    total_rec_processed = 0


    for item in data:
        # SUB TOTAL
        if item['Status'] == 'Resolved' and item['Resolution'] == 'Done':
            resolved_done += 1
            created_time = parser.parse(item['Created'])
            resolved_time = parser.parse(item['Resolved'])
            diff = abs(resolved_time - created_time).total_seconds() / 3600.0
            total_time = total_time + diff
            num_resolved_closed += 1
            total_rec_processed = total_rec_processed + float(item['Custom field (Record Number)'])
        elif item['Status'] == 'Closed' and item['Resolution'] == 'Won\'t Do': 
            closed_not_do += 1
            created_time = parser.parse(item['Created'])
            resolved_time = parser.parse(item['Resolved'])
            diff = abs(resolved_time - created_time).total_seconds() / 3600.0
            total_time = total_time + diff
            num_resolved_closed += 1
            total_rec_processed = total_rec_processed + float(item['Custom field (Record Number)'])
        elif item['Status'] == 'Pending-External':
            pending_external += 1
        elif item['Status'] == 'Pending-Internal':
            pending_internal += 1
        elif item['Status'] == 'Canceled':
            canceled += 1
        elif item['Status'] == 'Waiting for support':
            waiting_support += 1
        else:
            other += 1
        # NEW_SUB
        if item['Custom field (Submission Type)'] == 'New':
            new_subs += 1
        # SUB_INTERNAL & Sub_EXTERNAL
        if item['Custom field (Request Source)'] == 'Internal':
            sub_internal += 1
        elif item['Custom field (Request Source)'] == 'External':
            sub_external += 1
    # SUB_INCOMPLETE == add open, waiting for support, pending-internal, pending-external
    sub_incomplete = other + waiting_support + pending_internal + pending_external

    # Find the time/record here
    average_time_record = round(((total_time*100)/100.0)/(total_rec_processed), 4)

    total = resolved_done + closed_not_do + pending_external + pending_internal + waiting_support + other
    x = PrettyTable()
    x.field_names = ['Status', 'Resolution', 'Count']
    x.add_row(['Resloved', 'Done', resolved_done])
    x.add_row(['Closed', 'Won\'t Do', closed_not_do])
    x.add_row(['Pending - internal', ' ', pending_internal])
    x.add_row(['Pending - external', ' ', pending_external])
    x.add_row(['Canceled', ' ', canceled])
    x.add_row(['Waiting for Support', ' ', waiting_support])
    x.add_row(['Other', ' ', other])
    x.add_row(['----------', '----------', '----------'])
    x.add_row(['Total (Excluding Canceled)', ' ', total])
    x.add_row(['----------', '----------', '----------'])
    x.add_row(['Total New Submissions', ' ', new_subs])
    x.add_row(['----------', '----------', '----------'])
    x.add_row(['Internal Submissions', ' ', sub_internal])
    x.add_row(['External Submissions', ' ', sub_external])
    x.add_row(['----------', '----------', '----------'])
    x.add_row(['Incomplete Submissions', ' ', sub_incomplete])
    x.add_row(['----------', '----------', '----------'])
    x.add_row(['Average Total time (Resolved & Closed)', ' ', str((floor(total_time*100)/100.0)/num_resolved_closed) + " hours"])
    x.add_row(['----------', '----------', '----------'])
    x.add_row(['Total Records processed', ' ', total_rec_processed])
    x.add_row(['----------', '----------', '----------'])
    x.add_row(['Average Time for Record', ' ', str(average_time_record) + " hour/records"])
    x.add_row(['----------', '----------', '----------'])
    print(x)       
        
        
if __name__ == '__main__':
    main()