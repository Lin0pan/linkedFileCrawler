import urllib2

def fetch_url(url):
    response = urllib2.urlopen(url)
    return response.read()

def cull_links(page):
    links = []
    while page.find("href=")  >= 0:
        ref_mark = page.find("href=") 
        page = page[ref_mark + 6:]
        for i in range((len(page)-1)):
            c = page[i:i+1]
            if c == "\"" or c == "\'":
                links.append(page[0:i])
                page = page[i:]
                break
    return links

def filter(filetype, links):
    result = []
    for link in links:
        if(link[-len(filetype):]) == filetype:
            result.append(link)
    return result


page = fetch_url("https://iccl.inf.tu-dresden.de/web/Theoretische_Informatik_und_Logik_(SS2017)")
links = (cull_links(page))
print (filter("pdf", links))



