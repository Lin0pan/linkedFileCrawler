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


page = fetch_url("https://www.golem.de")
print (cull_links(page))




