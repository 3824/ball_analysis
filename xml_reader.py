import xml.etree.ElementTree as ET
import io

if __name__ == '__main__':
    file_path = "sample_data/inning_all.xml"

    f = open(file_path)
    inning_data = f.read()  # ファイル終端まで全て読んだデータを返す
    f.close()

    root = ET.fromstring(inning_data)

    for inning in root.iter('inning'):
        print(inning.attrib["num"])
        for pitch in inning.findall("./top/atbat/pitch"):
            print(pitch.attrib)

