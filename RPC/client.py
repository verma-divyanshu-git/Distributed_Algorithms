from rpc import RPCClient

# Use 'localhost' or '127.0.0.1' for connecting to a local server
server = RPCClient("localhost", 6969)

server.connect()

print(server.add(5, 6))
print(server.sub(5, 6))

server.disconnect()
