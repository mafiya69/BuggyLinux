#!/usr/bin/env python2

from __future__ import print_function
from bs4 import BeautifulSoup as bs
import requests
import shutil
import sys
import os

def getRound():
    if len(sys.argv) < 2:
        return raw_input("Enter the round number : ")
    else:
        return sys.argv[1]

class buggylinux:

    def __init__(self):
        """
        Initializes the class
        """
        self.round = getRound()
        self.url = r"http://codeforces.com/contest/" + str(self.round) + r"/problems"

        print("Connecting to CodeForces...")
        self.soup = bs(requests.get(self.url).text)
        print("Connected!")

        self.tmpPath = os.path.expanduser("~/.buggy/" + str(self.round) + "/")

        self.data = [{}]
        self.input = []
        self.output = []


    def getIO(self):
        """
        Parses input/output data from self.soup
        """
        di = self.soup.findAll('div',{'class' : 'input'})
        do = self.soup.findAll('div',{'class' : 'output'})

        for x, y in zip(di, do):
            t1 = str(x).replace("<div class=\"input\"><div class=\"title\">Input</div><pre>","")
            t1 = t1.replace("<br/>","\n").replace("</pre></div>","")
            t2 = str(y).replace("<div class=\"output\"><div class=\"title\">Output</div><pre>","")
            t2 = t2.replace("<br/>","\n").replace("</pre></div>","")

            self.input.append(t1)
            self.output.append(t2)

    def getQuestion(self):
        """
        Parses Question from self.soup
        """
        t1 = []
        for x in self.soup.findAll('div', {'class' : 'title'}):
            t1.append(x.text)

        currQues = -1

        while len(t1) > 0:
            if t1[0] == "Input":
                try:
                    try:
                        self.data[currQues]["input"].append(self.input[0])
                        self.data[currQues]["output"].append(self.output[0])
                    except:
                        self.data[currQues]["input"] = []
                        self.data[currQues]["output"] = []
                        self.data[currQues]["input"].append(self.input[0])
                        self.data[currQues]["output"].append(self.output[0])
                finally:
                    self.input.pop(0)
                    self.output.pop(0)
                    t1.pop(0)

            elif t1[0] == "Output":
                t1.pop(0)

            else:
                currQues += 1
                self.data[currQues]["question"] = t1[0]
                t1.pop(0)
                self.data.append({})

        self.data.pop()

        i = 0
        for t1 in self.soup.findAll('div', {'class' : 'problem-statement'}):
            full_quest = ""
            for quest in t1.findAll('p'):
                full_quest = full_quest + '\n' + quest.text
            self.data[i]["detail"] = full_quest
            i += 1

    def showAll(self):
        """
        Show All data on screen
        """
        for dat in self.data:
            print("Question : ")
            print(dat["question"])
            print(dat["detail"])
            print("Input : ")
            for x in dat["input"]:
                print(x)
            print("Output : ")
            for x in dat["output"]:
                print(x)
            raw_input("Press Any Key...")

    def saveData(self):
        """
        Save data to Disk
        """
        for tgn in xrange(len(self.data)):

            tg = chr(ord('A') + tgn)
            tagPath = self.tmpPath + tg + "/"

            if not os.path.exists(tagPath):
                os.makedirs(tagPath)

            inputFile = tagPath + "input.txt"
            outputFile = tagPath + "output.txt"
            cppFile = tagPath + "program.cpp"

            fileI = open(inputFile, "w")
            for x in self.data[tgn]["input"]:
                try:
                    fileI.write(x)
                except:
                    fileI.write(x.encode('utf8'))
            fileI.close()

            fileO = open(outputFile, "w")
            for x in self.data[tgn]["output"]:
                try:
                    fileO.write(x)
                except:
                    fileO.write(x.encode('utf8'))
            fileO.close()

            fileTemp = open("template.cpp", "r")
            templateData = fileTemp.read()
            fileTemp.close()

            fileC = open(cppFile, "w")
            fileC.write("/*")
            try:
                fileC.write(self.data[tgn]["question"])
            except:
                fileC.write(self.data[tgn]["question"].encode('utf8'))
            try:
                fileC.write(self.data[tgn]["detail"])
            except:
                fileC.write(self.data[tgn]["detail"].encode('utf8'))
            fileC.write("*/\n\n")
            fileC.write(templateData)
            fileC.close()



            os.system("subl " + cppFile)

bl = buggylinux()
bl.getIO()
bl.getQuestion()
bl.saveData()
#bl.showAll()
