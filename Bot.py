import hashlib
import socket
import ssl

class Bot:
    def __init__(self, data):
        self.data = data
        self.conf = data["conf"]
        self.s = None
        self.connect()

    @staticmethod
    def sha2(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((self.conf["irc"], self.conf["port"]))
            s.settimeout(130)
            self.s = ssl.wrap_socket(s)
        except Exception as e:
            print("Failed to connect. %s:%d" % (self.conf["irc"], self.conf["port"]))
            print(e)
            exit()

    def _send(self, msg):
        self.s.send(msg.encode())

    def message(self, msg, chan):
        self._send("PRIVMSG %s :%s\r\n" % (chan, msg))

    def notice(self, user, msg):
        self._send("NOTICE %s :%s\r\n" % (user, msg))

    def auth(self):
        print("[+] Sending credentials for %s" % self.conf["nick"])
        self._send("PASS %s\r\n" % self.conf["pass"])
        self._send("NICK %s\r\n" % self.conf["nick"])
        self._send("USER %s 0 * :%s\r\n" % (self.conf["user"], self.conf["real"]))
        print("[+] Credentials send. Waiting for authentication.")

    def ping(self):
        while True:
            try:
                recvd = self.s.recv(4096).decode()

                if "PING" in recvd:
                    self.pong(recvd)
                elif "%s!%s" % (self.conf["nick"], self.conf["user"]) in recvd:
                    break

            except socket.timeout:
                raise("[-] Error: ", socket.timeout)

    def pong(self, msg):
        num = msg.strip("PING :")
        self._send("PONG :%s" % num)
        
    def join(self):
        print("[+] Joining channels.\n")
        self._send(":source PRIVMSG nickserv :IDENTIFY %s\r\n" % self.conf["pass"])

        for x in self.conf["chans"]:
            self._send(":source JOIN :%s\r\n" % x)

        self._send(":source MODE %s +B \r\n" % self.conf["nick"])

    def listen(self):
        try:
            recvd = self.s.recv(1024).decode()
        except socket.timeout:
            print("[-] Error: Socket timeout.")
            return self.listen()

        info = recvd.split()[3:]
        msg = " ".join(info)[1:]
        nick = recvd.split("!")[0][1:]
        chan = recvd.split()[2] if "PRIVMSG #" in recvd else None

        if "PING" in recvd:
            self.pong(recvd)
        elif "JOIN" in recvd and self.sha2(nick) not in self.data["users"]:
            msg = "?welcome"
        elif " " not in nick:
            print("<%s> %s" % (nick, msg))

        return nick, msg, chan
        
