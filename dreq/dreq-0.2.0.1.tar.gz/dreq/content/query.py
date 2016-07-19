

import dreq


def pluck(section, item=None, attr=None):
	section = dreq.content[section]
	if item is None:
		return section

	item = section[item]
	if attr is None:
		return item

	return getattr(item, attr)
