# DMAP-Date-Divider
## Installation
### Requirements
* Pandas 0.2.0+
* numpy 1.13.0
### Download
All code is contained within the DMAP-Date-Divider.py file. Clone or download the repository, or just the py file.

## Running
DMAP-Date-Divider is designed to be either run from the command line or within an environment.

### Data Format
Data must be stored in a text (.txt) file, in a comma separated format, with a new line for each row.
Data **MUST** be sorted by both Species code **and** Grid Reference, this is not done by the program.
Data file should not have headings

Example File:
```
101,"TF0171",1898
101,"NN5114",2007
101,"NN5114",2007
101,"SP9811",1940
101,"SP9811",2010
101,"SP9812",2010
102,"NN5114",2007
```
Example File Output:
```
 101
TF0171 G
NN5114 A
SP9811 D
SP9812 A
-1
 102
NN5114 A
-1

```
### Running From Command Line/Shell
Navigate to src directory.
Run program with
```
python DMAP-Date-Divider.py
```
There are six command line arguments available:
* inFile
* outFile
* date
* before
* after
* both
```
 -h, --help            show this help message and exit
  -i INFILE, --inFile INFILE
                        Path to input file
  -o OUTFILE, --outFile OUTFILE
                        Path for output file
  -d DATE, --date DATE  Cut off date
  --before 				Symbol to display in DMAP for grid references before cut off date
  --after 				Symbol to display in DMAP for grid references after cut off date
  --both 				Symbol to display in DMAP for grid references both sides of cut off date
```
Leave an argument out for default values.
For example: a input file called IN.txt, output file called OUT.txt, 1960 cut off date, G D A for before, both and after respectively.
```
 python DMAP-Date-Divider.py --inFile="IN.txt" --outFile="OUT.txt" --date=1960 --before=G --after=A --both=D
 ```
 These are also the default options.
### Manual Execution
1. Open DMAP-Date-Divider.py in preferred environment.
2. Run DMAP-Date-Divider.py
3. Each option will be presented in turn, enter values; blank answers will fall back on default values.
 ```
λ python DMAP-Date-Divider.py
Enter input file path: IN.txt
Enter output file path: OUT.txt
Enter the cut off date (Included in before): 1960
Enter symbol code for before date data: G
Enter symbol code for after date data: A
Enter symbol code for both date data: D
```
