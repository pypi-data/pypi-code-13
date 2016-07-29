def run(action, music=None, value=100, fade=0, delta=False, **kwargs):
    if music is not None:
        music.set_volume(value, delta=delta, fade=fade)
    else:
        action.mapping.set_master_volume(value, delta=delta, fade=fade)

def description(action, music=None,
        value=100, delta=False, fade=0, **kwargs):
    message = ""
    if delta:
        if music is not None:
            message += "{:+d}% to volume of « {} »" \
                    .format(value, music.name)
        else:
            message += "{:+d}% to volume" \
                    .format(value)
    else:
        if music is not None:
            message += "setting volume of « {} » to {}%" \
                    .format(music.name, value)
        else:
            message += "setting volume to {}%" \
                    .format(value)

    if fade > 0:
        message += " with {}s fade".format(fade)

    return message
