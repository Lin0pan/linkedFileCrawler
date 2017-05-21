import urllib2
import urllib
import sys

url  = "https://iccl.inf.tu-dresden.de/web/Theoretische_Informatik_und_Logik_(SS2017)"
filetype = "pdf"

print arguments
def cull_links(url):
    links = []
    response = urllib2.urlopen(url)
    page = response.read()
    domain = url.split("/")[0] + "//" + url.split("/")[2]
    while page.find("href=")  >= 0:
        ref_mark = page.find("href=") 
        page = page[ref_mark + 6:]
        end_of_link = False
        for i in range((len(page)-1)):
            c = page[i:i+1]
            if c == "\"" or c == "\'":
                link = page[0:i]
                if not (link[0:7] == "https:/" or link[0:7] == "http://"):
                    link = domain + link
                links.append(link)
                page = page[i:]
                end_of_link = True
                break
        if not end_of_link:
            page = ""
    return links

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



links = (cull_links(url))
pdfs = (filter(filetype, links))
save_files(pdfs)



