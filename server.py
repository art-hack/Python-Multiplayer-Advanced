import socket
from _thread import *
import pickle
from game import Game

server = "172.22.45.173"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    pass

s.listen(20)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def thread_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break
    print("Lost connection")

    try:
        del games[gameId]
        print("Closing game" + str(gameId))
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("connected to: ", str(addr))

    idCount += 1
    p = 0
    gameId = (idCount-1)//2
    if idCount % 2 ==1:
        games[gameId] = Game(gameId)
        print("Creating A New Game")
    else:
        games[gameId].ready = True
        p = 1
    start_new_thread(thread_client, (conn, p, gameId))
