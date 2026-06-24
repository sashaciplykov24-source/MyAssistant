from modules.dispatcher import dispatch

command = {
    "command": "open_program",
    "program": "/data/history.json"
}

print(dispatch(command))