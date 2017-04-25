#!/usr/bin/env python2
from Queue import Queue
import platform
import hashlib
import random
import thread
import string
import socket
import time
import ssl
import re

art = """
   _____              _______              _               ____        _
  / ____|            |__   __|            | |             |  _ \      | |
 | (___   _____  ___   _| | ___  __ _  ___| |__   ___ _ __| |_) | ___ | |_
  \___ \ / _ \ \/ / | | | |/ _ \/ _` |/ __| '_ \ / _ \ '__|  _ < / _ \| __|
  ____) |  __/>  <| |_| | |  __/ (_| | (__| | | |  __/ |  | |_) | (_) | |_
 |_____/ \___/_/\_\\__, |_|\___|\__,_|\___|_| |_|\___|_|  |____/ \___/ \__|
                    __/ |
                   |___/
                                  Special thanks to ClaudiaD & leet
"""

# Config
config = {}
execfile("configuration.conf", config)
version = "This bot was forked from ClaudiaMIND v0.1.3 - Special thanks to ClaudiaD and leet. https://github.com/ClaudiaDAnon/Hive"

# Courses
coursefile = "courses.txt"
descriptionsfile = "descriptions.txt"
courses = {}
descriptions = {}
execfile(coursefile, courses)
execfile(descriptionsfile, descriptions)

nickname = "SexyTeacherBot"
username = ""
realname = nickname
password = ""

ircd = config["ircd"]
ircport = config["ircport"]
admins = config["admins"]
channel = config["channel"]

# Message-sending
def message(msg):
    s.send("PRIVMSG " + channel + " :" + msg + "\r\n")

# Private-Messaging
def privmessage(user2, msg):
    s.send(":source PRIVMSG " + user2 + " :" + msg + "\r\n")

# Get file length
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# Take input from terminal
def take_input(chan, s):
    while 1:
        data = raw_input()
        send_data = (":source PRIVMSG " + channel + " :" + data + "\r\n")
        s.send(send_data)

def isWindows():
    return platform.system() == "Windows"

def isNewUser(user):
    userfile = open("users.txt","r")
    previous = []
    for line in userfile:
        line = line.strip('\r\n')
        line = line.strip('\n')
        previous += [line]
    userfile.close()
    return sha2(user) not in previous

def saveuser(user):
    save = open("users.txt","a")
    save.write(sha2(user) + "\n")
    save.close()

#Better way to not repeat the same thing over and over
def switch(terms):
    for term in terms:
        if term == sentmessage:
            return True
    return False

#Save usernames in SHA-256
def sha2(text):
    return hashlib.sha256(text).hexdigest()

def pingpong(msg):
    number = msg.strip("PING :")
    pong = "PONG :" + number
    s.send(pong)

def getNick(recvd):
    try:
        return recvd.split("!")[1].split("@")[0]
    except:
        return None

def rest():
    try:
        if ("?" == sentmessage[0]) or ("what" == sentmessage[:4]):
            time.sleep(1)
    except:
        pass

# Aesthetics
if isWindows():
    class bcolors:
        HEADER = ''
        OKBLUE = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''
else:
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

