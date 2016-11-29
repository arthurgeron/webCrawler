import thread
import Queue
import re
import urllib
import urlparse
import time
import sys
processedURLsCounter = 0
errorCounter = 0
matchCounter = 0
dupcheck = set()
queue = None  # Html Queue
textToLookFor = None
searchingLimit = None
matchTextRegex = None
matchesList = []


def processInitialUserInputAndInitiateVariables():
    global queue, textToLookFor, searchingLimit, matchTextRegex
    if len(sys.argv) >= 4:
        searchingLimit = sys.argv[3]
    else:
        searchingLimit = raw_input("Type in the maximum number of pages you want to search into:\n")
    queue = Queue.Queue(int(searchingLimit))  # It's best to hard-code the queue's limit just in case
    if len(sys.argv) < 2:   # This was an experimental flag, which allows the user to run the python script with flags
        queue.put('http://' + raw_input("Type in a link without http//: \n"))
    else:
        queue.put(sys.argv[1])
    if len(sys.argv) >= 3:
        textToLookFor = sys.argv[2]
    else:
        textToLookFor = raw_input("Type in a word that you want to look for: \n")
    logFile = open("errorLog.txt", "w")
    logFile.close()
    matchTextRegex = [r"((<p([A-Za-z-0-9=\"'_ \\-]|\s){0,}?[>])){1}(.{0,}?",
                      r".{0,}?)(<[\/|\\]?([A-Za-z-0-9=\"'_ \-]|\s){0,}?p[>]){1}"]


def processAndTellResult():
    print("Searching done, writing results to matches.txt ...")
    resultFiles = open("matches.txt", "w")
    resultFiles.close()
    resultFiles = open("matches.txt", "a")
    resultFiles.write("Word matched: " + textToLookFor + "\n\n")
    for match in matchesList:
        resultFiles.write(match)
    resultFiles.close()
    print("Done! Matches have been written into matches.txt \nURLs processed: " + str(processedURLsCounter)
          + "\nURLs with positive matches: " + str(matchCounter) + "\nErrors while processing URLs: "
          + str(errorCounter))


def queueURLs(html, origLink):  # Processes HTML code looking for other URLs inside the domain
    for url in re.findall(r'<a[^>]+href=["\'](.[^"\']+)["\']', html, re.I):  # Searches the HTML for other URLs
        link = url.split("#", 1)[0] if url.startswith("http") else '{uri.scheme}://{uri.netloc}'.format(uri=urlparse.urlparse(origLink)) + url.split("#", 1)[0]
        if link in dupcheck:  # Checks if link has already been processed
            continue
        dupcheck.add(link)
        if len(dupcheck) > 99999:  # It's better to avoid memory overflow problems
            dupcheck.clear()
        if processedURLsCounter >= int(searchingLimit):
            with queue.mutex:  # Clears queue in a thread safe way
                queue.queue.clear()
        else:
            queue.put(link)


def getHTML(link):
    try:
        global processedURLsCounter, matchCounter, errorCounter
        processedURLsCounter += 1
        html = urllib.urlopen(link).read()  # Here we transform a URL into a string containing the HTML code of the page
        print("Processing link: " + link + "\n")
        # Bellow it will scan the HTML code for texts inside P elements which contain the chosen word or phrase
        for match in re.findall(matchTextRegex[0] + textToLookFor + matchTextRegex[1], html, re.I):
            # If it gets inside the loop it has basically found a match
            matchCounter += 1
            print("Match found:\n")
            print(str(match[3]) + "\n\n")  # Warns the user that it has found a match
            # Adds match to list so we can throw all that into a text file later, doing this while processing HTMLs
            # will just slow the process
            matchesList.append("Link:\n " + link + "\nMatched paragraph:\n " + match[3] + "\n\n")
        queueURLs(html, link)  # Query queueURLs to look for other links in that page
    except (KeyboardInterrupt, SystemExit):  # User can interrupt the process anytime
        dupcheck.add(link)
        raise
    except Exception, e:
        errorCounter += 1
        dupcheck.add(link)  # If the link generates an exception we need to make sure it won't process it again
        print("Error while processing: " + link + " check errorLog.txt for more details \n")
        logFile = open("errorLog.txt", "a")
        logFile.write("Error processing " + link + " : " + str(e) + "\n")  # Writes error to log file
        logFile.close()
        pass


processInitialUserInputAndInitiateVariables()

while queue.empty() is not True or len(dupcheck) < 1:  # Core loop of this script, starts the chain effect
    thread.start_new_thread(getHTML, (queue.get(),))
    time.sleep(0.5)  # Without this the while loop will cycle too fast and think that the queue is empty

processAndTellResult()
