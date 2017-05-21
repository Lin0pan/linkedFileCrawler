import urllib2
import urllib

def cull_links(url):
    links = []
    response = urllib2.urlopen(url)
    page = response.read()
    split = url.split("/")
    domain = split[0] + "//" + split[2]
    print domain
    while page.find("href=")  >= 0:
        ref_mark = page.find("href=") 
        page = page[ref_mark + 6:]
        for i in range((len(page)-1)):
            c = page[i:i+1]
            if c == "\"" or c == "\'":
                link = page[0:i]
                if not (link[0:7] == "https:/" or link[0:7] == "http://"):
                    link = domain + link
                links.append(link)
                page = page[i:]
                break
    print "links:"
    return links

def filter(filetype, links):
    result = []
    for link in links:
        if(link[-len(filetype):]) == filetype:
            result.append(link)
    return result

def save_files(links):
    for link in links:
        split = link.split("/")
        file_name = split[-1]
        urllib.urlretrieve(link, file_name)



links = (cull_links("https://iccl.inf.tu-dresden.de/web/Theoretische_Informatik_und_Logik_(SS2017)"))
pdfs = (filter("pdf", links))
print pdfs
save_files(pdfs)



