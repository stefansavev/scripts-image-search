# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
 
def read_names(fname):
  with open(fname) as f:
    content = f.readlines()  
    def process_line(line):
      line = line.rstrip()
      key = line.split("|")[0]
      return (key.strip().lower(), map(lambda name: name.strip(), line.split("|")))
    return map(process_line, content)

import os
def mkdir(dir_name):
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

def read_key(fname):
  with open(fname) as f:
    return f.read().strip()
 

def main():
    import json
    import io
    mkdir("output")

    
    key = read_key('bingkey.txt')

    for (orig, parsed) in read_names("flower-names.txt"):
        d = "output" + "/" + orig
        mkdir(d)
        for query in parsed:
          filename = d + "/" + query + ".txt"  
          if (os.path.exists(filename)):
            print "skipping query " + query + " because file " + filename + " exists"
          else:
            print "running query " + query
            res = bing_image_search(key, "flower " + query)
            output = [(orig, query, res)] 
            #json.dump(output, outfile) 

            with io.open(filename, 'w', encoding='utf-8') as f:
              f.write(unicode(json.dumps(output, sort_keys = True, indent = 4, ensure_ascii=False)))

    #query = "sunshine"
    #query ="daisy"
    #print bing_search(query, 'Web')
    #bing_search(query, 'Image')
 
def bing_image_search(key, query):
    search_type = "Image"
    #search_type: Web, Image, News, Video

    query = urllib.quote(query)
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = (':%s' % key).encode('base64')[:-1]
    auth = 'Basic %s' % credentials
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=50&$format=json'
    request = urllib2.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib2.build_opener()
    response = request_opener.open(request) 
    response_data = response.read()
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']
    i = 0
    items = []
    for item in result_list:
      #print("item: " + str(i))
      #print(item)
      content = item[u'ContentType']
      url = item[u'MediaUrl']
      items.append((content, url))      
      i += 1
      #print("------------")
    #print result_list
    #return result_list
    return items

if __name__ == "__main__":
  import sys
  done = False
  #guard against network errors  
  while (not done):
    try:
      main()
      done = True
    except KeyboardInterrupt:
      print "Stopping the program" 
      done = True
    except:
      print "Unexpected error:", sys.exc_info()[0]
      


