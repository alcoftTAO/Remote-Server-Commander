import websockets
import sys
import os
import base64
import asyncio
import json

ServerPassword: str = ""
PasswordRequired: bool = True
Commands: dict[str, str] = {}
ServerSocket: websockets.WebSocketServerProtocol = None

async def ProcessClient(Client: websockets.WebSocketClientProtocol) -> None:
    while (True):
        try:
            received = await Client.recv()

            if (len(received) == 0):
                print("Got empty response, closing connection...")
                Client.close()
            
            if (type(received) == bytes):
                received = base64.b64decode(received).decode("utf-8")
            elif (type(received) == str):
                received = base64.b64decode(received.encode("utf-8")).decode("utf-8")
            else:
                print("Unrecognized response type.")
            
            received = json.loads(received)
            cmd = received["Cmd"]
            password = received["Password"]
            failcode = 0

            if (password != ServerPassword or list(Commands.keys()).count(cmd) == 0):
                if (list(Commands.keys()).count(cmd) == 0):
                    failcode = 1
                else:
                    failcode = 2

                await Client.send(base64.b64encode(("FAIL " + str(failcode)).encode("utf-8")).decode("utf-8"))
                continue

            os.system(Commands[cmd])
            await Client.send(base64.b64encode("OK".encode("utf-8")).decode("utf-8"))
        except Exception as ex:
            print("Error! Could not process the client (details: " + str(ex) + "). Closing connection...")
            await Client.close()
            Client = None

            break

async def ManageClient(ClientSocket: websockets.WebSocketClientProtocol) -> None:
    print("Incomming connection of '" + ClientSocket.remote_address[0] + ":" + str(ClientSocket.remote_address[1]) + "'...")
    await ProcessClient(ClientSocket)

async def StartServer() -> None:
    global ServerSocket

    ServerSocket = await websockets.serve(ManageClient, "0.0.0.0", 19380)
    print("Server started on port 19380.")

try:
    for arg in sys.argv:
        if (sys.argv.index(arg) == 0):
            continue

        if (arg.startswith("pwd=")):
            ServerPassword = arg[4:]
        elif (arg.startswith("cmds=")):
            Commands = json.loads(arg[5:])
        elif (arg == "allowNoPassword"):
            PasswordRequired = False
        elif (arg == "help"):
            print("Syntax:\n   Server.py [args]")
            print("\nArgs:\n")
            print("   pwd=[PASSWORD] - Password of the server (REQUIRED UNLESS YOU USE THE `allowNoPassword` ARG).")
            print("   cmds=[JSON] - Commands of the server.")
            print("   allowNoPassword - Allows the clients to access the server without a password (NOT RECOMMENDED).")

            os._exit(0)
        else:
            print("Unrecognized arg. Ignoring.")

    if (len(ServerPassword.strip()) == 0 and PasswordRequired):
        raise Exception("Error! Server password is null! Execute with 'allowNoPassword' to ignore this.")
    
    loop = asyncio.new_event_loop()

    loop.run_until_complete(StartServer())
    loop.run_forever()
except KeyboardInterrupt:
    print("\nClosing server...")

    ServerSocket = None
    os._exit(0)
except Exception as ex:
    print("Fatal error! Details: " + str(ex))
    os._exit(1)