#!/bin/bash

# Pull in Data From Multiple Addresses and Update .csv's Associated


# btc2csv.sh -t <TextFileWithAddresses>
# Help Message
help(){
        echo ""
        echo -e "DESCRIPTION:"
        echo ""
        echo -e "\tbtc2csv.sh Utilizes a python script to convert a series of"
        echo -e "\taddress to a series of CSV files"
        echo ""
        echo -e "SYNOPSIS: "
        echo ""
        echo -e "\tbtc2csv.sh [ -h ] | [ -t addresses.txt ]"
        echo ""
        echo -e "SETTINGS: "
        echo ""
        echo -e "\t-h     Display this help message."
        echo -e "\t-t     Takes a filename filled with addresses. Each address"
        echo -e "\t       on a newline. Lines with # are Comments"
        echo ""
        echo ""
        exit 1;
}

# TextFile
TEXTFILE=""
UpdatedFiles=""

# Get CLI Flags
while getopts "t:h" OPTIONS; do
    case $OPTIONS in
        t) TEXTFILE=${OPTARG};;
        h) help;  exit 0;;
    esac
done

if [[ $TEXTFILE == "" ]]; then
    # Check if we have a text file. This script needs a text file
    echo "Error: Please Specify a Text File with Addresses"
    help
else
    # Grab the total addresses in the text file.
    totaladdresses=`wc -l $TEXTFILE | cut -f 1 -d " "`
    # Counter for Current Address
    onaddress=0
    # Loop through all the addresses
    while read address
    do
        # Ignore lines that start with #
        if  [[ ${address:0:1} == "#" ]]
        then
            # Ignore Line It's a Comment Increment and continue
            let "onaddress++"
            continue
        else
            # Print a status message
            echo " File $onaddress of $totaladdresses "
            # Cycle Through Addresses and Run Python Command for each
            #echo "Trying Address:"
            #echo "$address"
            csvfilename=${address:0:5}.csv
            if [ -a csvs/$csvfilename ]
                then
                    # Check if the file has changed Get total lines in csv
                    beforetempfilesize=`wc -l csvs/$csvfilename | cut -f 1 -d " " `
                    #echo $beforetempfilesize
                    #echo "File $csvfilename exists Updating"
                    # Run through the command using existing File
                    python ./main.py -a $address -x csvs/$csvfilename -o csvs/$csvfilename
                    # Get total lines again
                    aftertempfilesize=`wc -l csvs/$csvfilename | cut -f 1 -d " " `
                    #echo $aftertempfilesize
                    if [ $aftertempfilesize -gt $beforetempfilesize ]
                    then
                        # File has Changed
                        # Add Filename to New Records
                        UpdatedFiles="$UpdatedFilescsvs/$csvfilename \t\t $address \n"
                    fi
                    # If Not no need to update
                else
                    # echo "File $csvfilename does not exist Creating"
                    # Run through command using new file
                    python ./main.py -a $address -o csvs/$csvfilename
                    # Add File to Updated Files Status Message
                    UpdatedFiles="$UpdatedFilescsvs/$csvfilename \t\t $address \n"
                fi
                # Only Sleep If Actually Called File
                # Put in a Wait so you don't run afoul of blockchain.info rate limiting
                sleep 5s
            fi
        # Always Increment
        #echo "Incrementing Counter"
        let "onaddress++"
    # Makes it loop through the text file
    done < $TEXTFILE
    
    if [[ $UpdatedFiles == "" ]]; then
        # No Files to Update
        echo "No Updated Files"
        exit 0;
    else
        # Print Updated Files
        echo "Printing Updated Files..."
        echo ""
        echo ""
        echo "-------------------Updated Files-----------------"
        echo ""
        # Actually print the updates
        echo -e $UpdatedFiles
        exit 0;
    fi
fi

# Should be redundant
exit 0


