# csv2md

csv2md turns CSV into a clean GitHub-flavored Markdown table. It reads a file or standard input, handles quoted fields, embedded commas and newlines, doubled quotes, empty cells and ragged rows, and prints a table you can paste straight into a README, issue or pull request.

Built by the Commonwealth swarm. Every change arrives as a pull request from an agent, passes the checks in `test.sh`, and is reviewed by another member's agent before it is merged.

## Requirements

Python 3.8 or newer. No dependencies.

## Install

No pip needed. Download `csv2md.py`, or clone the repository:

```
git clone https://github.com/commonwealthswarm/csv2md
```

## Usage

```
python3 csv2md.py data.csv              # read a file
cat data.csv | python3 csv2md.py        # read stdin
python3 csv2md.py - < data.csv          # - also means stdin
python3 csv2md.py --delimiter ';' data.csv
```

From Python:

```python
from csv2md import convert
print(convert("a,b\n1,2\n"), end="")
```

## Examples

Simple table:

```
name,role
Ada,Engineer
Grace,Admiral
```

```
| name | role |
| --- | --- |
| Ada | Engineer |
| Grace | Admiral |
```

Quoted field with a comma and a newline:

```
product,notes
"Widget, large","Ships in a box
Assembly required"
```

```
| product | notes |
| --- | --- |
| Widget, large | Ships in a box<br>Assembly required |
```

Ragged rows are padded to the widest row:

```
a,b,c
1
1,2,3,4
```

```
| a | b | c |  |
| --- | --- | --- | --- |
| 1 |  |  |  |
| 1 | 2 | 3 | 4 |
```

## Rules

The first row is the header. A `|` inside a cell becomes `\|`. Newlines inside a cell become `<br>`. Leading and trailing whitespace in each cell is stripped. A leading UTF-8 byte order mark is ignored. Blank input prints nothing.

## Exit codes

`0` on success, `1` if the file cannot be read or is not valid UTF-8.

## Tests

```
bash test.sh
```

## License

MIT
