# TO-DO For python3 and python2 compatiablity of poretools

## Just conversion to py3, py2 not tested... yet 

1. **stats** - printing throughout the loop for each addition of reads, failing tests. Expected outcome is one output. 
 -1. also not generating N50 or N75, don't know if this is a byproduct of the print issue or a sepperate issue

2. **qualdist** - seems to be working, but has too many decimals and fails test. 

3. **nucdist** - seems to be working, but has too many decimals and fails test. 

4. **yield_plot** 
	```Traceback (most recent call last):
  File "/home/sbrimer/Documents/poretools/ENV/bin/poretools", line 11, in <module>
    load_entry_point('poretools==0.6.0', 'console_scripts', 'poretools')()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 539, in main
    args.func(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 55, in run_subtool
    submodule.run(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/yield_plot.py", line 75, in run
    start_time = fast5.get_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 587, in get_start_time
    exp_start_time  = self.get_exp_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 431, in get_exp_start_time
    if self.keyinfo['tracking_id'].attrs['exp_start_time'].endswith('Z'):
TypeError: endswith first arg must be bytes or a tuple of bytes, not str
```
5. **squiggle** - need to rework next and import iterateitems
```	Traceback (most recent call last):
  File "/home/sbrimer/Documents/poretools/ENV/bin/poretools", line 11, in <module>
    load_entry_point('poretools==0.6.0', 'console_scripts', 'poretools')()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 539, in main
    args.func(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 55, in run_subtool
    submodule.run(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/squiggle.py", line 73, in run
    first_fast5 = fast5_set.next()
AttributeError: 'Fast5FileSet' object has no attribute 'next'```

6. **time**
	```Traceback (most recent call last):
  File "/home/sbrimer/Documents/poretools/ENV/bin/poretools", line 11, in <module>
    load_entry_point('poretools==0.6.0', 'console_scripts', 'poretools')()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 539, in main
    args.func(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 55, in run_subtool
    submodule.run(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/times.py", line 25, in run
    start_time = fast5.get_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 587, in get_start_time
    exp_start_time  = self.get_exp_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 431, in get_exp_start_time
    if self.keyinfo['tracking_id'].attrs['exp_start_time'].endswith('Z'):
TypeError: endswith first arg must be bytes or a tuple of bytes, not str
```
7. **occupancy**
	```Traceback (most recent call last):
  File "/home/sbrimer/Documents/poretools/ENV/bin/poretools", line 11, in <module>
    load_entry_point('poretools==0.6.0', 'console_scripts', 'poretools')()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 539, in main
    args.func(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 55, in run_subtool
    submodule.run(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/occupancy.py", line 64, in run
    start_time = fast5.get_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 587, in get_start_time
    exp_start_time  = self.get_exp_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 431, in get_exp_start_time
    if self.keyinfo['tracking_id'].attrs['exp_start_time'].endswith('Z'):
TypeError: endswith first arg must be bytes or a tuple of bytes, not str
```
8. **combine** - not sure about this one, may need work or better understanding of how to use it. 

9. **index**
```Traceback (most recent call last):
  File "/home/sbrimer/Documents/poretools/ENV/bin/poretools", line 11, in <module>
    load_entry_point('poretools==0.6.0', 'console_scripts', 'poretools')()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 539, in main
    args.func(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 55, in run_subtool
    submodule.run(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/index.py", line 35, in run
    start_time = fast5.get_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 587, in get_start_time
    exp_start_time  = self.get_exp_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 431, in get_exp_start_time
    if self.keyinfo['tracking_id'].attrs['exp_start_time'].endswith('Z'):
TypeError: endswith first arg must be bytes or a tuple of bytes, not str```

10. **readstats**
```Traceback (most recent call last):
  File "/home/sbrimer/Documents/poretools/ENV/bin/poretools", line 11, in <module>
    load_entry_point('poretools==0.6.0', 'console_scripts', 'poretools')()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 539, in main
    args.func(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 55, in run_subtool
    submodule.run(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/readstats.py", line 10, in run
    start_time = fast5.get_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 587, in get_start_time
    exp_start_time  = self.get_exp_start_time()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/Fast5File.py", line 431, in get_exp_start_time
    if self.keyinfo['tracking_id'].attrs['exp_start_time'].endswith('Z'):
TypeError: endswith first arg must be bytes or a tuple of bytes, not str```



## Working Modules - for py3
1. **fastq**
2. **fasta**
3. **winner**
4. **qualpos**
5. **hist**
6. **tabular**
7. **metadata**