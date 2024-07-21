# from src.main.packages.common.splunk import splunk_connection
#
#
# sb = splunk_connection.SplunkConnection('localhost', port=8089, username='Muthamizh',password='Rocky@001')
# print(sb.connect())
# print(sb.service)
from datetime import datetime, timedelta
import yaml
from src.main.packages.common.splunk import splunk_operations1

sb = splunk_operations1.SplunkOperations('localhost', 8089, 'Muthamizh', 'Rocky@001')
with open('/Users/muthamizh/PycharmProjects/datapipeline/src/main/packages/config/get_data.yaml', 'r') as f:
    data = yaml.safe_load(f)

start_time = data['start_time']
end_time = data['end_time']
x = (end_time - start_time)
print(x.total_seconds())
no_of_chunks = int(x.total_seconds() / 300)
print("no of chunks: ", no_of_chunks)
no_of_144_chunks = int(no_of_chunks / 144)
print("No of 144 chunks: ", no_of_144_chunks)
last_chunk = int(no_of_chunks % 144)
print("last chunk: ", last_chunk)
e_time = start_time
for i in range(no_of_144_chunks):
    print("Going to run")
    sb.run_hello_in_parallel(12, e_time)
    print("process complete")
    e_time += timedelta(hours=1)

# '2024-07-21T18:57:04.442+05:30'
