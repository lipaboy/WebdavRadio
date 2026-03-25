import sys

# искать повторы папок для примера можно сделать

if __name__ == "__main__":
    music_dict = dict[str, str]()
    repeat_folders = set()
    with open('./db/song_list2.txt', 'r', encoding="utf-8") as f:
        for path in f:
            pos = path.rfind('/')
            folder = path[:pos]
            track = path[pos + 1:]
            if track in music_dict:
                repeat_folders.add(folder + ' | ' + music_dict[track])
            else:
                music_dict[folder] = folder
    for f in repeat_folders:
        print(f)