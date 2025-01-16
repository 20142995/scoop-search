import os
import re
import sys
import json
from prettytable import PrettyTable

def search_json_files(directory, keywords):
    results = []
    for _dir in os.listdir(directory):
        directory_3 = os.path.join(directory,_dir,'bucket')
        for filename in os.listdir(directory_3):
            if filename.endswith(".json"):
                name = filename[:-5]
                file_path = os.path.join(directory_3, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)
                        item = {}
                        item["Name"] = name
                        item["Version"] = data['version']
                        item["Homepage"] = data['homepage']
                        if any([re.findall(keyword ,str(data.get("description","")) + str(data.get("notes",""))  + str(data.get("bin","")) + name + str(data.get('version','')) + str(data.get('homepage','')) + str(data.get('bin','')),re.I) for keyword in keywords]):
                            item["Description"] = ';'.join([",".join(re.findall(r'\S{1,5}'+ keyword +r'\S{1,5}',str(data.get("description","")),re.I)) for keyword in keywords])
                            item["Notes"] = ';'.join([",".join(re.findall(r'\S{1,5}'+ keyword +r'\S{1,5}',str(data.get("notes","")),re.I)) for keyword in keywords])
                            item["Bin"] = ','.join(re.findall(r'[\w\\\.]+',str(data.get("bin","")),re.I)[:3]) # 只展示前三
                            results.append(item)
                    except json.JSONDecodeError:
                        print(f"Warning: {file_path} is not a valid JSON file.")
                    except:
                        continue
    return results

def display_results(results):
    if not results:
        print("No results found.")
        return

    table = PrettyTable()
    table.field_names = ["Name", "Version", "Homepage", "Description", "Notes","Bin"]

    for result in results:
        table.add_row([
            result.get("Name",""),
            result.get("Version",""),
            result.get("Homepage",""),
            result.get("Description",""),
            result.get("Notes",""),
            result.get("Bin",""),
        ])
    
    print(table)

def main():
    directory = r"D:\Tools\buckets"
    if not os.path.exists(directory):
        directory = os.path.join('./','../../../','buckets')
    keywords = sys.argv[1:]
    results = search_json_files(directory,keywords)
    display_results(results)

if __name__ == "__main__":
    main()
