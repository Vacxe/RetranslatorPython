import sys
import os
from xml.etree import ElementTree
from requests.utils import quote
import requests
import json
import io
import re

supportedLocales = ['ru', 'es', 'de', 'zh', 'cz', 'nl', 'fr',
                    'it', 'ja', 'ko', 'pl', 'ar', 'bg', 'ca',
                    'hr', 'da', 'fi', 'el', 'iw', 'hi', 'hu',
                    'in', 'lv', 'lt', 'nb', 'pt', 'ro', 'sr',
                    'sk', 'sl', 'sv', 'tl', 'th', 'tr', 'uk',
                    'vi', 'en']
shieldSymbol = ' {} // '


def saveToFile(resdir, locale, xml):
    localizedValueDir = resdir + "/values-" + locale
    if not os.path.isdir(localizedValueDir):
        os.mkdir(localizedValueDir)

    localizedValuesFile = localizedValueDir + "/strings.xml"

    io.open(localizedValuesFile, "w", encoding='utf8').writelines(xml)
    print("Successful file creation for {} locale".format(locale))

    pass


def translateString(query, targetLocale):
    shieldSymbols = re.findall('[%][bBhHsScCdoxXeEfgGaAtTn]', query)
    query = re.sub('[%][bBhHsScCdoxXeEfgGaAtTn]', shieldSymbol, query)

    request = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={}&dt=t&q={}" \
        .format(targetLocale, quote(query))
    translation = json.loads(requests.get(request).content)[0][0][0]
    translation = translation.replace("{} //", "{}").format(*shieldSymbols)
    return translation
    pass


def translateTo(baseXML, locale):
    root = baseXML.getroot()

    for string in root.findall('string'):
        string.text = translateString(string.text, locale)

    for stringArray in root.findall('string-array'):
        for item in stringArray.findall('item'):
            item.text = translateString(item.text, locale)

    for stringArray in root.findall('plurals'):
        for item in stringArray.findall('item'):
            item.text = translateString(item.text, locale)
    return ElementTree.tostring(baseXML.getroot(), encoding='utf8').decode()


def main(argv):
    print("Starting script...")

    projectDir = os.getcwd()

    print("Project dir is: " + projectDir)

    print("Try to find resources directory")

    resDir = projectDir + "/app/src/main/res"

    if os.path.isdir(resDir):
        print("Successful detection: " + resDir)
    else:
        while not os.path.isdir(resDir):
            print("Input res directory manually")
            resDir = input()

    templateStringXmlLocation = resDir + "/values/strings.xml"
    if os.path.exists(templateStringXmlLocation):
        print("Template string.xml detected")
    else:
        print("Could't find string.xml in default value directory")
        pass

    baseXML = ElementTree.parse(templateStringXmlLocation)

    for locale in supportedLocales:
        translatedXML = translateTo(baseXML, locale)
        saveToFile(resDir, locale, translatedXML)
    pass


if __name__ == "__main__":
    main(sys.argv)
