import discord
from discord.ext import commands
from discord.utils import get
from PIL import ImageGrab
import sys
import random
import ffmpeg
import asyncio
from os import listdir
from os.path import isfile, join
import re
import xlwt 
from xlrd import open_workbook

bot = commands.Bot(command_prefix='>')
logOut = 0
def emojif(word):
    currentletters = 0
    result = ''
    for letter in word:
        for c in letter:
            if c == '(' or c == ')' or c == "'" or c == '"' or c == ",":
                continue
            if c == '.':
                result = result + '.'
                continue
            if c == ' ':
                result = result + '   '
                continue
            else:
                result = result + ':regional_indicator_' + c + ':'
    return(result)

@bot.command()
async def emojify(ctx,*meow):
    await ctx.send(emojif(str(meow)))

    
    
toPlay = []
names = []
pickedSong = ""
def playAll(folder, specificSong, userName):
    folder = folder.lower()
    if folder == "minecraft":
        mainFolder = "C:/Users/oheya/AppData/Roaming/.minecraft/assets/virtual/legacy/sounds/"
    elif folder == "smash":
        mainFolder = "A:/Music/Super Smash Bros. Ultimate OST"
    elif folder == "undertale":
        mainFolder = "B:/Undertale"
    elif folder == "liked":
        return(getColBasedOnName(userName))

    else:
        for innerFolder in listdir("A:/Music/Super Smash Bros. Ultimate OST/"):

            exists = re.search(folder.lower(), innerFolder.lower())
            if type(exists) != type(None):
                mainFolder = "A:/Music/Super Smash Bros. Ultimate OST/" + innerFolder
            
    


    global toPlay
    toPlay = []
    global names
    names = []
    global pickedSong

    getAllFiles(mainFolder)
    print(specificSong)
    try:
        print(specificSong[0])
        pickSpecificSong(specificSong.lower())
    except IndexError:
        pickSong()
    

    print(pickedSong)
    return pickedSong

def getAllFiles(currPath):
    global toPlay
    global names
    for folder in listdir(currPath):
        newPath = (currPath + "/" + folder)
        if isfile(newPath):
            toPlay.append(newPath)
            names.append(folder)
        else:
            getAllFiles(newPath)

def pickSong():
    global toPlay
    global names
    global pickedSong
    num = random.randint(0, (len(names)-1))
    if names[num].endswith(".mp3") or names[num].endswith(".ogg"):
        pickedSong = [toPlay[num], names[num]]
    else: 
        pickSong()



def pickSpecificSong(specificSong):
    global pickedSong
    for song in names:
        exists = re.search(specificSong.lower(), song.lower())
        if type(exists) != type(None) and (song.endswith(".mp3") or song.endswith(".ogg")):
            pickedSong = [toPlay[names.index(song)], song]
        

skip = 0
queue = []
playing = False
@bot.command()
async def streamSongs(ctx, folder, specificSong=""):
    global skip
    global logOut
    global playing
    global queue
    channel = ctx.message.author.voice.channel
    userName = ctx.author.name
    if playing == False:
        vc = await channel.connect()
        playing = True
        firstTime = 1
        lastTime = 1
        #while done < int(times) and logOut == 0:
        queue.append(playAll(folder, specificSong, userName))
        while len(queue) > 0:
            song = queue[0]
            if firstTime:
                message = await ctx.send("now playing: " + song[1])
                #u2B1B
                await message.add_reaction("\u2B1B")
                firstTime = 0

            else: 
                await message.edit(content="now playing: " + song[1])
            vc.play(discord.FFmpegPCMAudio(song[0]), after=lambda e: print('done', e))

            while vc.is_playing() and logOut == 0:
                print(vc.is_playing())
                print(queue)
                message = await message.channel.fetch_message(message.id)
                a = message.reactions[0]
                reactionAmount = a.count
            
                if not reactionAmount == lastTime:
                    skip = 1
                lastTime = reactionAmount
                if skip == 1:
                    
                    vc.stop()
                    queue.remove(song)
                    print("queue after deletion is: ")
                    print(queue)
                    skip = 0
                    continue
                await asyncio.sleep(1)
            if song in queue:
                vc.stop()
                queue.remove(song)
                print("queue after deletion is: ")
                print(queue)
        await vc.disconnect()
        playing = False
        logOut = 0
    else:
        song = playAll(folder, specificSong, userName)
        queue.append(song)
        await ctx.send("added " + song[1] + " to the queue")
        

