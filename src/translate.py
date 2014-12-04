import urllib2

def translate(message):
    # Needs to be appended with &hl=LANGUAGE, &tl=LANGUAGE, and &text=STRING
    requestURL = "http://translate.google.com/translate_a/t?client=t&sl=auto&multires=1&sc=1"
    url = requestURL + "&hl=en&tl=en&text=" + urllib2.quote(message)
    
    request = urllib2.Request(url)

    # Fake browser request, google won't allow it otherwise
    request.add_header("Proxy", None)
    request.add_header("User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")

    response = urllib2.urlopen(request)

    result = response.read()
    # Response structure looks something like this:
    # [[["A little", "Un poco",,,,...] , ......

    start = str.find(result,'"')+1
    end = str.find(result, '"', start)
    # All casts in the original code? => Python
    return result[start:end]
