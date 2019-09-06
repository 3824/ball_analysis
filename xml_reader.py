import xml.etree.ElementTree as ET

import pandas as pd
import glob
import re

pitch_attrib_list = ["pitch_type", "start_speed", "end_speed", "spin_dir", "spin_rate", "pfx_x", "pfx_z", "px", "pz",
                     "x0", "y0", "ax", "ay", "az", "vx0", "vy0", "vz0","sz_top","sz_bot"]

def read_pitch_xml(_file_path, gid):
    f = open(_file_path)
    inning_data = f.read()  # ファイル終端まで全て読んだデータを返す
    f.close()

    root = ET.fromstring(inning_data)

    data = {}
    for inning in root.iter('inning'):
        inning_num = inning.attrib["num"]
        for atbat in inning.findall("./*/atbat"):
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
                    # print(pitch.attrib)
                    pass
    col_names = ["pitcher_id", "batter_id"]
    pitch_df = pd.DataFrame.from_dict(data, orient='index', columns=col_names + pitch_attrib_list)
    pitch_df.to_csv("pitch_{}.csv".format(gid), index=False)
    pitch_df["gid"] = gid
    return pitch_df

if __name__ == '__main__':
    gid_pattern = re.compile(".+(gid_.+)\\.xml")
    # file_path = "data/gid_2018_03_01_milmlb_arimlb_1.xml"
    df_list = []
    for file_path in glob.glob("data/*.xml"):
        res = gid_pattern.match(file_path)
        if res:
            gid = res.group(1)
            df_list.append(read_pitch_xml(file_path, gid))
    pd.concat(df_list, axis=0).to_csv("pitch_df.csv", index=False)

    # path = "data/gid_2018_03_01_atlmlb_detmlb_1.xml"
    # print(read_pitch_xml(path, "gid_2018_03_01_atlmlb_detmlb_1"))

