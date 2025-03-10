# Turing Machine Simulator Automarker

An automarking tool that uses the JSON TM's from this [simulator](https://tm.seagrass.co.za).

> [!WARNING]
> Currently in python, but will eventually switch over to a compiled language for performance reasons

## Usage

```bash
python3 automarker.py <json_tm_filepath> <test_string> <outcome>
```

### Arguments

1. Filepath to the JSON turing machine
2. Test String - need to specify an empty string as "<blank_symbol>"
3. Expected Outcome - 1 = Accepted, 0 = Rejected

### Output

The script will print 1 if the computated answer, and the expected answer match, else it will print 0.
