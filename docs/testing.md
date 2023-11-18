# Shapely to Plotly Regression Testing

The regression testing system is based mostly on directed random testing, 
and runs under pytest (https://docs.pytest.org/).

The pytests are self-checking, and do not produce a visual graph by default.

We typically also run the following scripts, and visually check the result:
* docs/example1.py
* examples/splotches.py
* examples/planet_3d.py

The last two require Numpy.

## Pytest Tests

The pytest tests are stored in the tests directory.
Run pytest either from the root or tests directories.

In addition, the tests can be run as normal scripts, and debugged normally under a debugger.

Example:
```commandline
shapely_plotly\tests>python test_line2d.py -h

usage: Usage: test_line2d.py [options] tests...

Tests can be regular expressions.  All matching test names will be matched.

Defined tests are:
   test_linestring_plot2d
   test_linering_plot2d
   test_multiline_plot2d

positional arguments:
  test_list             List tests to execute at the end. These are regular expressions. All matching tests will
                        executed.

options:
  -h, --help            show this help message and exit
  -s, --show            Show the results of any geometries built during the test.
  -n TEST_NUM, --test_num TEST_NUM
                        For random tests, which random seeds to run. Can be given twice to define a beginning and
                        (exclusive) end.

```

The random test system uses integer test identifiers to seed the random number generators.
The same random tests are run every time, unless the user explicitly specifies a different test range.

To run 50 random tests from test 50 to 99 (the end test is exclusive):

```commandline
shapely_plotly\tests>python test_line2d.py -n 50 -n 100 "test_.*"

Running Test test_linestring_plot2d


Running Test test_linering_plot2d


Running Test test_multiline_plot2d
```

You can debug a single test with just a single -n parameter.
If you want to actually see the randomly generated geometry, add -s:

```
shapely_plotly\tests>python test_line2d.py -n 1 -s ".*linest.*"
```


