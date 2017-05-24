import urllib2
import urllib
import sys
from urlparse import urlparse
import os.path
import operator
import time

visited_pages = []

def interpret_arguments():
    url = sys.argv[1]
    if not (url[0:7] == "https:/" or url[0:7] == "http://"):
        url = "http://" + url
    else:
        url = url.translate(None, "\\")
    filetype = sys.argv[2]
    return url, filetype, int(sys.argv[3])

def cull_links(url):
    visited_pages.append(url)
    links = []
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print "can not acess " + url + "(" + str(e.code) + ")"
        return []
    except urllib2.URLError, e:
        return []
    except:
        return []

    page = response.read()
    parsed_url = urlparse(url)
    scheme = parsed_url[0] + "://"
    netloc = parsed_url[1]
    path = parsed_url[2]
    keywords = ["href=","src="]
    for key in keywords:
        tmp_page = page
        while tmp_page.find(key)  >= 0:
            ref_mark = tmp_page.find(key) 
            tmp_page = tmp_page[ref_mark + len(key) + 1:]
            end_of_link = False
            for i in range((len(tmp_page)-1)):
                c = tmp_page[i:i+1]
                if c == "\"" or c == "\'":
                    link = tmp_page[0:i]
                    parsed_link = urlparse(link)
                    if parsed_link[0] == "":
                        link =  scheme + netloc + link
                    links.append(link)
                    tmp_page = tmp_page[i:]
                    end_of_link = True
                    break
            if not end_of_link:
                tmp_page = ""
    return set(links)

def filter(filetype, links):
    result = []
    for link in links:
        if(link[-len(filetype):]) == filetype:
            result.append(link)
    return result

def save_files(links):
    for link in links:
        split = link.split("/")
        filename = split[-1]
        illigal_chars = "*|\:\"<>?/"
        for c in illigal_chars:
            filename.replace(c, "")
        while (os.path.exists(filename)):
            filename = "_" + filename
        try:
            print "downloading " + filename + " ..."
            urllib.urlretrieve(link, filename)
        except:
            print "failed to download " + link
url = interpret_arguments()[0]
filetype = interpret_arguments()[1]
urls = [interpret_arguments()[0]]
max_depth = interpret_arguments()[2]


def main(urls, depth, max_depth):
    if max_depth > depth:
        for u in urls:
            if not u in visited_pages:
                print "crawling files from " + u + " (depth:" + str(depth) + ")"
                links = (cull_links(u))
                filtered_links = (filter(filetype, links))
                save_files(filtered_links)
                main(links, depth + 1, max_depth)

s = time.time()
main(urls, 0, max_depth)
e = time.time()
print("finished in: ") + str(e - s) + (" seconds")





