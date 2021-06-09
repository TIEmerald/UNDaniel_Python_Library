
import os
import re
import sys
import pandas as pd
from pandas.core.frame import DataFrame

class FilerScanner: 

    def read_and_split_file(self, file_name: str) -> list:
        text_data = list()
        current_file = os.path.abspath(os.path.join(".", file_name))
        if os.path.exists(current_file):
            print(current_file)
            open_file = open(current_file, 'r', encoding="latin-1")
            text_data = open_file.read().split('\n')
            text_data = list(filter(None, text_data))
        return text_data

    def read_and_extract_info(self, file_name: str) -> pd.DataFrame:
        usingFileName = file_name
        text_data = self.read_and_split_file(usingFileName)
        lineCount = 0
        title = ""
        content = ""
        score = 0
        date = ""
        version = ""
        df_list = list()
        index = 0
        skip_to_version = False
        country = ""
        shouldAddOne = False
        for line in text_data:
            # checking if have Developer Response or not.
            results = re.search("Developer Response - [A-Z]{1}[a-z]{2} [12]?[0-9]{1}, 2021", line)
            if results is not None:
                # if Found, we need skip until the line for Version
                skip_to_version = True

            if skip_to_version:
                results = re.search("Version [0-9]{1}\.[0-9]{1,2}\.[0-9]*", line)
                if results is None:
                    continue
                else:
                    skip_to_version = False  
                
            if lineCount == 0:
                results = re.match("^(.*) ([1-5])$", line)
                if results is not None:
                    lineCount = (lineCount + 1) % 4
                    title = results[1]
                    score = int(results[2])
            elif lineCount == 1:
                results = re.search("[A-Z]{1}[a-z]{2} [12]?[0-9]{1}, 2021", line)
                if results is not None:
                    lineCount = (lineCount + 1) % 4
                    date = results[0]
            elif lineCount == 2:
                lineCount = (lineCount + 1) % 4
                content = line
            elif lineCount == 3:
                results = re.search("Version ([0-9]{1}\.[0-9]{1,2}\.[0-9]*) ([A-Za-z]*)", line)
                if results is not None:
                    lineCount = (lineCount + 1) % 4
                    version = results[1]
                    country = results[2]
                    shouldAddOne = True # one record read finished
            if shouldAddOne:
                data = {'index':[index],  'title': title, 'content': content, 'date': date, 'version': version, 'score': score, 'country': country}
                data_frame = pd.DataFrame(data)
                index += 1
                df_list.append(data_frame)
                shouldAddOne = False
        df = pd.concat(df_list)
        df.to_csv(usingFileName+"_results.csv", sep=',')
        return df


# fun2
def main(argv):
    files = ["sg_file", "id_file", "vn_file", "my_file", "ph_file", "th_file", "total_file"]
    scanner = FilerScanner()
    for file in files:
        scanner.read_and_extract_info(file)

# fun2
if __name__ == '__main__':
    main(sys.argv[1:])