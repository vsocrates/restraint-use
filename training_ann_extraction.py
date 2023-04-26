import pandas as pd
import jsonlines
import glob, os

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

demo = []
present = []
treatment = []
staff = []

demo_prefix = "./annotations/v2/incar_status_demo_edpsych_v1"
present_prefix = "./annotations/v2/incar_status_present_edpsych_v1"
treatment_prefix = "./annotations/v2/incar_status_treatment_edpsych_v1"
staff_prefix = "./annotations/v2/incar_status_staff_edpsych_v1"


# TODO: fix - we assume that tth22 has done all the annotations
with jsonlines.open(f"{demo_prefix}-tth22.jsonl") as reader:
    for line in reader:
        entry = {}
        entry['id'] = line['_input_hash']
        entry['text'] = line['text']
        demo.append(entry)

with jsonlines.open(f"{present_prefix}-tth22.jsonl") as reader:
    for line in reader:
        entry = {}
        entry['id'] = line['_input_hash']
        entry['text'] = line['text']
        present.append(entry)

with jsonlines.open(f"{treatment_prefix}-tth22.jsonl") as reader:
    for line in reader:
        entry = {}
        entry['id'] = line['_input_hash']
        entry['text'] = line['text']
        treatment.append(entry)

with jsonlines.open(f"{staff_prefix}-tth22.jsonl") as reader:
    for line in reader:
        entry = {}
        entry['id'] = line['_input_hash']
        entry['text'] = line['text']
        staff.append(entry)

# columns
# id, text, annotation by annotator (column for each)

for file in glob.glob(f"{demo_prefix}-*"):
    name = file[file.rfind("-") + 1:-6]
    with jsonlines.open(file) as reader:
        for line in reader:
            # find the line in the list that has the matching text for this annotation
            idx = find(demo, "id", line['_input_hash'])
            demo[idx][name] = line['accept']
            if "user_input" in line.keys():
                demo[idx][name + "_comments"] = line['user_input']

for file in glob.glob(f"{present_prefix}-*"):
    name = file[file.rfind("-") + 1:-6]
    with jsonlines.open(file) as reader:
        for line in reader:
            idx = find(present, "id", line['_input_hash'])
            present[idx][name] = line['accept']
            if "user_input" in line.keys():
                present[idx][name + "_comments"] = line['user_input']

for file in glob.glob(f"{treatment_prefix}-*"):
    name = file[file.rfind("-") + 1:-6]
    with jsonlines.open(file) as reader:
        for line in reader:
            idx = find(treatment, "id", line['_input_hash'])
            treatment[idx][name] = line['accept']
            if "user_input" in line.keys():
                treatment[idx][name + "_comments"] = line['user_input']

for file in glob.glob(f"{staff_prefix}-*"):
    name = file[file.rfind("-") + 1:-6]
    with jsonlines.open(file) as reader:
        for line in reader:
            idx = find(staff, "id", line['_input_hash'])
            staff[idx][name] = line['accept']
            if "user_input" in line.keys():
                staff[idx][name + "_comments"] = line['user_input']

pd.DataFrame.from_records(staff).fillna("N/A").to_csv("staff_edpsych_annotations.csv", index=False)
pd.DataFrame.from_records(demo).fillna("N/A").to_csv("demos_edpsych_annotations.csv", index=False)
pd.DataFrame.from_records(treatment).fillna("N/A").to_csv("treatment_edpsych_annotations.csv", index=False)
pd.DataFrame.from_records(present).fillna("N/A").to_csv("presentation_edpsych_annotations.csv", index=False)