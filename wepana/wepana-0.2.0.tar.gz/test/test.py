# _*_encode=utf-8_*_
from wepana import WebPageAnalyzer


def test():
    test_url = 'http://huaban.com/favorite/design/'

    analyzer = WebPageAnalyzer(url=test_url, timeout=5)

    # title
    print('title: %s' % analyzer.get_title())

    # images
    images = analyzer.get_images()
    image_count = len(images)
    print('image count: %d' % image_count)

    if image_count > 0:
        print('images:')
        for image in images:
            print('    %s' % image)

    # links
    links = analyzer.get_links()
    link_count = len(links)
    print('link count: %d' % link_count)

    if link_count > 0:
        print('links:')
        for link in links:
            print('    %s' % link)

    # keywords
    keywords = analyzer.get_keywords()
    keyword_count = len(keywords)
    print('keyword count: %d' % keyword_count)

    if keyword_count > 0:
        print('keywords:')
        for keyword in keywords:
            print('    %s' % keyword)


if __name__ == '__main__':
    test()
