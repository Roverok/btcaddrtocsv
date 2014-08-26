#!/bin/bash

# Pull in Data From Multiple Addresses and Update .csv's Associated


# btc2csv.sh -t <TextFileWithAddresses>

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

while getopts "t:h" OPTIONS; do
    case $OPTIONS in
        t) TEXTFILE=${OPTARG};;
        h) help;  exit 0;;
    esac
done

if [[ $TEXTFILE == "" ]]; then
    echo "Error: Please Specify a Text File with Addresses"
    help
else
    totaladdresses=`wc -l $TEXTFILE | cut -f 1 -d " "`
    onaddress=0
    while read address
    do
        if  [[ ${address:0:1} == "#" ]]
        then
            # Ignore Line It's a Comment
            let "onaddress++"
            continue
        else
            echo " File $onaddress of $totaladdresses "
            # Cycle Through Addresses and Run Python Command for each
            #echo "Trying Address:"
            #echo "$address"
            csvfilename=${address:0:5}.csv
            if [ -a csvs/$csvfilename ]
                then
                    beforetempfilesize=`wc -l csvs/$csvfilename | cut -f 1 -d " " `
                    #echo $beforetempfilesize
                    #echo "File $csvfilename exists Updating"
                    # Run through the command using existing File
                    python ./main.py -a $address -x csvs/$csvfilename -o csvs/$csvfilename
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
                fi
                # Only Sleep If Actually Called File
                # Put in a Wait so you don't run afoul of blockchain.info rate limiting
                sleep 5s
            fi
        # Always Increment
        #echo "Incrementing Counter"
        let "onaddress++"
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
        echo -e $UpdatedFiles
        exit 0;
    fi
fi

# Should be redundant
exit 0


