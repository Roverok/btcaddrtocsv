# Bitcoin Public Address to CSV Tools

This is two scripts that can provide the ability to pull Bitcoin Public Address information off blockchain.info's API and put it into a CSV file. It is broken into two parts.

## main.py - Pulling a single address.

```main.py``` provides the ability to pull a single address down from blockchain.info's api and store it in a CSV file. Usage:

```
main.py [-h] -a BTCADDRESS [-o OUTPUTFILE] [-x EXISTING]

optional arguments:
  -h, --help            show this help message and exit
  
  -a BTCADDRESS, --btcaddress BTCADDRESS Bitcoin Address 
  
  -o OUTPUTFILE, --outputfile OUTPUTFILE CSV Formatted Output File
  
  -x EXISTING, --existing EXISTING CSV Formatted Existing File
```

Eample in use:

```
$ python3 main.py -a 1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd -x 1M72S.csv -o 1M72S.csv
```

In this example main.py will pull the transaction info for ```1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd``` (Sean's Outpost Donation address). It will pull the info into a csv file and leave a spot for you to add custom notes. If you want to update the an old csv file with custom notes (as in this example). You can specify the former .csv file. It can be the same file.

## btc2csv.sh - Pulling Multiple Addresses

```btc2csv.sh``` provides a wrapper to call main.py a number of times and grab a numerous amount of btc addresses. Usage:

```
DESCRIPTION:

        btc2csv.sh Utilizes a python script to convert a series of
        address to a series of CSV files

SYNOPSIS:

        btc2csv.sh [ -h ] | [ -t addresses.txt ]

SETTINGS:

        -h     Display this help message.
        -t     Takes a filename filled with addresses. Each address
               on a newline. Lines with # are Comments
```

Example in Use:

```
$ ./btc2csv.sh -t addresses.txt
```

In this example ```btc2csv.sh``` will pull all the addresses listed in addresses.txt. Lines beginning with # are ignored. It outputs each addresses data into a csv file in ```./csvs/1ST5L.csv``` where "1ST5L" is the first five characters of the BTC address in question.

## .CSV Format

Below is an example of the format used:

| Date | Time | Account | Description | Money In | Money Out | Notes |
|:-----|:-----|:--------|:------------|:---------|:----------|:------|
| 14-08-26 | 16:11:07 | 1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd | 73cfc9a5456b6e1904e2905dab07e6e9377af66c10d825f81eee93a877f4b5ef | 0.001 | 0.0 | Sample Manual Added Note |
| 14-08-25 | 20:21:36 | 1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd | fb0b14980194671725341b5998ebb47a036652bff61d90436ec0dd01e4e1b162 | 0.0 | 0.17760045 |  |

Values:

| Item | Description |
|:-----|:------------|
| Date | A Day in YY-MM-DD |
| Time | A 24 Hour UTC Time|
| Account | The Public Address In question |
| Description | The Transaction ID |
| Money In | How much BTC cam in (Can be in Scientific Notation)| 
| Money Out | How much BTC went out (Can be in Scientific Notation)|


## Todo

* Add Name Custimization options to ```btc2csv.sh```
* Better documentation of Python Code.
* Add ability to pull directly from running bitcoind instance
* Add ability to output to more formats like .ods
* Add GUI? Maybe not sure if actually desired.