#!/usr/bin/python3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import collections

def mysum(list):
    return 0 if len(list) == 0 else sum(list)

def parse_data(filename):
    events = {}

    with open(filename) as f:
        # Example line:
        # 14-04-2016 11:01:28.737 UTC 200 GET /url_a 0.000863 seconds
        for l in f.readlines():
            date, time, tz, status, method, path, latency, _ = l.split()
            dt = datetime.strptime(date + " " + time, "%d-%m-%Y %H:%M:%S.%f")
            # Build up a dictionary of timestamp -> number of events happening at that time
            events[dt] = 1

    time_series = pd.Series(events)

    # Count how many events were in each 50ms period
    time_series = time_series.resample('50L', how=mysum)
    return time_series

def save_png(time_series):
    fig = plt.figure()
    p = time_series.plot(style=".")
    fig.add_subplot(p)
    fig.savefig('graph.png')

def print_values_over(time_series, max):
    print(time_series[time_series >= max])

def display_graph(time_series):
    fig = plt.figure()
    p = time_series.plot(style=".")
    fig.add_subplot(p)
    plt.show()

ts = parse_data('access.log')

q1 = ts.quantile(0.25)
q3 = ts.quantile(0.75)

outlier_boundary = q3 + (3*(q3-q1))

print(outlier_boundary)

print_values_over(ts, outlier_boundary)

buckets_by_number_of_events = collections.defaultdict(lambda: 0)
for value in ts:
    buckets_by_number_of_events[value] += 1

display_graph(pd.Series(buckets_by_number_of_events))
print(pd.Series(buckets_by_number_of_events))
save_png(pd.Series(buckets_by_number_of_events))
display_graph(ts)