@bot.command()
async def qui(ctx):
    global queue
    toPrint = ""
    for song in queue:
        toPrint += (song[1] + "\n")
    await ctx.send("```queue is:```")
    await ctx.send(toPrint)

@bot.command()
async def skip(ctx):
    global skip
    skip = 1

@bot.command()
async def listSongs(ctx, folder):
    message = [""]
    if folder == "minecraft":
        mainFolder = "C:/Users/oheya/AppData/Roaming/.minecraft/assets/virtual/legacy/sounds/"
    elif folder == "smash":
        mainFolder = "A:/Music/Super Smash Bros. Ultimate OST"
    elif folder == "undertale":
        mainFolder = "B:/Undertale"
    else:
        for innerFolder in listdir("A:/Music/Super Smash Bros. Ultimate OST/"):

            exists = re.search(folder.lower(), innerFolder.lower())
            print(exists)
            if type(exists) != type(None):
                mainFolder = "A:/Music/Super Smash Bros. Ultimate OST/" + innerFolder
            else:
                print("no matching folders")
    n = 0

    for file in listdir(mainFolder):
        if len(message[n]) <= 1900:
            message[n] += (file + "\n")
        else:
            n += 1
            message.append(file + "\n")
    await ctx.send("songs in folder " + mainFolder + " :")
    for text in message:
        await ctx.send(text)

#@bot.command()
#async def spam(ctx):
#    while True:
#        await ctx.send(".bruh")

@bot.command()
async def me(ctx):
    msg = await ctx.send(ctx.author)
    print(ctx.author)




#A:/cool XD stuff that i make/shitstuff/very very bad photos/blueheart.png
#@bot.command()
#async def sauce(ctx):
#    print(ctx.author.name)
#    if ctx.author.name != "MarShesh":
#        im = ImageGrab.grab()
#        im.save("meow.png")
#        await ctx.send(file=discord.File(fp="A:/Code/python/Discord Bot/meow.png"))
#    else:
#        await ctx.send("no")


# 0 = playing, 1 = winning, 2 = losing
currentState = 0
#amount of letters in word
letters = 0
#how many letters were guessed, when guessedLetters == letters, you win
guessedLetters = 0
#the original word
listedWord = []
#what is to be printed
printedWord = []
wrongLetters = []
#amount of current lives, starts at 5, when reaches 0 you lose
lives = 5
firstTime = 1
@bot.command()
async def hangman(ctx, *input):
    try:
        input1 = input[0]
    except IndexError:
        await ctx.send(emojif("in order to begin do") + "```>hangman {number of lives}```" + emojif("and then to guess a letter do") + "```>hangman {letter you want to guess}```")
        return()
    global word
    global firstTime
    global lives
    global printedWord
    global listedWord
    global guessedLetters
    global letters
    global wrongLetters
    global currentState
    
    if firstTime == 1:
        firstTime = 0 
        #get word from long list
        with open('A:/Code/python/hangman lists/nations.txt', 'r+') as reading:
            colorList = reading.read()
            color = colorList.split("\n")
            a = random.randint(0, len(color))
            word = (color[a])
            reading.close()
        #turn word into list
        for letter in word:
            listedWord.append(letter.lower())
            if letter == " ":
                printedWord.append("  ")
            else:
                letters += 1
                printedWord.append("-")
        lives = int(input1)
        toSend = ""
        for item in printedWord:
            toSend += (item + " ")
        await ctx.send("**" + toSend + "     " + int(lives) * "\U0001F496" + "**")

    else:

        #the loop of guessing letters
        takenLetter = input1
        TorF = 0
        for item in listedWord:
            if takenLetter == item:
                TorF = 1
            else:
                if TorF == 0:
                    TorF = 0

        if TorF == 1:
            for item in listedWord:
                if item == takenLetter:
                    printedWord[listedWord.index(item)] = takenLetter
                    listedWord[listedWord.index(item)] = "+"
                    guessedLetters += 1
        else:
            lives -= 1
            wrongLetters.append(takenLetter)
            toPrint = ""
            
        toPrint = ""
        for item in printedWord:
            toPrint += (item + " ")


        toPrint += ("     " + int(lives) * "\U0001F496")
        await ctx.send("*" + toPrint + "*")

        #\U0001F496
        if letters == guessedLetters:
            currentState = 1
        if lives == 0:
            currentState = 2
        
        #endgame messages      
        if currentState == 1:
            await ctx.send(emojif("you won"))
        if currentState == 2: 
            await ctx.send(emojif("you lost"))
            await ctx.send("**the word was: " + word + "**")
        if currentState == 1 or currentState == 2:
            # 0 = playing, 1 = winning, 2 = losing
            currentState = 0
            #amount of letters in word
            letters = 0
            #how many letters were guessed, when guessedLetters == letters, you win
            guessedLetters = 0
            #the original word
            listedWord = []
            #what is to be printed
            printedWord = []
            wrongLetters = []
            #amount of current lives, starts at 5, when reaches 0 you lose
            lives = 5
            firstTime = 1


