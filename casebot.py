#!/usr/bin/env python2
import platform
import re
import requests
import argparse
#import socks
import socket
import ssl
import time
import random
import thread
import threading
import string
from Queue import Queue

# Function def

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

# Returns whether given user has access rights
def isAdmin(user):
    return (senderuser == botmaster) or (senderuser == masterbot) or (senderuser in admins)

# Take input from terminal
def take_input(chan, s):
    while 1:
        data = raw_input()
        send_data = (":source PRIVMSG " + channel + " :" + data + "\r\n")
        s.send(send_data)

def isWindows():
    return platform.system() == "Windows"

def isNewUser(user):
    # Top secret

def saveuser(user):
    # Top secret


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

global port
port = None


# Config
config = {}
execfile("configuration.conf", config)
version = "This bot was forked from ClaudiaMIND v0.1.3 - Special thanks to ClaudiaD and leet. https://github.com/ClaudiaDAnon/Hive"

# Courses
coursefile = "courses.txt"
descriptionsfile = "descriptions.txt"
courseoftheweek = config["cotw"]
courseoftheday = "c0"
courses = {}
descriptions = {}
execfile(coursefile, courses)
execfile(descriptionsfile, descriptions)

# Argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("--port", "-p",
#                    help="SOCKS5 port")
#args = parser.parse_args()

# Program start
print(bcolors.OKBLUE + art + bcolors.ENDC)
time.sleep(1)

#sport = args.port if args.port else raw_input("SOCKS5 port (def. 9050): ")
#if sport == "":
#    sport = 9050
#else:
#    sport = int(sport)
#native_ip = "0"
#if native_ip == "0":
#    print(bcolors.WARNING + "You might want to set your native IP inside the file in order to make this process shorter." + bcolors.ENDC)
#    time.sleep(2)
#native_ip = requests.get("http://canihazip.com/s").text
#print("Your native IP: " + native_ip)
# Tor
# TODO: Allow tor argument
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", sport, True)
#socket.socket = socks.socksocket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP = requests.get("http://canihazip.com/s").text
#if IP == native_ip:
#    IP = 0
#    print(bcolors.FAIL + "Detected IP leaks." + bcolors.ENDC)
#    time.sleep(2)
#else:
#    print(bcolors.OKGREEN + "No IP leaks detected." + bcolors.ENDC)
#    time.sleep(1)
#print(bcolors.OKBLUE + "IP: " + IP + bcolors.ENDC)

# Setting nicknames and realnames
nickname = "SexyTeacherBot" # SET THIS VALUE TO BE THE BOT NICKNAME
username = "G3nn1"
realname = nickname
password = ""
ircd = config["ircd"]
ircport = config["ircport"]
sport = ircport # TODO: adapt for tor

botmaster = config["botmaster"]
masterbot = config["masterbot"]
admins = config["admins"]

channel = config["channel"]

try:
    print(bcolors.OKBLUE + "Establishing connection to IRC:" + str(ircd) + "/" + str(ircport) + bcolors.ENDC)
    s.connect((ircd, ircport))
    s = ssl.wrap_socket(s)
    print(bcolors.OKGREEN + "Connection established!" + bcolors.ENDC)

except Exception as e:
    print(bcolors.FAIL + "Failed to connect. [" + str(sport) + "]" + bcolors.ENDC)
    print(e)
    exit()

print(bcolors.OKBLUE + "Sending credentials. Bot nickname: " + nickname + bcolors.ENDC)
s.send("PASS " + password + "\r\n")
s.send("NICK " + nickname + "\r\n")
s.send("USER " + username + " 0 * :" + realname + "\r\n")
print(bcolors.OKBLUE + "Credentials sent. Waiting for log-in..." + bcolors.ENDC)

# Wait for ping from server
connected = 0
while connected == 0:
    recvd = s.recv(4096)
    if "PING :" in recvd:
        recvd = recvd.strip("PING :")
        pong = "PONG :" + recvd
        s.send(pong)

    if nickname + "!" + username in recvd:
        connected = 1

# Message the authorities and join channel
#s.send("PRIVMSG " + botmaster + " :" + IP + " @" + version + "\r\n") # sends only your Tor IP
#s.send("PRIVMSG " + masterbot + " :" + IP + " @" + version + "\r\n")
#for admin in admins:
#    s.send("PRIVMSG " + admin + " :" + IP + " @" + version + "\r\n")
#time.sleep(2)

print(bcolors.OKBLUE + "Joining channel: " + channel + bcolors.ENDC)
s.send(":source PRIVMSG nickserv :IDENTIFY "+ password + "\r\n")
s.send(":source JOIN :" + "#bots" + "\r\n")
s.send(":source JOIN :" + channel + "\r\n")
s.send(":source MODE SexyTeacherBot +B \r\n")

# Loop to receive input and execute commands
q = Queue()
thread.start_new_thread(take_input, (channel,s,))

free_for_all = 1 # Freemode on, everyone can issue commands
allowed = 0

