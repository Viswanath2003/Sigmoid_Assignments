#!/bin/bash
#
#Shell script to change the value in the file sig.conf based on user input validation.
#
conf_file="sig.conf"

while true; do
        read -p "Enter Component Name [INGESTOR/JOINER/WRANGLER/VALIDATOR]: " component
        case "$component" in
            INGESTOR|JOINER|WRANGLER|VALIDATOR)
                break
                ;;
            *)
                echo "Invalid Component. Try again :)"
                ;;
        esac
done

while true; do
	read -p "Enter Scale [MID/HIGH/LOW]: " scale
        case "$scale" in
            MID|HIGH|LOW)
                break
                ;;
            *)
                echo "Invalid Scale. Try again :)"
                ;;
        esac
done

while true; do
        read -p "Enter View [Auction/Bid]: " view
        case "$view" in
            Auction)
                view_str="vdopiasample"
                break
                ;;
            Bid)
                view_str="vdopiasample-bid"
                break
                ;;
            *)
                echo "Invalid View. Try again :)"
                ;;
        esac
done

while true; do
        read -p "Enter Count (0-9): " count
        case "$count" in
            [0-9])
                break
                ;;
            *)
                echo "Invalid Count. Enter single digit (0-9) :)"
                ;;
        esac
done

echo "Got the valid inputs!"
echo "Finding the maching from the file $conf_file...."


match1="${view_str} ; ${scale} ; ${component} ; ETL ; vdopia-etl=$count"
match="${view_str} ; ${scale} ; ${component} ; ETL ;"

lineno=0
flag=0
while IFS= read -r line; do
	((lineno++))
	if [[ "$line" == "$match1" ]]; then
		echo "This input is already present in the file. Try with different values!"
		flag=1
		break

	elif [[ "$line" == "$match"* ]]; then
		echo "Match found!!"
		echo "Updating the line."
		flag=2
		sed -i "s/$line/$match1/" "$conf_file"
		echo "Updated."
		echo "$lineno: $match1"
		break;
	fi
done < "$conf_file"

if [[ $flag == 0 ]]; then
	echo -e "This input is not on the file.\nAppending this to the file."
	echo "$match1" >> $conf_file
fi