@bot.command()
async def disconnect(ctx):
    global logOut
    logOut = 1


wb = xlwt.Workbook() 
wbr = open_workbook('favourites.xls')

class Sheets:

    sheetList = []
    objectList = []
    global wb
    global wbr
    def __init__(self, name):
        self.name = name
        self.sheet = wb.add_sheet(name)
        self.sheetList.append(self.sheet)
        self.objectList.append(self)
        self.currRow = 0
        self.bonus = 0
        self.justCreated = 0


    def makeReadable(self):
        self.sheetRead = wbr.sheet_by_name(self.name)

    
    def globalCategory(self, category):
        
        for sheet in self.sheetList:
            sheet.write(0,self.currRow,category)
        self.currRow += 1

    def addValue(self, row, col, value):
        print(row)
        print(col)
        print(value)
        self.sheet.write(row,col,value)

    def colCountCells(self, col):
        number_of_rows = self.sheetRead.nrows
        tempCount = -1
        for row in range(number_of_rows):
            if (self.sheetRead.cell(row,col).value) != "":
                tempCount += 1
        return(tempCount)

    def appendValue(self, category, value):
        self.sheet.write(self.colCountCells(category)+1+self.bonus,category,value)
        print("added")

    def checkExistance(self, col, value):
        answer = False
        number_of_rows = self.sheetRead.nrows
        for row in range(number_of_rows):
            if (self.sheetRead.cell(row,col).value) == value:
                answer = True
        return(answer)

    def addIfNew(self, col, value):
        if not self.checkExistance(col, value):
            self.appendValue(col, value)

    def checkIfNameTaken(self, name):
        for sheet in self.sheetList:
            if name == sheet.name:
                return(1)

    def returnAllInCol(self, col):
        number_of_rows = self.sheetRead.nrows
        toReturn = []
        for row in range(number_of_rows):
            toReturn.append(self.sheetRead.cell(row,col).value)
        return(toReturn)

    def __del__(self):
        print("deleted")
        



def refreshList():
    global wb
    global wbr
    
    # Workbook is created
    wb = xlwt.Workbook() 
    wbr = open_workbook('favourites.xls')

    for sheet in wbr.sheets():
        currSheet = Sheets(sheet.name)
        currSheet.makeReadable()
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        for row in range(number_of_rows):
            for col in range(number_of_columns):
                if (sheet.cell(row,col).value) != "":
                    currSheet.addValue(row, col, (sheet.cell(row,col).value))
    
    wb.save('favourites.xls')
    print("updated list")

