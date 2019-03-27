# gcide2sqlite
A simple tool for converting the [GNU Collaborative International 
Dictionary of English](http://gcide.gnu.org.ua/) to an SQLite database, with
the option of filtering out words. The filter file should list each word to
be filtered on a new line. An example filter list is 
[available here](https://www.cs.cmu.edu/~biglou/resources/bad-words.txt).

## Usage

```
usage: gcide2sqlite.py [-h] [--ignore IGNORE] dir outfile

Convert the GNU Collaborative InternationalDictionary of English to an SQLite
database

positional arguments:
  dir              path to the GCIDE directory
  outfile          output file path

optional arguments:
  -h, --help       show this help message and exit
  --ignore IGNORE  optional file containing words to ignore
```
