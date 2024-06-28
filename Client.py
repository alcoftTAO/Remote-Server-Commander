import websockets
import sys
import os
import base64
import asyncio
import json
import traceback

Ip: str = ""
Password: str = ""
UseTerminal: bool = False
Command: str = ""
CSocket: websockets.WebSocketClientProtocol = None

async def ConnectToServer() -> bool:
    global CSocket
    CSocket = None

    try:
        CSocket = await websockets.connect("ws://" + Ip + ":19380")
        return True
    except Exception as ex:
        print("Error! Could not connect to the server (details: " + str(ex) + ").")
        traceback.print_exc()
        
        return False

async def SendCommand(Cmd: str) -> str | int:
    if (CSocket == None):
        raise Exception("Connect to a server first!")
    
    if (len(Cmd.strip()) == 0):
        raise Exception("Command is empty!")
    
    try:
        await CSocket.send(base64.b64encode(json.dumps({"Password": Password, "Cmd": Cmd.strip()}).encode("utf-8")).decode("utf-8"))
        received = base64.b64decode(await CSocket.recv()).decode("utf-8")

        if (received == "OK"):
            return 0
        elif (received.startswith("FAIL")):
            failcode = int(received[4:].strip())
            return failcode
        else:
            return received
    except Exception as ex:
        print("Error! Could not send or receive the command or the server response (details: " + str(ex) + ").")
        return -1
    
async def ProcessResponse() -> None:
    response = await SendCommand(Command)

    if (type(response) == int):
        if (response == 0):
            print("Command executed successfully OwO.")
        else:
            failmsg = ""

            if (response == -1):
                failmsg = "Unknown error"
            elif (response == 1):
                failmsg = "The command doesn't exists"
            elif (response == 2):
                failmsg = "The password is incorrect"

            print("Command failed to execute. Fail code: " + str(response) + ("" if (len(failmsg) == 0) else " (" + failmsg + ")."))
    else:
        if (type(response) != str):
            response = str(response)
        
        print("Server response: " + response)

for arg in sys.argv:
    if (sys.argv.index(arg) == 0):
        continue

    if (arg.startswith("ip=")):
        Ip = arg[3:]
    elif (arg.startswith("cmd=")):
        Command = arg[4:]
    elif (arg == "term" or arg == "terminal" or arg == "console"):
        UseTerminal = True
    elif (arg.startswith("pwd=")):
        Password = arg[4:]
    elif (arg == "help"):
        print("Syntax:\n   Client.py [args]")
        print("\nArgs:\n")
        print("   ip=[SERVER IP] - Set the IP of a server (REQUIRED).")
        print("   pwd=[PASSWORD] - Password to access the server (REQUIRED).")
        print("   cmd=[COMMAND] - Execute a command on the server (REQUIRED UNLESS YOU USE THE `terminal` ARG).")
        print("   terminal - Use a terminal to type multiple commands.")

        os._exit(0)
    else:
        cont = input("Unrecognized arg `" + arg + "`. Continue? [Y/n] ").strip().lower()

        if (cont == "n" or cont == "no"):
            print("   Connection cancelled.")
            os._exit(1)

if (len(Ip) == 0 or len(Password) == 0 or (len(Command) == 0 and not UseTerminal)):
    raise Exception("Error! A required arg is empty. Please check the args.")

loop = asyncio.new_event_loop()
connection = loop.run_until_complete(ConnectToServer())

while (not connection):
    if (UseTerminal):
        reconnect = input("Error connecting to the server. Please check the IP. Try again? [Y/n] ").lower().strip()

        if (reconnect == "n" or reconnect == "no"):
            os._exit(3)
        else:
            connection = loop.run_until_complete(ConnectToServer())
    else:
        print("Error connecting to the server. Please check the IP.")
        os._exit(3)

if (UseTerminal):
    print("Type `exit` to close the terminal.")

    while (True):
        Command = input(Ip + " $ UwU > ").strip()

        if (Command == "exit"):
            CSocket = None
            os._exit(0)
        elif (Command.startswith("-os ")):
            Command = Command[4:]
            os.system(Command)

            continue

        loop.run_until_complete(ProcessResponse())
else:
    loop.run_until_complete(ProcessResponse())