while 1:
    recvd = s.recv(1024)
    msg = string.split(recvd)[3:]
    sentmessage = " ".join(msg)[1:]

    #userfinding
    recvdfix = recvd.strip("\r\n")
    senderuser = recvdfix.split(" ")
    senderuser = senderuser[0].split("!")
    senderuser = senderuser[0].strip(":")

    if recvd == "":
        exit(); #Hope this works

    if "PING :" in recvd:
        recvd = recvd.strip("PING :")
        pong = "PONG : " + recvd
        s.send(pong)
    else:
        print bcolors.OKBLUE + "<" + senderuser + "> " + bcolors.ENDC + sentmessage
    if free_for_all == 1:
        allowed = 1

    sentmessage = sentmessage.lower()
    # execute any commands detected from authorised people
    if allowed == 1:#TODO remove this and leave validation only for ?command
    	if "JOIN :#learninghub" in recvd:
    	    if isNewUser(senderuser):
                  message("Welcome to #learninghub " + senderuser + "! Here you'll find lots of resources and people to learn hacking/pentesting as well as other IT subjects. Type ?goldmine to get started. Type ?desc <coursenumber> to know the description of a course. You have to use the course number in the ghostbin. Type ?help for more.")
                  saveuser(senderuser)
        if ("?randomcourse" == sentmessage) or ("?rc" == sentmessage):
          time.sleep(1)
          rand = int(random.random() * file_len(coursefile))
          message(courses["c"+str(rand)])
        if ("?goldmine" == sentmessage) or ("?gm" == sentmessage):
          time.sleep(1)
          message("Get your computer skillz improved with these amazing courses! ->  ONLINE: http://handbookproject.github.io DOWNLOAD: www.ghostbin.com/paste/t7nyv || www.github.com/caseanon/Dump")
        if ("?courseoftheweek" == sentmessage) or ("?cotw" == sentmessage):
          time.sleep(1)
          message(courses[courseoftheweek])
        if ("?courseoftheday" == sentmessage) or ("?cotd" == sentmessage):
          time.sleep(1)
          message(courses[courseoftheday])
        if "?desc " in sentmessage:
              try:
                time.sleep(1)
                course = sentmessage.replace("?desc ", "")
                message(descriptions["c" + course])
              except Exception as e:
                message("Input a valid course faggot")
                print(e)
        if ("?version" == sentmessage) or ("?v" == sentmessage):
            time.sleep(1)
            message(version)
        if ("?help" == sentmessage) or ("?halp" == sentmessage) or ("?h" == sentmessage):
            time.sleep(1)
            message("Available commands: ?courseoftheweek, ?desc, ?courseoftheday, ?randomcourse, ?goldmine, ?version, ?help, ?welcome. Shorts work too: ?cotw, ?rc, ?gm, etc. Do ?help <fullcommandname> to know more. Eg: ?help desc")
        if ("?welcome" == sentmessage) or ("?w" == sentmessage):
            time.sleep(1)
            message("Welcome to #learninghub! Here you'll find lots of resources and people to learn hacking/pentesting as well as other IT subjects. Type ?goldmine to get started. Type ?desc <coursenumber> to know the description of a course. You have to use the course number in the ghostbin. Type ?help for more.")
        if ("?help desc" == sentmessage) or ("?h desc" == sentmessage):
            time.sleep(1)
            message("This command will provide a description on a given course. Usage: ?desc <coursenumber>. Eg: ?desc 1 - Courses go from 0, 1, 2 and upwards. The course identifier can be found in the ?goldmine")
        if ("?help courseoftheweek" in sentmessage) or ("?h courseoftheweek" in sentmessage):
            time.sleep(1)
            message("This command will print the course decided for the week. Join us :)")
        if "?luna" == sentmessage:
            time.sleep(1)
            message("When I admire the beauty of Luna, my soul expands in the worship of the creator.")
        if "what of luna" == sentmessage:
            time.sleep(1)
            message("Luna is the way, Luna is the light. She's one of a kind, a sight for sore eyes.")
        if ("what of anakin" == sentmessage) or ("?anakin" == sentmessage):
            time.sleep(1)
            message("You were supposed to bring glory to the navy, not destroy it you faggot")
        if ("what of claudiad" == sentmessage) or ("?claudiad" == sentmessage):
            time.sleep(1)
            message("Tearing apart people's souls since forever. She also rides a unicorn.")
        if ("what of niggers" == sentmessage) or ("?niggers" == sentmessage):
            time.sleep(1)
            message("They smell.")
        if ("?help courseoftheday" in sentmessage) or ("?h courseoftheday" in sentmessage):
            time.sleep(1)
            message("This command will print the course decided for the day, for those hardcore enough to do one a day :)")
        if ("?help randomcourse" == sentmessage) or ("?h randomcourse" == sentmessage):
            time.sleep(1)
            message("This command will print a random course from the goldmine, in case you want to do one and can't decide")
        if ("?help goldmine" == sentmessage) or ("?h goldmine" == sentmessage):
            time.sleep(1)
            message("This command will print the goldmine with the full list of courses. Most of them are extracted from pluralsight, others are provided by anons.")
        if isAdmin(senderuser):
          if ("?setcotw " in sentmessage):
            time.sleep(1)
            courseoftheweek = sentmessage.replace("?setcotw ", "")
          if ("?setcotd " in sentmessage):
            time.sleep(1)
            courseoftheday = sentmessage.replace("?setcotd ", "")
          if ("?updatecourselist" == sentmessage):
            time.sleep(1)
            courses = {}
            descriptions = {}
            execfile(coursefile, courses)
            execfile(descriptionsfile, descriptions)
          if "?command" in sentmessage:
              try:
                commanddata = sentmessage.replace("?command ", "")
                result = re.findall(r'(.*?) (.*)', commanddata)
                if result[0][0] == nickname or "*":
                  s.send(result[0][1] + "\r\n")
              except Exception as e:
                print(bcolors.FAIL + "Incorrect ?command format." + bcolors.ENDC)
                message("Incorrect ?command format.")
                print(e)
