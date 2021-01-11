import yaml

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

if __name__ == "__main__":
    # Get test config file
    config = get_config()
    # Validate config
    validate_config(config)
    print(config)
