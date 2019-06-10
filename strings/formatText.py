###########################################################################
# Python Text Formater Script 06/06/2019
# Developer : Marcelo Lobeiro 
#
#    usage: formatText.py [-h] text limit justify
#
#    Formatador de texto.
#
#    positional arguments:
#      text        Texto que dever ser formatado.
#      limit       Numero de caracteres por linha.
#      justify     Justificar o texto de saida. (True/False)
#
#    optional arguments:
#      -h, --help  show this help message and exit
###########################################################################

import sys
import argparse

### Default Values of parameters definition
DEFAULT_INPUT_TEXT = "In the beginning God created the heavens and the earth. Now the earth was formless and empty, darkness was over the surface of the deep, and the Spirit of God was hovering over the waters.\n" + "\n" +  "And God said, \"Let there be light,\" and there was light. God saw that the light was good, and he separated the light from the darkness. God called the light \"day,\" and the darkness he called \"night.\" And there was evening, and there was morning - the first day."
DEFAULT_LIMIT = 40;
DEFAULT_JUSTIFY = True;

### Function for Text justification
### parameter text  => the text to be justified
### parameter limit => characters value per line to be achieved
### returns a justified text based on 'limit' parameter as width per line.
def justifyText(text,limit):
    textSplit = text.split('\n')
    justifiedText=''
    for eachLine in textSplit:
        if eachLine=='':
            justifiedText+='\n'
            continue
        lineSplit = eachLine.split(' ')
        spaceSize=1
        listSpace=[]
        for eachWord in lineSplit:
            if len(eachWord)==0:
                continue
            listSpace.append(len(eachWord))
            listSpace.append(spaceSize)
        if len(listSpace)==0:
            continue
        else:
            listSpace=listSpace[:-1]
        while((sum(listSpace)<limit) and (spaceSize<limit)):
            spaceSize+=1
            for index in range(1,len(listSpace)-1,2):
                listSpace[index]=spaceSize
                if sum(listSpace)>=limit:
                    break
        index=1
        for eachWord in lineSplit:
            justifiedText+=eachWord
            if index<len(listSpace):
                justifiedText+=listSpace[index]*' '
            index+=2
        justifiedText+='\n'

    return justifiedText

### Function for text format
### parameter text    => the text to be formated
### parameter limit   => maximum number of characters per line
### parameter justify => Enable text justification
### returns a formated text with 'limit' characters per line with/without justification
def formatText(text,limit,justify):
    fullText=lineCompose=lineComposeBack = ''
    textSplit = text.split('\n')
    for eachLine in textSplit:
        eachLine+='\n'
        lineSplit = eachLine.split(' ')
        lineBuffer=lineCompose= ''
        for eachWord in lineSplit:
            lineComposeBack=lineCompose
            lineCompose+=eachWord
            if (len(lineCompose)>limit):
                lineBuffer+=lineComposeBack+'\n'
                lineCompose=eachWord
            if (len(lineCompose)>0) and (lineCompose!='\n'):
                lineCompose+=' '
        fullText+=lineBuffer+lineCompose
    fullText=fullText.replace(' \n','\n')
    if justify==True:
        fullText = justifyText(fullText,limit)
        
    return fullText        

### Function for checking boolean input in argparse
### parameter value => The string entered as boolean parameter
### return a boolean value acoording to text value or raise an exception
def boolCheck(value):
    value= value.upper().strip()
    if value == 'TRUE':
        return True
    elif value =='FALSE':
        return False
    else:
        raise argparse.ArgumentTypeError('Valor esperado True ou False.')

if __name__ == '__main__':
    
    text = DEFAULT_INPUT_TEXT;
    limit = DEFAULT_LIMIT;
    justify = DEFAULT_JUSTIFY;    

    parser = argparse.ArgumentParser(description="Formatador de texto.")

    parser.add_argument('text',type=str, default=DEFAULT_INPUT_TEXT, help='Texto que dever ser formatado.')
    parser.add_argument('limit',type=int, default=DEFAULT_LIMIT,help='Numero de caracteres por linha.')
    parser.add_argument('justify',type=boolCheck,default=DEFAULT_JUSTIFY , help='Justificar o texto de saida. (True/False)')

    argumentsAmount = len(sys.argv)
    if argumentsAmount==2:
        args = parser.parse_args([sys.argv[1],str(DEFAULT_LIMIT),str(DEFAULT_JUSTIFY)])
        text = args.text
    if argumentsAmount==3:
        args = parser.parse_args([sys.argv[1],sys.argv[2],str(DEFAULT_JUSTIFY)])
        text,limit  = args.text,args.limit
    if argumentsAmount==4:
        args = parser.parse_args([sys.argv[1],sys.argv[2],sys.argv[3]])    
        text,limit,justify    = args.text,args.limit,args.justify
    
    # Print input data
    print ("Inputs: ")
    print ("Text: ",text)
    print ("Limit: ",limit)
    print ("Should justify: ",justify)
    print ("=========================")

    # Run Formatter
    outputText = formatText(text,limit,justify)

    # Print output text
    print ("Output: ")
    print (outputText)    



