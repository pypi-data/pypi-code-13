def take(n, gen):
    i = 0
    for item in gen:
        if i < n:
            yield item
            i += 1
        else:
            break
