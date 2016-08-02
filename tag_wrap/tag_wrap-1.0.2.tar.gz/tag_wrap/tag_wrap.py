"""Method that has at least two arguments and returns a string
 1) tag to wrap with
 2) content to wrap (anything that returns a string)
 3) Optionally, you may have keyword attributes.
    These must come after all non-keyword submissions.
"""


def tag_wrap(tag_name, *args, **kwargs):
    """Take a tag that will wrap the content
    and return the final comined string.
    """

    if kwargs is not None:
        attributes = []
        for attr in kwargs:
            attributes.append(attr + '="' + kwargs[attr] +'"')


    tag = tag_name.strip()

    if attributes:
        all_attributes = ' '.join(attributes)
        start_tag = '<' + tag + ' ' + all_attributes + '>'
    else:
        start_tag = '<' + tag + '>'

    end_tag = '</' + tag + '>'
    content = ''
    for arg in args:
        content = content + arg

    return start_tag + content + end_tag

