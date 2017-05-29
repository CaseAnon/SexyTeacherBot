import json

commands = {
    "version": "The bot is currently running on version 3. Code is open-sourced on https://github.com/caseanon/SexyTeacherBot. Thi
s bot was forked from ClaudiaMIND v0.1.3 - Special thanks to ClaudiaD and leet. https://github.com/ClaudiaDAnon/Hive",
    "goldmine": "Get your computer sk1llz improved with these amazing courses! -> download -> www.ghostbin.com/paste/wsyuc or www.
github.com/caseanon/Dump || WATCH ONLINE http://handbookproject.github.io",
    "read": "Read before asking! Most problems can be solved by reading the actual output you are getting from the program. Just g
o ahead and read them so you can be one step ahead to solving the problem.",
    "browse": "Before asking a question be sure you have checked out all your resources to try to fix it, most of the times, answe
rs are just in Google",
    "ask": "Don't ask to ask, just ask!",
    "donate": "Case needs money for drugs. Be sure to drop your cash at 13gTWmA9X6KUswbrxBuf62nwLWLr5QjoXc. You are welcome.",
    "linux": "Linux?? Never heard of it. Oh, wait, you must mean GNU/Linux!"
}

whatof = {
    "Case": "Henry Dorsett Case is a low-level hustler in the underworld of Chiba City, Japan. Once a talented computer hacker, Ca
se was caught stealing from his employer. As punishment, Case's nervous system was damaged with a mycotoxin, leaving him unable to
 access the global computer network in cyberspace. Unemployable, addicted to drugs, and suicidal, Case desperately searches the Ch
iba black clinics for a miracle cure.",
    "luna": "When I admire the beauty of Luna, my soul expands in the worship of the creator.",
    "multithr3d": "May your htop stats be low and your beards grow long.",
    "anakin": "You were supposed to bring glory to the navy, not destroy it you faggot",
    "ClaudiaD": "Tearing apart people's souls since forever. She also rides a unicorn.", "niggers": "They smell.",
    "S1rLancelot": "Sir Lancelot du lac is a cold black hat hacker that would do anything to help his king, Arthur"
}


def read_file(filename):
    file = open(filename, "r")
    info = [a.split(' = ')[1].replace('"', '') for a in file.read().splitlines()]
    file.close()
    return info


def read_users(filename):
    file = open(filename, "r")
    info = [a for a in file.read().splitlines()]
    file.close()
    return info


descs = read_file("descriptions.txt")
cors = read_file("courses.txt")
titles = []
links = []

for c in cors:
    i = c.split(" -- ")
    titles.append(i[0])
    links.append(i[1])

courses = []
courses.extend([0] * 109)

for i in range(109):
    course = {"id": str(i), "title": titles[i] if i < len(titles) else "", "desc": descs[i] if i < len(descs) else "",
        "link": links[i] if i < len(links) else ""}
    courses[i] = course
    
conf = {"nick": "", "user": "", "pass": "", "real": "", "irc": "irc.anonops.com",
    "port": 6697, "chans": ["#learninghub", "#bots"], }

users = read_users("users.txt")

defs = {"h": "halp", "help": "halp", "rc": "random_course", "randomcourse": "random_course", "w": "welcome",
    "welcome": "welcome", "d": "desc", "desc": "desc", "wof": "whatof", "whatof": "whatof", "l": "link", "link": "link"}

helps = {
    "randomcourse": "This command will print a random course from the goldmine, in case you want to do one and can't decide",
    "goldmine": "This command will print the goldmine with the full list of courses. Most of them are extracted from pluralsight,
others are provided by anons.",
    "desc": "This command will provide a description on a given course. Usage: ?desc <coursenumber>. Eg: ?desc 1 - Courses go from
 0, 1, 2 and upwards. The course identifier can be found in the ?goldmine"
}

data = {"commands": commands, "courses": courses, "conf": conf, "users": users, "defs": defs, "whatof": whatof, "helps": helps, "admins": ["Case", "S1rLancelot", "Woz"]}

outfile = open("conf.json", "w")
json.dump(data, outfile)
