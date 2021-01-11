import time
import requests


# Standard headers to make it look like a browser request.
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
}


# No known standard cookies. If you have some, add theme here.
cookies = {}


# Run a single request and get the response time.
#       Return a tuple of (response_time, html).
#       Note HTML is optional.
def run_single(url, cookies=None, headers=None, save=False):
    start = time.time()
    response = requests.get(url, cookies=cookies, headers=headers)
    end = time.time()
    response_time = end - start
    print("Response time: " + str(response_time))
    html = None
    if save == True:
        html = response.text
    return (response_time, html)


# Run the entire test.
def run(test, config, save_html):

    page = test["page"]
    auth = test["auth"]
    load = test["load"]
    url = config["base_url"] + test["path"]

    # Filename for the benchmark data is [page]_[auth]_[load].dat
    # for example: Homepage_Public_BAL.dat
    filename = "_".join([page, auth, load]) + ".dat"
    filepath = "./data/" + filename
    print("Saving test data to " + filepath)

    print("""
Running benchmark:
    page: %s
    auth: %s
    load %s
    url: %s
    """ % (page, auth, load, url))

    # If we want to save an HTML copy of the benchmark, do it here.
    html_filename = filename.split(".")[0] + ".html"
    html_filepath = "./data/" + html_filename
    if save_html == True:
        print("Saving html test copies to " + html_filename)

    # Add additional cookies per the config.

    # `auth` should either be "Auth" or "Public". if "Public", this doesn't really matter.
    if auth.lower() == "auth":
        cookies["c_user"] = str(config["c_user"])
        cookies["xs"] = str(config["xs"])

    # `load` referes to the load-balancer. Should be either "BAL" or "UNBAL". if "BAL", this doesn't really matter.
    if load == "UNBAL":
        cookies["AWSALB"] = str(config["AWSALB"])
        cookies["AWSALBCORS"] = str(config["AWSALBCORS"])

    # Run the tests as many times as configured
    num_req = config["num_req"]

    # Collect and aggregate the response times.
    response_times = []

    # Loop
    for i in range(num_req):
        # Only save the html on the first download if it's configured.
        if i == 0:
            (response_time, html) = run_single(url, cookies, headers, save_html)
            if html is not None:
                html_file = open(html_filepath, "w")
                html_file.write(html)
                html_file.close()
            response_times.append(str(response_time))
        else:
            # In this case, html will always return None
            (response_time, html) = run_single(url, cookies, headers, False)
            response_times.append(str(response_time))

        # Sleep between requests to spread out the load as configured.
        time.sleep(config["sleep"])

    # Save the response time to the data file.
    response_times = ",".join(response_times)
    data_file = open(filepath, "w")
    data_file.write(response_times)
    data_file.close()


    print("""
Benchmark complete...
--------------------------------------------------------------------------------""")
