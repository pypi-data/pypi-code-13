def run(action, music=None, **kwargs):
    for music in action.music_list(music):
        if music.is_loaded_paused():
            music.unpause()

def description(action, music=None, **kwargs):
    if music is not None:
        return "unpausing « {} »".format(music.name)
    else:
        return "unpausing all musics"
