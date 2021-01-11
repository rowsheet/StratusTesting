import sys
import yaml
import os
import time
import shutil

def get_config():
    with open("config.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def validate_config(config):
    def check_var(name, obj):
        if name not in obj:
            raise ValueError("Missing variable: " + name)
        if obj[name] is None:
            raise ValueError("Missing variable value: " + name)
    def check_test(test):
        check_var("page", test)
        check_var("auth", test)
        check_var("load", test)
        check_var("path", test)
    try:
        check_var("base_url", config)
        check_var("c_user", config)
        check_var("xs", config)
        check_var("AWSALB", config)
        check_var("AWSALBCORS", config)
        check_var("num_req", config)
        check_var("sleep", config)
        if "tests" not in config:
            raise ValueError("This config has no tests.")
        for test in config["tests"]:
            check_test(test)
    except Exception as ex:
        print("Invalid config. Please see sample configuration file.")
        print(ex)
        exit()

def print_usage():
        print("""
Usage: python3 main.py [benchmark|graph]
    --overwrite_data    Delete old test data and overwrite
    --save_html         Save html copy of page tested
        """)
        exit()

def remove_old_data():
    filenames = os.listdir("./data")
    for filename in filenames:
        if filename.split("_")[0] != "archive":
            filepath = os.path.join("./data", filename)
            os.remove(filepath)

def archive_old_data():
    archive_path = "./data/archive_" + str(time.time()).split(".")[0]
    print("Saving previous test data to " + archive_path)
    os.makedirs(archive_path)
    filenames = os.listdir("./data")
    for filename in filenames:
        if filename.split("_")[0] != "archive":
            shutil.move(os.path.join("./data", filename), os.path.join(archive_path, filename))

if __name__ == "__main__":
    # Get test config file
    config = get_config()
    # Validate config
    validate_config(config)
    if len(sys.argv) == 1:
        print_usage()
    if sys.argv[1] == "benchmark":
        print("Running benchmarks...")
        if "--overwrite_data" in sys.argv:
            remove_old_data()
        else:
            archive_old_data()
        if "--save_html" in sys.argv:
            print("Saving html test copies in data/html...")
    elif sys.argv[1] == "graph":
        print("Generating graph...")
    else:
        print_usage()
