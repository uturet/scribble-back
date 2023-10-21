from app.app import app

users = {}

@app.sio.on('connect')
async def connect(sid, environ, auth):
    users[sid] = auth
    await app.sio.emit('join', {'sid': sid})

@app.sio.on('disconnect')
async def disconnect(sid):
    del users[sid]
    print(f'{sid}: disconnected')