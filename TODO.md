# TO-DO For python3 and python2 compatiablity of poretools

## Just conversion to py3, py2 not tested... yet 

1. **stats** - printing throughout the loop for each addition of reads, failing tests. Expected outcome is one output. 
 -1. also not generating N50 or N75, don't know if this is a byproduct of the print issue or a sepperate issue

2. **qualdist** - seems to be working, but has too many decimals and fails test. 

3. **nucdist** - seems to be working, but has too many decimals and fails test. 

4. ~~**yield_plot** 
Traceback (most recent call last):
  File "/home/sbrimer/Documents/poretools/ENV/bin/poretools", line 11, in <module>
    load_entry_point('poretools==0.6.0', 'console_scripts', 'poretools')()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 539, in main
    args.func(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 55, in run_subtool
    submodule.run(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/yield_plot.py", line 96, in run
    plot_collectors_curve(args, start_times, read_lengths)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/yield_plot.py", line 35, in plot_collectors_curve
    d = {'start': [start_times[n] for n in xrange(0, len(start_times), step)],
NameError: name 'xrange' is not defined~~

5. **squiggle** - need to rework next ~~and import iterateitems~~
`WARNING:poretools:Could not extract template events for read: test_data/2016_3_4_3507_1_ch13_read1474_strand.fast5.
`

6. ~~**time**
Traceback (most recent call last):
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
TypeError: endswith first arg must be bytes or a tuple of bytes, not str~~

7. ~~**occupancy** Traceback (most recent call last):
  File "/home/sbrimer/Documents/poretools/ENV/bin/poretools", line 11, in <module>
    load_entry_point('poretools==0.6.0', 'console_scripts', 'poretools')()
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 539, in main
    args.func(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/poretools_main.py", line 55, in run_subtool
    submodule.run(parser, args)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/occupancy.py", line 81, in run
    plot_performance(parser, args, tot_reads_per_pore)
  File "/home/sbrimer/Documents/poretools/ENV/lib/python3.5/site-packages/poretools-0.6.0-py3.5.egg/poretools/occupancy.py", line 39, in plot_performance
    d = {'rownum': range(1,17)*32, TypeError: unsupported operand type(s) for *: 'range' and 'int ~~


8. ~~**combine** - not sure about this one, may need work or better understanding of how to use it.~~ User error :/

9. ~~**index**
Traceback (most recent call last):
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
TypeError: endswith first arg must be bytes or a tuple of bytes, not str~~

10. **readstats**
~~start_time channel_number  read_number template_events complement_events
poretools internal error in file 'test_data/YYYYMMDD_HHMM_SampleID/Fail/1/2016_3_4_3507_1_ch120_read443_strand.fast5': unknown HDF5 structure: can't find read block item
                 Please report this error (with the offending file) to:
                 https://github.com/arq5x/poretools/issues~~  ** Not and error, test data has older file structure **

11. **logger** - doesn't log currently? 


## Working Modules - for py3
1. **fastq**
2. **fasta**
3. **winner**
4. **qualpos**
5. **hist**
6. **tabular**
7. **metadata**
8. **combine** 
9. **index**
10. **times**
11. **occupancy**
12. **yield_plot**
13. **readstats**