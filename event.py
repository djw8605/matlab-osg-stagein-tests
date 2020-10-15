import htcondor
import sys
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Process some HTCondor log files.')
parser.add_argument('logs', metavar='N', type=str, nargs='+',
                    help='Log file to parse')
args = parser.parse_args()

df = pd.DataFrame(columns=['start-stagein', 'end-stagein', 'execution', 'start-stageout', 'start-module'])
for logfile in args.logs:
    jel = htcondor.JobEventLog(logfile)
    events = {}
    for event in jel.events(stop_after=0):
        if event.type is htcondor.JobEventType.GENERIC:
            if event['info'].startswith("STAGE-IN Complete"):
                # Get the timestamp
                events['end-stagein'] = int(event['info'].split()[2])
            elif event['info'].startswith("EXECUTION Complete"):
                events['execution'] = int(event['info'].split()[2])
            elif event['info'].startswith("MODULE Load Start"):
                events['start-module'] = int(event['info'].split()[3])
            
        # Stage-in begins
        if event.type is htcondor.JobEventType.FILE_TRANSFER and event['Type'] == 2:
            events['start-stagein'] = event.timestamp
        if event.type is htcondor.JobEventType.FILE_TRANSFER and event['Type'] == 5:
            events['start-stageout'] = event.timestamp
    jel.close()
    #print(events)
    df = df.append(events, ignore_index=True)

df['stage-time'] = df['end-stagein'] - df['start-stagein']
df['total-time'] = df['execution'] - df['start-stagein']
df['execution-time'] = df['execution'] - df['end-stagein']
df['module-time'] = df['end-stagein'] - df['start-module']
df_elim = df[np.abs(df['total-time']-df['total-time'].mean()) <= (2*df['total-time'].std())]
#print(df)
print("Eliminating 2 std. deviations resulted in removing {} rows".format((len(df.index) - len(df_elim.index))))
print("Total time average: {:.2f}".format(df_elim['total-time'].mean()))
print("Total time std. dev.: {:.2f}".format(df_elim['total-time'].std()))

print("Stage-in average: {:.2f}".format(df_elim['stage-time'].mean()))
print("Stage-in std. dev.: {:.2f}".format(df_elim['stage-time'].std()))

print("Execution average: {:.2f}".format(df_elim['execution-time'].mean()))
print("Execution std. dev.: {:.2f}".format(df_elim['execution-time'].std()))

print("Module Load average: {:.2f}".format(df_elim['module-time'].mean()))
print("Module Load std. dev.: {:.2f}".format(df_elim['module-time'].std()))