print(bcolors.OKBLUE + art + bcolors.ENDC)
time.sleep(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print(bcolors.OKBLUE + "Establishing connection to IRC:" + str(ircd) + "/" + str(ircport) + bcolors.ENDC)
    s.connect((ircd, ircport))
    s.settimeout(130)
    s = ssl.wrap_socket(s)
    print(bcolors.OKGREEN + "Connection established!" + bcolors.ENDC)
except Exception as e:
    print(bcolors.FAIL + "Failed to connect. [" + str(ircport) + "]" + bcolors.ENDC)
    print(e)
    exit()

print(bcolors.OKBLUE + "Sending credentials. Bot nickname: " + nickname + bcolors.ENDC)
s.send("PASS " + password + "\r\n")
s.send("NICK " + nickname + "\r\n")
s.send("USER " + username + " 0 * :" + realname + "\r\n")
print(bcolors.OKBLUE + "Credentials sent. Waiting for log-in..." + bcolors.ENDC)

# Wait for ping from server
while True:
    recvd = s.recv(4096)

    if recvd == "":
        exit(0)
    elif "PING :" in recvd:
        pingpong(recvd)
    elif (nickname + "!" + username) in recvd:
        break

print bcolors.OKBLUE + "[+] Joining channel: " + channel + bcolors.ENDC
s.send(":source PRIVMSG nickserv :IDENTIFY "+ password + "\r\n")
s.send(":source JOIN :" + "#bots" + "\r\n")
s.send(":source JOIN :" + channel + "\r\n")
s.send(":source MODE " + nickname + " +B \r\n")

# Loop to receive input and execute commands
q = Queue()
thread.start_new_thread(take_input, (channel,s,))

while True:
    recvd = s.recv(1024)
    msg = string.split(recvd)[3:] #WHY
    sentmessage = " ".join(msg)[1:].lower()
    senderuser = recvd.split("!")[0][1:]
    # Quits the program before it bugging
    if recvd == "":
        exit(0)

    if "PING :" in recvd:
        pingpong(recvd)
    else:
        print bcolors.OKBLUE + "<" + senderuser + "> " + bcolors.ENDC + sentmessage

    # TODO: implement a white input list
    if ("JOIN :" + channel in recvd) and isNewUser(senderuser):
      message("Welcome to #learninghub " + senderuser + "! Here you'll find lots of resources and people to learn hacking/pentesting as well as other IT subjects. Type ?goldmine to get started. Type ?desc <coursenumber> to know the description of a course. You have to use the course number in the ghostbin. Type ?help for more.")
      saveuser(senderuser)
    elif switch(["?rc","?randomcourse"]):
      rand = random.randint(1,len(courses))
      message(courses["c" + str(rand)])
    elif switch(["?gm","?goldmine"]):
      message("Get your computer sk1llz improved with these amazing courses! -> download -> www.ghostbin.com/paste/j858d or www.github.com/caseanon/Dump || WATCH ONLINE http://handbookproject.github.io")
    elif switch(["?cotw","?courseoftheweek"]):
      message(courses[checkCourse(1)])
    elif "?desc" == sentmessage[:5]:
        try:
            course = sentmessage[6:]
            message(descriptions["c" + course])
        except Exception as e:
            message("Input a valid course faggot")
            print(e)
    elif switch(["?v","?version"]):
        message(version)
    elif switch(["?h","?help","?halp"]):
        message("Available commands: ?courseoftheweek, ?desc, ?randomcourse, ?goldmine, ?version, ?help, ?welcome. Shorts work too: ?cotw, ?rc, ?gm, etc. Do ?help <fullcommandname> to know more. Eg: ?help desc")
    elif switch(["?w","?welcome"]):
        message("Welcome to #learninghub! Here you'll find lots of resources and people to learn hacking/pentesting as well as other IT subjects. Type ?goldmine to get started. Type ?desc <coursenumber> to know the description of a course. You have to use the course number in the ghostbin. Type ?help for more.")
    elif switch(["?h desc","?help desc"]):
        message("This command will provide a description on a given course. Usage: ?desc <coursenumber>. Eg: ?desc 1 - Courses go from 0, 1, 2 and upwards. The course identifier can be found in the ?goldmine")
    elif switch(["what of case"]):
        message("Henry Dorsett Case is a low-level hustler in the underworld of Chiba City, Japan. Once a talented computer hacker, Case was caught stealing from his employer. As punishment, Case's nervous system was damaged with a mycotoxin, leaving him unable to access the global computer network in cyberspace. Unemployable, addicted to drugs, and suicidal, Case desperately searches the Chiba black clinics for a miracle cure.")
    elif switch(["?try","what of try"]):
        message("Do or Do not. There is no try.")
    elif switch(["?luna"]):
        message("When I admire the beauty of Luna, my soul expands in the worship of the creator.")
    elif switch(["?multithr3d","what of multithr3d"]):
        message("May your htop stats be low and your beards grow long.")
    elif switch(["what of luna"]):
        message("Luna is the way, Luna is the light. She's one of a kind, a sight for sore eyes.")
    elif switch(["?anakin","what of anakin"]):
        message("You were supposed to bring glory to the navy, not destroy it you faggot")
    elif switch(["?claudiad","what of claudiad"]):
        message("Tearing apart people's souls since forever. She also rides a unicorn.")
    elif switch(["?niggers","what of niggers"]):
        message("They smell.")
    elif switch(["?h courseoftheweek","?help courseoftheweek"]):
        message("This command will print the course decided for the week. Join us :)")
    elif switch(["?h randomcourse","?help randomcourse"]):
        message("This command will print a random course from the goldmine, in case you want to do one and can't decide")
    elif switch(["?h goldmine","?help goldmine"]):
        message("This command will print the goldmine with the full list of courses. Most of them are extracted from pluralsight, others are provided by anons.")
    if senderuser in admins:
        if switch(["?updatecourselist"]):
            courses = {}
            descriptions = {}
            execfile(coursefile, courses)
            execfile(descriptionsfile, descriptions)
