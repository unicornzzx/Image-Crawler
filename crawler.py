import socket   #for sockets
import threading 
import os
import re

port = 80

def formalLink(foundURL,fatherURL): # judge a URL found in a html file is an absolute path or relative path, and change them to absolute path
    host = ''
    if foundURL.split('/')[0] == 'http:': # absolute path
        foundURL = foundURL
        host = foundURL.split('/')[2]
    elif foundURL.split('/')[0] == fatherURL.split('/')[3]: # relative path (in the same root directory with fatherURL)
        host = host = fatherURL.split('/')[2]
        foundURL = 'http://' + host + '/' + foundURL
    else:
        host = fatherURL.split('/')[2]
        foundURL = fatherURL + foundURL
    return (foundURL, host) # return a tuple

def createFolder(url): # create a set of folders for a webpage
    lista = url.split('/')
    path = ''
    for i in range(2,len(lista)): # ignore the 'http://'
        if i == 2:
            path = path + lista[i]
        elif lista[i] == '':
            path = path
        else:
            path = path + '\\' +lista[i]
    if os.path.exists(path):
        path = path
    else:
        os.makedirs(path)
    path = os.getcwd() + '\\'+path
    return path

def get(linkInfo): # request to certain webpage and return the reply
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((linkInfo[1], port))
    msg = 'GET '+ linkInfo[0] +' HTTP/1.1\r\nhost: '+ linkInfo[1] + '\r\n'+ 'Connection: Close\r\n\r\n'
    s.sendall(msg.encode())
    buffer = [] #############this part is from internet source################
    while True:
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break;
    reply = b''.join(buffer)
    s.close()
    header, body = reply.split(b'\r\n\r\n',1)
    result = b'200 OK' in header #############this part is from internet source################
    return (body, result)
    
def getImg(imgLink, path): # download the image by given img url, and store them in associated folders
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    reg = r'/?([^/]+?\.(gif|jpg|jpeg|png|webp))'
    dirPattern = re.compile(reg, re.I)
    dir = (dirPattern.findall(imgLink[0]))[0]# get the name of img from the URL
    s.connect((imgLink[1], port))
    msg = 'GET '+ imgLink[0] +' HTTP/1.1\r\nhost: '+ imgLink[1] + '\r\n'+ 'Accept: image/' + dir[1] +'*/*\r\nConnection: Close\r\n\r\n'
    print(msg)
    s.sendall(msg.encode())
    buffer = [] #############this part is from internet source################
    while True:
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break;
    reply = b''.join(buffer)
    s.close()
    header, img = reply.split(b'\r\n\r\n',1)
    result = b'200 OK' in header #############this part is from internet source################
    if result:
        print ('image from link ' + imgLink[0] + ' download successfully')
        f = open(path + '\\' + dir[0],'wb')
        f.write(img)
        f.close()
    else:
        print (imgLink[0] + 'is an invalid URL for image') 

def getImgList(html, fatherURL):
    reg = br'=[\s]?"([^=<>]*?\.)(gif|jpg|jpeg|png|webp)"'
    imgPattern = re.compile(reg, re.I)
    imgList = imgPattern.findall(html) # find all urls of images in the given html file, return them as a list
    for i in range (0, len(imgList)): # change each element in above list to a formal linkInfo
        imgList[i] = formalLink((imgList[i][0].decode() + imgList[i][1].decode()), fatherURL)
    imgList = list(set(imgList)) # eliminate the duplication
    return imgList

def getLinkList(html, fatherURL): 
    reg = br'href[\s]?=[\s]?"([\S]*?)"'
    hrefPattern = re.compile(reg, re.I)
    hrefList = hrefPattern.findall(html)# find all urls of href links in the given html file, add them to a list
    print (hrefList)
    for i in range (0, len(hrefList)): # change each element in above list to a formal linkInfo
        hrefList[i] = formalLink(hrefList[i].decode(), fatherURL)
    hrefList = list(set(hrefList)) # eliminate the duplication
    print (hrefList)
    return hrefList
    
def repeating(depth,links):
    if depth >= 0:    # the variable depth represents maxDepth - current depth
        print ('depth = ' + str(depth))
        nextLinks = []    # this list which will contain all href in next recursion
        for i in range (0, len(links)):
            reply = get(links[i]) # get html file for this link
            if reply[1]:
                print ('successfully connect to' + links[i][0])
                path = createFolder(links[i][0])
                imgList = getImgList(reply[0], links[i][0])    # add all img URLs to a list
                if len(imgList) == 0:
                    print('no img in webpage: ' + links[i][0])
                else:
                    threadList = []
                    for m in range(0,len(imgList)):    # download all imgs in the html file of this href
                        t = DownloadThread(imgList[m], path)
                        threadList.append(t)
                    for n in range(0,len(imgList)):
                        threadList[n].start()
                a = getLinkList(reply[0], links[i][0])
                print (a)
                nextLinks.extend(getLinkList(reply[0], links[i][0]))
            else:
                print(links[i][0] + ' is an invalid URL      depth = ' + str(depth))
        if len(nextLinks) == 0:    # in this case, each html files in current depth has no href URL
            depth = -1
        else:
            depth -= 1
        repeating(depth,nextLinks)
    else:
        print('Done')
        
def inputMaxDepth():
    maxDepth = 5
    stillLoop1 = True
    stillLoop2 = True
    while (stillLoop1):
        answer = input('Do you want reset the maximum depth(default: 5)?   y/n')
        if answer == 'y'or answer == 'Y':
            while(stillLoop2):
                newDepth = input('Enter the new maximum depth (positive integer):')
                try: 
                    nd = int(newDepth)
                    if nd > 0:
                        maxDepth = nd
                        stillLoop2 = False
                    else:
                        print('Invalid input, please enter a positive integer.')
                except Exception as e:
                    print('Invalid input, please enter a positive integer.')    
            stillLoop1 = False
        elif answer == 'n' or answer =='N':
            stillLoop1 = False
        else:
            print('Invalid input, please enter y/n')
    return maxDepth
    
class DownloadThread(threading.Thread):# about downloading all imgs for a html file 
    def __init__(self, imgLink, path):
        threading.Thread. __init__(self)
        self.imgLink = imgLink
        self.path = path
        
    def run(self):
        getImg(self.imgLink, self.path)


rec = input('Please input the url of starting point (do not include :"http://" !!!)')
maxDepth = inputMaxDepth()
url = 'http://' + rec
host = rec.split('/')[0]
initLinks = [(url,host)]
print(initLinks)
repeating(maxDepth,initLinks)
