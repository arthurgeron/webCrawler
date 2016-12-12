# Web Crawler
Web crawler made in python.

# How it works
After you define the starting URL this script will use the urllib and re libraries to find more URLs on that page's source code while also looking for a text that contains the word or phrase you've entered.  

# How to use it
(Optional) Set proxies:
Edit the list proxies (line 18) and add your own proxies, example:
```python
proxies = [ # Place your proxy list here with port, example: exampleproxy.com:8080
    {'http': 'http://exampleproxy.com:80'},
    {'http': 'http://0.0.0.0:3127'}
  ]
```
Run the Python script and enter type in the following info:
Number of pages you want to search into
The address where the crawler should start looking from
The word or text you're looking for

You can also initialize thie script with the following parameters and jump right into execution:
python Core.py "Url with http or https here" "Exact word or phrase you want to search for" "Max number of URLs you want to process"
Example:
```python
python Core.py "https://www.stackoverflow.com" "You" "50"
```

# Additional info and recommendations

It will write any matches to matches.txt, errors will be written to errorLog.txt. The script deletes these files each time you run it, so be sure to save the results before running it again.
