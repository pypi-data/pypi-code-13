from subprocess import Popen, PIPE
from bs4 import BeautifulSoup


class 轉換doc:

    def __init__(self, 檔名):
        self.檔名 = 檔名

    def 提html(self):
        return self.html

    def 提array(self):
        return self.array

    def 提json(self):
        return self.json

    def doc轉html(self):
        程序 = Popen(['wvWare', self.檔名], stdin=None, stdout=PIPE, stderr=PIPE)
        輸出資訊, _錯誤輸出資訊 = 程序.communicate()
        self.html = 輸出資訊.decode('utf-8', errors="replace")
        return self

    def html轉array(self):
        bs = BeautifulSoup(self.html, "lxml")
        table = bs.table
        全部資料 = []
        for tr in table.find_all('tr'):
            一逝資料 = []
            for td in tr.find_all('td'):
                一逝資料.append(td.get_text("", strip=True))
            全部資料.append(一逝資料)
        self.array = 全部資料
        return self

    def array轉json(self):
        全部資料 = {'資料': []}
        這馬篇 = None
        for 一逝 in self.array:
            if 一逝[0] == '篇名':
                if 這馬篇 is None:
                    這馬篇 = {'篇名': 一逝[1], '段': []}
                elif 這馬篇 is not None and '篇名' in 這馬篇:
                    全部資料['資料'].append(這馬篇)
                    這馬篇 = {'篇名': 一逝[1], '段': []}
                elif 這馬篇 is not None and '篇名' not in 這馬篇:
                    這馬篇[一逝[0]] = 一逝[1]
            elif 一逝[0] == '段' or (一逝[0] == '' and len(一逝) == 3):
                try:
                    這馬篇['段'].append((一逝[1], 一逝[2]))
                except:
                    if len(一逝) == 2 and 一逝[1] in [
                        '第十八課 我會曉講（二）',  # 金門國小五年級
                        '手揭sit8-toh扑倒吊',  # 2004平溪相褒歌
                        '想卜博筊起大厝',  # 2004平溪相褒歌
                        '阿君轉去免赫早',  # 2004平溪相褒歌
                    ]:
                        全部資料['資料'].append(這馬篇)
                        這馬篇 = {'篇名': 一逝[1], '段': []}
                    else:
                        raise
            elif 一逝[0] == '4' and len(一逝) == 3:  # 1993大家來說台灣母語
                這馬篇['段'].append((一逝[1], 一逝[2]))
            elif 一逝[0] == '作者' and 這馬篇 is not None:
                這馬篇['作者'] = 一逝[1]
            else:
                if 這馬篇 is not None:
                    if len(全部資料) == 1:
                        if 一逝[0] in 這馬篇:
                            全部資料['資料'].append(這馬篇)
                            這馬篇 = {'段': []}
                        這馬篇[一逝[0]] = 一逝[1]
                    else:
                        if len(全部資料['資料']) > 0:
                            raise RuntimeError('無應該閣出現別的資訊：{}'.format(一逝[0]))
                        if len(這馬篇['段']) == 0:
                            這馬篇[一逝[0]] = 一逝[1]
                        else:
                            全部資料.pop('資料')
                            這馬篇.update(全部資料)
                            全部資料 = {'資料': [這馬篇]}
                            這馬篇 = {一逝[0]: 一逝[1], '段': []}
                else:
                    全部資料[一逝[0]] = 一逝[1]
        if 這馬篇 is not None:
            全部資料['資料'].append(這馬篇)
        self.json = 全部資料
        return self
