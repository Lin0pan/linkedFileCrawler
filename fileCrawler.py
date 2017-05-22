import urllib2
import urllib
import sys
import socket
from urlparse import urlparse

#url  = "https://iccl.inf.tu-dresden.de/web/Theoretische_Informatik_und_Logik_(SS2017)"
#filetype = "pdf"

def interpret_arguments():
    url = sys.argv[1]
    if not (url[0:7] == "https:/" or url[0:7] == "http://"):
        url = socket.gethostbyname(url)
    else:
        url = url.translate(None, "\\")
    filetype = sys.argv[2]
    return url, filetype

def cull_links(url):
    links = []
    response = urllib2.urlopen(url)
    parsed_url = urlparse(url)
    scheme = parsed_url[0] + "://"
    netloc = parsed_url[1]
    path = parsed_url[2]
    keyword = "href="
    for i in range(2):
        page = response.read()
        while page.find(keyword)  >= 0:
            ref_mark = page.find(keyword) 
            page = page[ref_mark + len(keyword) + 1:]
            end_of_link = False
            for i in range((len(page)-1)):
                c = page[i:i+1]
                if c == "\"" or c == "\'":
                    link = page[0:i]
                    parsed_link = urlparse(link)
                    if parsed_link[0] == "":
                        link =  scheme + netloc + link
                    links.append(link)
                    page = page[i:]
                    end_of_link = True
                    break
            if not end_of_link:
                page = ""
            keyword = "src="
    return set(links)

def filter(filetype, links):
    result = []
    for link in links:
        if(link[-len(filetype):]) == filetype:
            result.append(link)
    return result

def save_files(links):
    for link in links:
        print "downloading " + link + " ..."
        split = link.split("/")
        file_name = split[-1]
        urllib.urlretrieve(link, file_name)


url = interpret_arguments()[0]
filetype = interpret_arguments()[1]
links = (cull_links(url))
filtered_links = (filter(filetype, links))
save_files(filtered_links)



