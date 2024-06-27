# Alcoft Remote Server Commander
This is a software that allows you to execute some root commands on a remote server, but without having full root access to the server.

## How to use
### Install dependencies
First of all, you need to install the dependencies for both client and server.
If you don't have access to the server, you may need to contact the person responsible of the server to start the program.

#### Install dependencies on Windows
1. Make sure you have Python and Git installed on your system (recommended Python 3.12).
2. Open a Microsoft PowerShell.
3. `cd` into the directory where you want so download this repository.
4. Execute:
```sh
git clone https://github.com/alcoftTAO/Remote-Server-Commander.git
cd Remote-Server-Commander
```

5. Download PIP for Python executing:
```sh
python -m ensurepip
```

6. Install the Python requirements executing:
```sh
python -m pip install -r requirements.txt
```

7. Done! You alredy installed the requirements.

#### Install dependencies on GNU/Linux
1. Make sure you have Python and Git installed on your system (recommended Python 3.12).
2. Open your favourite terminal.
3. `cd` into the directory where you want so download this repository.
4. Execute:
```sh
git clone https://github.com/alcoftTAO/Remote-Server-Commander.git
cd Remote-Server-Commander
```

5. Make sure you have pip installed. If you don't, install it using your package manager.
6. Install the Python requirements executing:
```sh
pip install -r requirements.txt
```

7. Done! You alredy installed the requirements.

> [!NOTE]
> If executing a `python [···]` command doesn't work, try executing `python3 [···]` or `py [···]`.

### Set the server
You need to execute the `Server.py` script on your server with root access.
If you want the server to automatically start, you can use `systemd`:
1. Create a systemd service:
```sh
sudo vim /etc/systemd/system/rsc.service
```

> [!NOTE]
> Replace `vim` with any other text editor that you like.

2. Write this in the new file:
```
[Unit]
Description=Remote Server Commander
After=network-online.target ufw.service

[Service]
Type=simple
WorkingDirectory=[DIR]
ExecStart=python Server.py [ARGS]

[Install]
WantedBy=multi-user.target
```

> [!NOTE]
> Replace `[DIR]` with the directory of the repository.
> Replace `[ARGS]` with the server args. If you don't know the args, enter the repository directory and execute `python Server.py help`.
> If you don't have `ufw` as your server's firewall, remove `ufw.service`.

3. Enable the service:
```sh
sudo systemctl daemon-reload
sudo systemctl enable rsc.service
```

4. Start the service:
```sh
sudo systemctl start rsc.service
```

5. Done!

### Connect to a server using the client
There are two ways to connect to execute a command on the server using the client.
1. One-time connection:
This connection can only execute 1 command, but might be faster.
To use this connection, execute:
```sh
python Client.py ip=[IP] pwd=[PASSWORD] cmd=[COMMAND]
```

> [!NOTE]
> Replace `[IP]` with the server IP.
> Replace `[PASSWORD]` with the server password.
> Replace `[COMMAND]` with the command you want to execute on the server. Make sure it's a valid command.

2. Terminal connection:
This connections creates a "terminal", where you can type as many commands as you want.
To use this connection, execute:
```sh
python Client.py ip=[IP] pwd=[PASSWORD] term
```

> [!NOTE]
> Replace `[IP]` with the server IP.
> Replace `[PASSWORD]` with the server password.
> When you are done executing commands, type `exit` on the terminal to close the program.

## License
MIT License.