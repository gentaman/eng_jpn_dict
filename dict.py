import urllib
from xml.etree import ElementTree
import sys


def main(word):
    search_word = word.replace(',', '')
    if search_word == '':
        return
    item_id = getItemID(search_word)
    text = getTranslatedText(item_id)
    if text == '':
        return
    texts = splitTranslatedText(text, '\t')
    if len(texts) >= 5:
        texts = texts[:5]
    texts = "\t".join(texts)
    text = text.replace('\t', '\n')
    return text.encode('utf-8')


def getXmlElementText(url, tag):
    try:
        xml = urllib.urlopen(url)
    except urllib.error.HTTPError as e:
        print('error code : ' + str(e.code))
        print('error read : ' + str(e.read()))
        return ''

    tree = ElementTree.parse(xml)
    root = tree.getroot()
    element = root.find('.//{http://btonic.est.co.jp/NetDic/NetDicV09}' + tag)
    if element is None:
        return ""
    text = element.text
    return text


def getItemID(search_word):
    head = 'http://public.dejizo.jp/NetDicV09.asmx/SearchDicItemLite?Dic=EJdict&Word='
    end = '&Scope=HEADWORD&Match=EXACT&Merge=OR&Prof=XHTML&PageSize=20&PageIndex=0'
    url = head + search_word + end
    return getXmlElementText(url, 'ItemID')


def getTranslatedText(item_id):
    head = 'http://public.dejizo.jp/NetDicV09.asmx/GetDicItemLite?Dic=EJdict&Item='
    end = '&Loc=&Prof=XHTML'
    url = head + item_id + end
    return getXmlElementText(url, 'Body/div/div')


def splitTranslatedText(translated_text, split_word):
    return translated_text.split(split_word)


if __name__ =='__main__':
    print(main(sys.argv[1]))
