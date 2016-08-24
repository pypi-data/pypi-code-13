from markdown import markdown

def hello1():
	data = "#Judul Hello 1\n"
	data += "**Hello 1**."
	return markdown(data)

def hello2():
	data = "#Judul Hello 2\n"
	data += "**Hello 2**."
	return markdown(data)