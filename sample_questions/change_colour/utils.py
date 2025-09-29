import re


def output_from_text(text):
    #extract the number in the last line of text
    try:
        lines = text.strip().split("\n")
        lines = list(filter(None, lines))
        pattern = r'^[^a-zA-Z0-9\s]+$'
        lines = [s for s in lines if not re.fullmatch(pattern, s)]
        quad = -1
        quad = int(re.findall(r"\b\d+\b", lines[-1])[0])

        if quad != -1:
            return {
                "OUTPUT": quad,
                "ERROR": None
            }
        else:
            return{
                "OUTPUT": None,
                "ERROR": 'Does not give correct format'
            }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }

"""import json
import os

def output_from_text(output_text):
    try:
        
        output_text = output_text.split('\n')
        # print(output_text)
        num_lines = len(output_text)

        if num_lines != 1:
            return {
                "OUTPUT": None,
                "ERROR": "Output file should have a single line"
            }
        else:
            out_words = output_text[0].split(' ')
            if len(out_words) != 1:
                return {
                    "OUTPUT": None,
                    "ERROR": "Output file should have a one words"
                }
            else:
                count = out_words[0].split(':')
                if (count[0] != 'COUNT' ):
                    return {
                        "OUTPUT": None,
                        "ERROR": "Output file should have format COUNT:<number>"
                    }
                else:
                    return {
                        "OUTPUT": {
                            "num_differences": int(count[1]),
                        },
                        "ERROR": None
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
        gold_output = row['num_objects']
        output_prompt = "COUNT:" + str(gold_output)
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }"""