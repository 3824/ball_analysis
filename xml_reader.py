import xml.etree.ElementTree as ET

import pandas as pd

pitch_attrib_list = ["pitch_type", "start_speed", "end_speed", "spin_dir", "spin_rate", "pfx_x", "pfx_z", "px", "pz",
                     "x0", "y0", "ax", "ay", "az", "vx0", "vy0", "vz0","sz_top","sz_bot"]

if __name__ == '__main__':
    file_path = "sample_data/inning_all_2.xml"

    f = open(file_path)
    inning_data = f.read()  # ファイル終端まで全て読んだデータを返す
    f.close()

    root = ET.fromstring(inning_data)

    data = {}
    for inning in root.iter('inning'):
        inning_num = inning.attrib["num"]
        for atbat in inning.findall("./top/atbat"):
            batter_id = atbat.attrib["batter"]
            pitcher_id = atbat.attrib["pitcher"]
            for pitch in atbat.findall("./pitch"):
                if "start_speed" in pitch.attrib:
                    row = []
                    id = pitch.attrib["id"]
                    row.append(pitcher_id)
                    row.append(batter_id)
                    for att in pitch_attrib_list:
                        row.append(pitch.attrib[att])
                    data[id] = row
                else:
                    print(pitch.attrib)
    col_names = ["pitcher_id", "batter_id"]
    pitch_df = pd.DataFrame.from_dict(data, orient='index', columns=col_names + pitch_attrib_list)
    pitch_df.to_csv("pitch_df.csv")
