import os
import re
import sys
import json
from prettytable import PrettyTable


def search_json_files(directory, keywords):
    results = []
    for _dir in os.listdir(directory):
        directory_3 = os.path.join(directory, _dir, "bucket")
        for filename in os.listdir(directory_3):
            if filename.endswith(".json"):
                name = filename[:-5]
                file_path = os.path.join(directory_3, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    try:
                        data = json.load(file)
                        item = {}
                        item["Name"] = f'{_dir}/{name}'
                        item["Version"] = data["version"]
                        item["Install"] = 'Y' if os.path.exists(os.path.join(directory,'../','apps',name)) else '-'
                        item["Homepage"] = data["homepage"]
                        # item["Bin"] = str(data.get('bin',''))
                        if all(
                            [
                                re.search(
                                    keyword,
                                    str(data.get("description", ""))
                                    + str(data.get("notes", ""))
                                    + str(data.get("bin", ""))
                                    + name
                                    + str(data.get("version", ""))
                                    + str(data.get("homepage", ""))
                                    + str(data.get("bin", "")),
                                    re.I,
                                )
                                for keyword in keywords
                            ]
                        ):
                            item["Description"] = "\n".join(
                                [
                                    "\n".join(
                                        re.findall(
                                            r"\S{,10}" + keyword + r"\S{,10}",
                                            str(data.get("description", "")),
                                            re.I,
                                        )
                                    )
                                    for keyword in keywords
                                ]
                            )
                            item["Notes"] = "\n".join(
                                [
                                    "\n".join(
                                        re.findall(
                                            r"\S{,10}" + keyword + r"\S{,10}",
                                            str(data.get("notes", "")),
                                            re.I,
                                        )
                                    )
                                    for keyword in keywords
                                ]
                            )
                            item["Bin"] = "\n".join(
                                re.findall(
                                    r"[\w\\\.-]+", str(data.get("bin", "")), re.I
                                )[:3]
                            )
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
    table.field_names = ["Name", "Version", "Install", "Homepage", "Description", "Notes", "Bin"]
    table.hrules = True
    for result in results:
        table.add_row(
            [
                result.get("Name", ""),
                result.get("Version", ""),
                result.get("Install", ""),
                result.get("Homepage", ""),
                result.get("Description", ""),
                result.get("Notes", ""),
                result.get("Bin", ""),
            ]
        )

    print(table)


def main():
    directory = r"D:\Tools\buckets"
    if not os.path.exists(directory):
        directory = os.path.join("./", "../../../", "buckets")
    keywords = sys.argv[1:]
    if len(keywords) == 0:
        print("No keywords.")
        return
    results = search_json_files(directory, keywords)
    display_results(results)


if __name__ == "__main__":
    main()
