import urllib2
import urllib
import sys
from urlparse import urlparse
import os.path

def interpret_arguments():
    url = sys.argv[1]
    if not (url[0:7] == "https:/" or url[0:7] == "http://"):
        url = "http://" + url
    else:
        url = url.translate(None, "\\")
    filetype = sys.argv[2]
    return url, filetype

def cull_links(url):
    links = []
    response = urllib2.urlopen(url)
    page = response.read()
    parsed_url = urlparse(url)
    scheme = parsed_url[0] + "://"
    netloc = parsed_url[1]
    path = parsed_url[2]
    keyword = "href="
    depth_links = []
    for i in range(2):
        tmp_page = page
        while tmp_page.find(keyword)  >= 0:
            ref_mark = tmp_page.find(keyword) 
            tmp_page = tmp_page[ref_mark + len(keyword) + 1:]
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
        filename = split[-1]
        illigal_chars = "*|\:\"<>?/"
        for c in illigal_chars:
            filename.replace(c, "")
        while (os.path.exists(filename)):
            filename = "_" + filename
        urllib.urlretrieve(link, filename)
    print "downloaded " + str(len(links)) + " files."


url = interpret_arguments()[0]
filetype = interpret_arguments()[1]
links = (cull_links(url))
filtered_links = (filter(filetype, links))
save_files(filtered_links)



