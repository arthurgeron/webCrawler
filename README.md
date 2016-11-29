# webCrawler
Web crawler made in python.

After you define the starting URL this script will use the urllib and re libraries to find more URLs on that page's source code while also looking for a text that contains the word or phrase you've entered.  

Simply run the Python and enter type in the following info:
Number of pages you want to search into
The address where the crawler should start looking from
The word or text you're looking for

You can also use the script with the following parameters and jump right into execution:
python Core.py "Url with http or https here" "Exact word or phrase you want to search for" "Max number of URLs you want to process"

It will write any matches to matches.txt, errors will be written to errorLog.txt. The script deletes these files each time you run it, so be sure to save the results before running it again.
