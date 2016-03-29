#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup

ONLYSHOWSUCCESS=False

def failure(total,DOMAIN,ErrorFile,errstr):
    if not ONLYSHOWSUCCESS :
        print '%-4i\t%-20s\t%s' %(total,DOMAIN,errstr)
    ErrorFile.writelines('%-4i\t%-20s\t%s\n' %(total,DOMAIN,errstr))

def successprocess(total,DOMAIN,TITLE,SuccessFile,errstr):
    print '%-4i\t%-20s\t%s' %(total,DOMAIN,TITLE)
    try :
        SuccessFile.writelines('%-4i\t%-20s\t%s\n' %(total,DOMAIN,TITLE.encode('utf-8')))
    except AttributeError:
        print errstr
        SuccessFile.writelines('%-4i\t%-20s\t%s\n' %(total,DOMAIN,errstr))

def main():

    InputFile=open('domain','rU')
    SuccessFile=open('success.log','w+')
    ErrorFile=open('error.log','w+')

    total=0
    success=0
    fail=0

    for line in InputFile :
        total+=1
        DOMAIN=line[1:-5]
        TRYWWW=False

        try :
            url='http://'+DOMAIN
            html=urllib2.urlopen(url,timeout=2).read()
        except :
            TRYWWW=True
            try :
                url='http://www.'+DOMAIN
                html=urllib2.urlopen(url,timeout=2).read()
            except :
                failure(total,DOMAIN,ErrorFile,'[Fail-1:Connect Error]')
                fail+=1
                continue
        try :
            soup=BeautifulSoup(html)
            TITLE=soup.title.string
        except AttributeError:
            if TRYWWW==True :

                failure(total,DOMAIN,ErrorFile,'[Fail-2:No Title]')
                fail+=1
            try :
                url='http://www.'+DOMAIN
                html=urllib2.urlopen(url,timeout=2).read()
            except :

                failure(total,DOMAIN,ErrorFile,'[Fail-3:Connect Error]')
                fail+=1

            try :
                soup=BeautifulSoup(html)
                TITLE=soup.title.string
            except AttributeError:
                failure(total,DOMAIN,ErrorFile,'[Fail-4:No Title]')
                fail+=1
            except :
                failure(total,DOMAIN,ErrorFile,'[Fail-5:BeautifulSoup Error]')
                fail+=1

            else :
                successprocess(total,DOMAIN,TITLE,SuccessFile,'[Fail-6:Write Error]')
                success+=1
        except :
            failure(total,DOMAIN,ErrorFile,'[Fail-7:BeautifulSoup Error]')
            fail+=1

        else :
            successprocess(total,DOMAIN,TITLE,SuccessFile,'[Fail-8:Write Error]')
            success+=1

    InputFile.close()
    SuccessFile.close()
    ErrorFile.close()
    print '----------\nTotal=%i\nSuccess=%i\nFail=%i' %(total,success,fail)


if __name__ == '__main__' :

    main()
