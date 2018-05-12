import sys
import os
import re
from requests.utils import quote
import requests
import json
import io

supportedLocales = ['ru', 'es', 'de', 'zh', 'cz', 'nl', 'fr',
                    'it', 'ja', 'ko', 'pl', 'ar', 'bg', 'ca',
                    'hr', 'da', 'fi', 'el', 'iw', 'hi', 'hu',
                    'in', 'lv', 'lt', 'nb', 'pt', 'ro', 'sr',
                    'sk', 'sl', 'sv', 'tl', 'th', 'tr', 'uk',
                    'vi']


def buildTranslationFile(resdir, locale, pairs):
    localizedValueDir = resdir + "/values-" + locale
    if not os.path.isdir(localizedValueDir):
        os.mkdir(localizedValueDir)

    localizedValuesFile = localizedValueDir + "/values.xml"

    lines = ["<resources>\n"]
    for pair in pairs:
        lines.append('\t<string name="{}">{}</string>\n'.format(pair[0], pair[1]))
    lines.append("</resources>")

    io.open(localizedValuesFile, "w", encoding='utf8').writelines(lines)
    print("Successful file creation for {} locale".format(locale))

    pass


def translateString(query, targetLocale):
    request = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={}&dt=t&q={}" \
        .format(targetLocale, quote(query))
    translation = json.loads(requests.get(request).content)[0][0][0]

    return translation
    pass


def translate(locale, pairs):
    tranlations = []
    for pair in pairs:
        tranlations.append((pair[0], translateString(pair[1], locale)))

    print('Localization finished for {} locale'.format(locale))
    return tranlations
    pass


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

    with open(templateStringXmlLocation) as f:
        content = f.readlines()
        pairs = []
        for line in content:
            m = re.search('<string name="(.+?)">(.+?)</string>', line)
            if m:
                stringId = m.group(1)
                value = m.group(2)
                pairs.append((stringId, value))

        print("Detected " + str(len(pairs)) + " strings")

    print("Translation processing...")

    for locale in supportedLocales:
        buildTranslationFile(resDir, locale, translate(locale, pairs))

    pass


if __name__ == "__main__":
    main(sys.argv)
