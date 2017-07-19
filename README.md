SexyTeacherBot is an interactive bot used in educational irc channel's, in this case: #learninghub.
The main purpose of this bot is to write an easy to use interface as well a providing some dynamic, helpful and fun functionality.

The project consists of a global Bot object, which, with the help of sockets, provides basic irc bot functionality.
All other files, both main.py and conf.json are specific for #learninghub

For security purposes, conf.json is incomplete. Lacking both 'users' and 'conf'.

```HTML
<pre>
    <div class="container">
        <div class="block two first">
            <h2>Configuration format</h2>
            <div class="wrap">
                'users' should contain a list of SHA2 Hashes, which should be the registered nicks.
            </div>
        </div>
    </div>

    <div class="container">
        <div class="block two first">
            <h2>Configuration format</h2>
            <div class="wrap">
                'conf' = {
                    "irc": str(),       # IRC's address
                    "port": int(),      # IRC's port
                    "nick": str(),      # Bot's nick name
                    "user": str(),      # Bot's user name
                    "real": str(),      # Bot's real name
                    "pass": str()       # Bot's password
                    "chans": [str()],   # Channels bot should connect to, it will only answer in the first one
                }
            </div>
        </div>
    </div>
</pre>
```
