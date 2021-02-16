# -*- encoding: utf-8 -*-

import re
import json

class Parser():

    _lineArray = []

    _outputJSON = {
        "Natuknica" : "",
        "Vrsta riječi" : "",
        "Gramatička obilježja" : [],
        "Definicije" : []
    }


    def parseFile(self, filename):
        self._file = open(filename, encoding='utf-8', mode='r')
        self._result = open("result.htm", encoding='utf-8', mode='w')
      

        for line in self._file:
            if line[0:2] != '<p':
                continue
            if line[0:3] == '<p>':
                currentLine = self.parseLineClear(line)
            else:
                currentLine = self.parseLineUnclear(line)
            
            if  currentLine[0] != '<':          
                y = re.search(r'im\s?[m|ž|s]',currentLine)             
                if y:
                    currentLine = self.stripOne(currentLine)
                    currentLine = self.stripTwo(currentLine)
                    self._lineArray.append(currentLine)
                    self._result.write(currentLine)

        for line in self._lineArray:
            print(line)
            self.parseToJSON(line)
            with open("output.json", "a", encoding='utf-8') as outfile:  
                json.dump(self._outputJSON, outfile) 
            self._outputJSON = {
                "Natuknica" : "",
                "Vrsta riječi" : "",
                "Gramatička obilježja" : [],
                "Definicije" : []
            }


        
      
        self._file.close()
        self._result.close()
        
##one koje pocinju sa <p>
    def parseLineClear(self, line):
        return re.sub(r'^<p(\s(\S)*)*><font ((\S)*(\s)*(\S)*\s(\S)*);">',"",line)

##one koje pocinju sa <p ...>
    def parseLineUnclear(self, line):
        return re.sub(r'^<p(\s(\S)*)><font ((\S)*(\s)*(\S)*\s(\S)*);">',"",line)

##micanje tagova
    def stripOne(self, line):
        return re.sub(r'(\s)*<(.)font><font(.)*?>'," ",line)
        

    def stripTwo(self, line):
        return re.sub(r'<(.)font(.)*>',"",line)
        

##vrati sve rijeci
    def getWord(self, line):
        return re.match(r'(\S)*\s', line)
        

    def parseToJSON(self, line):

        self._outputJSON = {
            "Natuknica" : "",
            "Vrsta riječi" : "",
            "Gramatička obilježja" : [],
            "Definicije" : []
        }

        x = re.match(r'([a-ž]+)', line)
        if x != None:
            self._outputJSON["Natuknica"] = x.group(0)

        x = re.search(r'(im\s?[m|ž|s]\s?[sg|pl]?)', line)
        if x != None:
            keyword = x.group(0).rstrip()
            #print(keyword)
            if('s' in keyword[2:4]):
                self._outputJSON["Vrsta riječi"] = "Imenica srednjeg roda "
            if('m' in keyword[2:4]):
                self._outputJSON["Vrsta riječi"] = "Imenica muškog roda "
            if('ž' in keyword[2:4]):
                self._outputJSON["Vrsta riječi"] = "Imenica ženskog roda "

            if 'p' in keyword:
                self._outputJSON["Vrsta riječi"] += "plurale tantum"
            if 'sg' in keyword:
                self._outputJSON["Vrsta riječi"] += "singularia tantum"
            if 'zb' in keyword:
                self._outputJSON["Vrsta riječi"] += "Zbirna imenica"
        

        attributes = re.search(r'\((.*?)\)', line)

        if attributes != None:
            attributes = attributes.group(0)

            x = attributes
            word = re.search(r'\((.*?)\;', x)
            if word != None: 
                self._outputJSON["Gramatička obilježja"].append(word.group(0)[1:-1])
            
        
        if attributes != None:
            definition = re.search(r'\).*', line)
            self._outputJSON["Definicije"].append(definition.group(0)[1:])
            




def main():
    parser = Parser()
    parser.parseFile('./pagesInOne.htm')


if __name__ == '__main__' : main()