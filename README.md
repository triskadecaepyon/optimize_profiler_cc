# optimize_profiler_cc
A code profiler that uses Radon Cyclomatic Complexity output to identify optimizable code.

## Motivation
In programming languages such as Python, the prototyping nature of such languages promote rapid code development with less focus on code refactoring or optimization.  Many reasons exist to not spend any time or resources to optimize completed code, but recent advances in software tools now allow for significant increases in performance to existing code with little penalty to testing and integration efforts.  Tools such as Continuum Analytics’ <a href="http://numba.pydata.org">*Numba*</a> package use *Python Decorators* (different from decorator patterns) that optimize a given function at the LLVM and assembly level, and can vastly optimize code with minimal syntax disruption.  

However, efforts typically revolve around detection of candidacy for optimizable code, versus the application of optimization tools on the codebase.  Software metrics such as McCabe’s Cyclomatic Complexity and the Maintainability Index (MI) can give insight into the specific optimizations that can be done on code, and can identify candidates in an automated or programmatic process quickly.

## Dependencies
Input requirements:
- <a href="http://radon.readthedocs.org/en/latest/">Radon</a>
- Radon McCabe's Cyclomatic Complexity output in JSON format <a href="http://radon.readthedocs.org/en/latest/commandline.html">(info here)</a>
- Example call (in bash): 
```
radon cc -s -i "../" -j ../django/django/db > django_db.json
```

Addition Python package dependencies:
- NumPy
- Pandas

## Usage
####Importing
```
from optimize_profiler_cc.optimize_profiler_cc import OptimizeProfilerCC as opcc
myrunner = opcc('django_db.json')
myrunner.run_cc_report()
```
####Natively in Project
```
myrunner = OptimizeProfilerCC('django_db.json')
myrunner.run_cc_report()
```
Instantiating an a OptimizeProfilerCC class with a Radon cc JSON output gives callable methods on the processed file. Running the report below gives a textual report on the recommend flagged functions and methods per file:
```
Running search...
--------------------------
Module Files: 89
Module Classes: 307
Module Methods: 1890
Module Functions: 94
Module Complexity Mean: 3.03928415539
Module Complexity Median: 2.0
Module Complexity Standard Deviation: 4.31640685612
--------------------------
File name: ../django/django/db/__init__.py
--------------------------
Flag Optimize - Sig name: reset_queries | Type: function | CC: 2 | LineNum: 54
Flag Optimize - Sig name: close_old_connections | Type: function | CC: 2 | LineNum: 62
--------------------------
File name: ../django/django/db/backends/base/base.py
--------------------------
Flag Optimize - Sig name: queries_logged | Type: method | CC: 2 | LineNum: 74
Flag Optimize - Sig name: queries | Type: method | CC: 2 | LineNum: 78
```
Callable methods:
- _run_cc_report(force_min_cc=None)_
  - Runs the report, and can force the minimum CC used for analysis and flagging
- _load_new_file(input_file_name)_
  - Allows for the loading of a new JSON file into the class
- _get_raw_cc_data()_
  - Gives back a shallow copy of the parsed and analyzed data in a Pandas Dataframe
- _get_file_name()_
  - Returns the file name of the file

#Future of Project
- _Integrated Radon Framework_
  - The current iteration of this project only uses the JSON output of Radon's output; future programmatic usage of Radon is planned such that one can directly call their file in Python to run the report
- _Additional analysis of static code for non-CC items_
 - Finding of specific optimizable structures such as for loops, list loops, etc.
- _Installable package from pip or conda install_
  - Easily install and analyze within one's own Python environment 

#License
- BSD
