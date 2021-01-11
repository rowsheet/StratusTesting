def run(test, config, save_html):

    page = test["page"]
    auth = test["auth"]
    load = test["load"]
    url = config["base_url"] + test["path"]

    # Filename for the benchmark data is [page]_[auth]_[load].dat
    # for example: Homepage_Public_BAL.dat
    filename = "_".join([page, auth, load]) + ".dat"

    print("""
Running benchmark:
    page: %s
    auth: %s
    load %s
    url: %s
    """ % (page, auth, load, url))

    if save_html == True:
        html_filename = filename.split(".")[0] + ".html"
        print("Saving html test copies in ./data/" + html_filename)

    print("""
Benchmark coplete...
--------------------------------------------------------------------------------""")
