Matlab OSG Runtime Tests
========================

The scripts and submit files to run the OSG's matlab stagein tests.


Processing
----------

After the jobs have completed, you can process the log files for statistics.  To prepare your environment:

    $ python3 -m venv venv
    $ .  venv/bin/activate
    $ pip install -r requirements.txt

To process the logs and report statistics in the console:

    $ python event.py logs/*.log

The output will be similar to:

```
Eliminating 2 std. deviations resulted in removing 2 rows
Total time average: 48.23
Total time std. dev.: 21.23
Stage-in average: 18.20
Stage-in std. dev.: 15.08
Execution average: 30.03
Execution std. dev.: 10.81
Module Load average: 1.12
Module Load std. dev.: 1.14
```

