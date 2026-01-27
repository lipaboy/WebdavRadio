import disk

client = disk.openClientSession()

def dir_list(f, path: str):
    items = client.list(path)
    for i in items:
        if '.' in i: #is file
            if i.endswith('.mp3'):
                f.write(path + '/' + i + '\n')
        elif i.endswith('/'): #dir
            dir=path + '/' + i[:-1]
            print(dir)
            dir_list(f, dir)

if __name__ == "__main__":
    start='Music'
    music_list = list()
    with open('db.txt', 'w', encoding="utf-8") as f:
        dir_list(f, start)

    # client.download_sync(remote_path="/Music/1.mp3", local_path="./music/1.mp3")