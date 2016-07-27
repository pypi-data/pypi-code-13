def run(action, music=None, **kwargs):
    for music in action.music_list(music):
        if music.is_loaded_playing():
            music.pause()

def description(action, music=None, **kwargs):
    if music is not None:
        return "pausing « {} »".format(music.name)
    else:
        return "pausing all musics"
