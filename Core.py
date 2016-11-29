import thread
import Queue
import re
import urllib
import urlparse
import time
import sys
processedURLsCounter = 0
dupcheck = set()
queue = None  # Html Queue
textToLookFor = None
searchingLimit = None
matchesList = []


def processInitialUserInput():
    global queue, textToLookFor, searchingLimit
    searchingLimit = raw_input("Type in the maximum number of pages you want to search into:\n")
    queue = Queue.Queue(int(searchingLimit))
    if len(sys.argv) < 2:
        queue.put('http://' + raw_input("Type in a link without http//: \n"))
    else:
        queue.put(sys.argv[1])
    textToLookFor = raw_input("Type in a word that you want to look for: \n")
    logFile = open("errorLog.txt", "w")
    logFile.close()


def processAndTellResult():
    print("Searching done, writing results to matches.txt ...")
    resultFiles = open("matches.txt", "w")
    resultFiles.close()
    resultFiles = open("matches.txt", "a")
    resultFiles.write("Word matched: " + textToLookFor + "\n\n")
    for match in matchesList:
        resultFiles.write(match)
    resultFiles.close()
    print("Done! Matches have been written into matches.txt \n")


def queueURLs(html, origLink):  # Processes HTML code looking for other URLs inside the domain
    for url in re.findall('''<a[^>]+href=["'](.[^"']+)["']''', html, re.I):
        link = url.split("#", 1)[0] if url.startswith("http") else '{uri.scheme}://{uri.netloc}'.format(uri=urlparse.urlparse(origLink)) + url.split("#", 1)[0]
        if link in dupcheck:  # Checks if link has already been processed
            continue
        dupcheck.add(link)
        if len(dupcheck) > 99999:
            dupcheck.clear()
        if processedURLsCounter >= int(searchingLimit):
            with queue.mutex:  # Clears queue in a thread safe way
                queue.queue.clear()
        else:
            queue.put(link)


def getHTML(link):
    try:
        global processedURLsCounter
        processedURLsCounter = processedURLsCounter + 1
        html = urllib.urlopen(link).read()
        print("Processing link: " + link + "\n")
        for match in re.findall(r"((<p([A-Za-z-0-9=\"'_ \\-]|\s){0,}?[>])){1}(.{0,}?" + textToLookFor + r".{0,}?)(<[\/|\\]?([A-Za-z-0-9=\"'_ \-]|\s){0,}?p[>]){1}", html):
            print("Match found:\n")
            print(str(match[3]) + "\n\n")
            matchesList.append("Link:\n " + link + "\nMatched paragraph:\n " + match[3] + "\n\n")
        queueURLs(html, link)  # Asks queueURLs to look for other links in that page
    except (KeyboardInterrupt, SystemExit):
        dupcheck.add(link)
        raise
    except Exception, e:
        dupcheck.add(link)
        print("Error while processing: " + link + " check errorLog.txt for more details \n")
        logFile = open("errorLog.txt", "a")
        logFile.write("Error processing " + link + " : " + str(e) + "\n")
        logFile.close()
        pass


processInitialUserInput()

while queue.empty() is not True or len(dupcheck) < 1:
    thread.start_new_thread(getHTML, (queue.get(),))
    time.sleep(0.5)

processAndTellResult()
