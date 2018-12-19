import re
import datetime
from collections import defaultdict

linepattern = re.compile(r"\[(?P<date>.+)\] (?P<message>.*)")
def parse(line):
    match = linepattern.match(line.strip()).groupdict()
    datestr = match["date"]
    message = match["message"]
    date = datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M")
    return (date, message)


def calc_minutes(naps):
    minutes = [0 for i in range(60)]
    for (start, end) in naps:
        for i in range(start, end):
            minutes[i] += 1
    return minutes

with open("day4input.txt") as file:
    lines = [parse(line) for line in file.readlines()]
    lines.sort(key=lambda p: p[0])
    print(lines[0:100])
    sleeps = defaultdict(list)
    start = 0
    id = 0
    for (time, message) in lines:
        if message.startswith("Guard"):
            id = re.search(r"\#(\d+)", message).group(1)
            start = time.minute
        elif message.startswith("falls"):
            start = time.minute
        elif message.startswith("wakes"):
            sleeps[id].append((start, time.minute))

    print(sleeps)

    totals = dict([(key, sum([end - start for (start, end) in value])) for (key, value) in sleeps.items()])
    (sleepiest, amount) = max(totals.items(), key=lambda item: item[1])
    print(sleepiest)
    minutes = calc_minutes(sleeps[sleepiest])
    print(minutes)
    (target, amount) = max(enumerate(minutes), key=lambda item: item[1])
    print(sleepiest, target)
    print ("strategy 1", int(sleepiest) * target)

    allminutes = dict([(guard, calc_minutes(naps)) for (guard, naps) in sleeps.items()])
    print(allminutes)
    maxminutes = dict([(guard, max(enumerate(minutes), key=lambda item: item[1])) for (guard, minutes) in allminutes.items()])
    print(maxminutes)
    (victim, (minute, times)) = max(maxminutes.items(), key=lambda item: item[1][1])
    print(victim, minute, times)
    print(sleeps[victim])
    print(allminutes[victim])
    print("strategy 2", int(victim)*minute)


