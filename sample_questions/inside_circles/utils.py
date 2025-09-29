import json
import os
import re

def output_from_text(response):
    try:
        pattern = r"COUNT:\s*(\d+)"
        
        # Find the match in the response
        match = re.search(pattern, response)

        if match:
            count = match.group(1).strip()
            return {
                "OUTPUT": int(count),
                "ERROR": None
            }
        else:
            return {
                "OUTPUT": None,
                "ERROR": "No match found"
            }
  
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": f"Unexpected error while parsing {str(e)}\n"
        }

def gold_to_output(i):
    gold_output = None
    try:
         #get directory of this file
        dir_of_file = os.path.dirname(os.path.realpath(__file__))
        #open the data file
        with open(dir_of_file + "\data.json") as f:
            data = json.load(f)
        row = data[i]
        gold_output = row['inside_circles']
        output_prompt = "COUNT:" + str(gold_output)
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }

# import json
# with open("./answer_inductive.json", "r") as f:
#     data = json.load(f)
#     # print(data[1])
#     for i in data:
#         output_text = i["gpt_response"]
#         i["Output"] = output_from_text(output_text)["OUTPUT"]
#         i["ERROR"] = output_from_text(output_text)["ERROR"]
#         #remove OUTPUT key
#         # i.pop("OUTPUT")
    
#     with open("./answer_inductive.json", "w") as f:
#         json.dump(data, f, indent=4)
#         print("Output saved to answer.json")