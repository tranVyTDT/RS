from datetime import timedelta
import csv, json, requests, time

TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidHlwZSI6ImFjY2Vzc190b2tlbiIsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJiQGdtYWlsLmNvbSIsImV4cCI6MTYzNDU2MjEzNX0.9vNmQ8H4KodtdAgBQJGkKESQjD1lK80HSgqJ7EpImBw'

URL = 'http://127.0.0.1:8000/posts/'

HEADER_UPLOAD_LINK = {
        "Content-Type" : "application/json;charset=UTF-8",
        "Authorization" : f"Bearer {TOKEN}",
        "Connection" : "keep-alive",
        'Accept-Encoding': 'gzip, deflate, br'
}

def create_post():
    pass

with open('thu_tuc_19_sbn.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # row[0]: tt_id
            # row[0]: ten
            # print(f'\t{row[0]}, {row[1]}, {row[2]}.')
            data = {
                "post_id" : row[0],
                "title"   : row[1],
                "content"  : "abc",
                "category" : "abc"
            }
            
            try:
                requests.post(URL, headers=HEADER_UPLOAD_LINK, data=json.dumps(data))
            except Exception as err:
                print(err)
            
            time.sleep(1)
    
    print(f'Processed {line_count} lines.')