def exceptionRefresh(sheetName, badRow):
    global wb
    global wbr
    print("doing exception refresh")
    # Workbook is created
    wb = xlwt.Workbook() 
    wbr = open_workbook('favourites.xls')
    
    lowerer = 0
    for sheet in wbr.sheets():
        currSheet = Sheets(sheet.name)
        currSheet.makeReadable()
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        if currSheet.name == sheetName:
            print("right sheet")
            for row in range(number_of_rows):
                if row != badRow:
                    print("good row")
                    for col in range(number_of_columns):
                        if (sheet.cell(row,col).value) != "":
                            currSheet.addValue(row-lowerer, col, (sheet.cell(row,col)).value)
                else:
                    print("bad row")
                    lowerer += 1
            
        else:
            for row in range(number_of_rows):
                for col in range(number_of_columns):
                    if (sheet.cell(row,col).value) != "":
                        currSheet.addValue(row, col, (sheet.cell(row,col).value))
    
    wb.save('favourites.xls')
    print("updated list")


@bot.command()
async def like(ctx, folder, specificName):
    refreshList()
    song = playAll(folder, specificName, "")
    addToList(song, ctx.author)
    await ctx.send("successfully liked " + song[1])
    

def addToList(valueList, userName):
    global wb
    exists = 0
    if Sheets.objectList[0].checkIfNameTaken(userName.name):
        print("taken")
        
        for sheet in Sheets.objectList:
            if sheet.justCreated == 1 and sheet.name == userName.name:
                print("adding")
                print(valueList)
                print(3+sheet.bonus)
                sheet.sheet.write(sheet.bonus, 0, valueList[0])
                sheet.sheet.write(sheet.bonus, 1, valueList[1])
                sheet.bonus += 1
                exists = 1
        if exists == 0:
            for sheet in Sheets.objectList:
                if sheet.name == userName.name:
                    print(sheet.name + userName.name)
                    sheet.addIfNew(0, valueList[0])
                    sheet.addIfNew(1, valueList[1])
                    sheet.bonus += 1
                    print("appending")

    else:
        operationalSheet = Sheets(userName.name)
        operationalSheet.justCreated = 1
        operationalSheet.addValue(0, 0, valueList[0])
        operationalSheet.addValue(0, 1, valueList[1])
        print("making")
        operationalSheet.bonus += 1
    
    wb.save('favourites.xls') 
    print("updated list")
    Sheets.objectList.clear()

@bot.command()
async def printLiked(ctx):
    toSend = ""
    refreshList()
    userName = ctx.author
    for sheet in Sheets.objectList:
        if sheet.name == userName.name:
            for song in sheet.returnAllInCol(1):
                toSend += (song + "\n")
            await ctx.send(toSend)


    Sheets.objectList.clear()

def getColBasedOnName(name):
    refreshList()
    toReturn = []
    for sheet in Sheets.objectList:
        if sheet.name == name:
            paths = sheet.returnAllInCol(0)
            names = sheet.returnAllInCol(1)

    randomInList = (random.randint(0, (len(paths)-1)))
    toReturn.append(paths[randomInList])
    toReturn.append(names[randomInList])
    Sheets.objectList.clear()
    return(toReturn)
    
@bot.command()
async def removeLiked(ctx, song):
    refreshList()
    
    for sheet in Sheets.objectList:
        if sheet.name == ctx.author.name:
            paths = sheet.returnAllInCol(1)
    index = 0
    for item in paths:
        
        exists = re.search(song.lower(), item.lower())
        if type(exists) != type(None):
            Sheets.objectList.clear()
            exceptionRefresh(ctx.author.name, index)
        index += 1


    Sheets.objectList.clear()

bot.run('NTcyMjgwODA3OTYwMzQ2NjI1.XP0dcA.EXY-1DvG4OMXw5baEjLUmwW9hws')
#https://discordapp.com/oauth2/authorize?client_id=572280807960346625&scope=bot&permissions=8
