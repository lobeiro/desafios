################################################################################
# Python Web Site vote Checking Script 08/06/2019
# Developer : Marcelo Lobeiro 
#
#    usage: redditVotes.py [-h] subreddit
#
#    Script de analise de votos em web site
#
#    positional arguments:
#      subreddit   Lista com nomes de subreddits separados por ponto-e-virgula
#                  (`;`). Ex: "askreddit;worldnews;cats"
#
#    optional arguments:
#      -h, --help  show this help message and exit
################################################################################

import os
import sys
import time 
import shutil
import argparse
import tempfile
import pyautogui
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup
from unidecode import unidecode

### Default Values of parameters definition
maximumPoints = 5000
siteUrl = 'https://old.reddit.com'
subredtiFlag = '/r/'
tmpDir   = 'pagina'
pathPage = os.path.abspath(r'.\\' + tmpDir)
tmpPage  = pathPage + r"\page.html"
pageRetry = 3
delTmpRetry = 3
outputReport = "output.txt"
pageFuncTimeout = 10
verboseMode = False
pyautogui.FAILSAFE = False

### Function for HTML Data Parsing
### parameter textPage => the text of HTML page
### parameter siteUrl  => the URL site of HTML page 
### returns a dictionary with formated according for idWall test request
def prcessingHTML(textPage,siteUrl):
    dictVotes = {}
    soup = BeautifulSoup(textPage,'html.parser')

    # TITLE THREAD
    threadTitles = []
    frases = soup.find_all('a',class_='title')
    for index,eachFrase in enumerate(frases):
        threadTitles.append(eachFrase.get_text())

    # POINTS THREAD
    threadPoints = []
    frases = soup.find_all(class_="score likes")
    for index,eachFrase in enumerate(frases):
        subSoup=BeautifulSoup(str(eachFrase),'html.parser')
        for linkComment in subSoup.find_all('div'):        
            if 'title' in str(linkComment):
                threadPoints.append(linkComment['title'])
            else:
                threadPoints.append('0')
                
    # TEST REQUESTED INFORMATION
    index=0
    frases = soup.find_all('div')
    for eachFrase in frases:
        try:
            comments = str(eachFrase['data-permalink'])
            if subredtiFlag in comments:
                comments = siteUrl + comments
            else:
                continue                
            dictVotes[index] = [threadPoints[index]]
            dictVotes[index].append(eachFrase['data-subreddit-prefixed'])    
            dictVotes[index].append(threadTitles[index])            
            postUrl = str(eachFrase['data-url'])
            if subredtiFlag in postUrl:
                postUrl = siteUrl + postUrl
            dictVotes[index].append(comments)
            dictVotes[index].append(postUrl)
            index+=1
        except:
            pass
    return dictVotes
 
### Function for delete and create a temporary area for HTML page saving
### parameter path  => the path of temporary HTML area
### parameter tries => the number of tries to delete path before fail
### returns true in case of success deleting and create path otherwise false
def prepareTmpDirectory(path,tries):
    try:
        if (os.path.exists(path)):
            tmp = tempfile.mktemp(dir=os.path.dirname(path))
            shutil.move(path, tmp)
            shutil.rmtree(tmp)
        os.makedirs(path)
        return True
    except:
        return False

### Function to create a formated printing output
### parameter text  => text to be printed
### returns a screen printing of text with datetime of execution
def printTextFormated(text):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")    
    print (date_time,' - ',text)   

### Main function
### returns an output file related to HTML votes processing
def main(arguments):
    parser = argparse.ArgumentParser(description="Script de analise de votos em web site")
    parser.add_argument('subreddit',type=str, help='Lista com nomes de subreddits separados por ponto-e-virgula (`;`). Ex: "askreddit;worldnews;cats"')
    
    argumentsAmount = len(arguments)
    if argumentsAmount==2:
        args = parser.parse_args([arguments[1]])
    else:
        args = parser.parse_args()    
    subReditList = (args.subreddit).split(';')

    print ("Inputs: ")
    print ("Text: ",subReditList)
    print ("=========================\n")
    
    #outHandle = open (outputReport,'w')  
    with open(outputReport, 'w') as outHandle:
        openBrowser=True
        countPageDataSucess=0
        for subreddit in subReditList:
            subreddit=subreddit.strip()
            tryGetPage = pageRetry
            pageDataSucess = False
            printTextFormated("Iniciando busca de pagina com subreddit " + subreddit)        
            while(tryGetPage>0):
                printTextFormated("Preparando arquivos temporarios...")
                if prepareTmpDirectory(tmpDir,delTmpRetry) == False:
                    printTextFormated("Erro ao preparar arquivos temporarios.")
                    return False
            
                if openBrowser==True:
                    webbrowser.open_new(siteUrl+subredtiFlag+subreddit)
                    openBrowser=False
                else:
                    pyautogui.hotkey('ctrl', 't')
                    time.sleep(2)
                    pyautogui.typewrite(siteUrl+subredtiFlag+subreddit)
                    pyautogui.hotkey('enter')
                time.sleep(pageFuncTimeout)
                    
                printTextFormated("Salvando pagina...")
                pyautogui.hotkey('ctrl', 's')
                time.sleep(2)   
                pyautogui.typewrite(tmpPage)
                time.sleep(2)
                pyautogui.hotkey('enter')
                time.sleep(2)            
                pyautogui.hotkey('esc')            
                time.sleep(pageFuncTimeout)

                try:
                    pageHandler = open(tmpPage,'r', encoding="utf-8")
                    textPage = pageHandler.read()
                    pageHandler.close()
                    tryGetPage = 0
                    pageDataSucess = True
                    countPageDataSucess+=1
                except:
                    printTextFormated("Bucando dados da pagina novamente..: " + str(tryGetPage))
                    openBrowser=True
                    tryGetPage-=1

            if pageDataSucess==False:
                printTextFormated("ERRO: Falha ao adquirir dados da pagina com subreddit " + subreddit)
                return False            

            printTextFormated("Processando dados da pagina com subreddit " + subreddit)            
            dictVotes = prcessingHTML(textPage,siteUrl)        
                    
            labels=[
                    '\npontuacao.........: ',
                    'subreddit.........: ',        
                    'titulo da thread..: ',
                    'link comentarios..: ',
                    'link thread.......: '       
                    ]      
            
            for eachData in dictVotes.values():        
                for index,data in enumerate(eachData):
                    if ('pontuacao' in  labels[index]) and (int(eachData[index]) <= maximumPoints):
                        break
                    if verboseMode == True:
                        print (labels[index],eachData[index])
                    outHandle.write(labels[index] + unidecode(eachData[index]) + '\n')
            printTextFormated("Dados pagina com subreddit " + subreddit + " gravados.")
        for eachTab in range(countPageDataSucess):
            pyautogui.hotkey('ctrl', 'w')    
        
        printTextFormated("Verifique o relatorio " + outputReport)
        #outHandle.close()
        return True
    
if __name__ == '__main__':
    main(sys.argv)

