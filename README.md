# Stratus Test

Performance Test for `www.stratus.co`

This does two things:

1. Runs N number of requests to the URL and path specified with a specified amount of time inbetween and times the request. After this, it saves the data to `./data`. If there was any previous data, it will either overwrite it or archive it in `./data/archive_[timestamp]`. It also optionally saves the html page that you're benchmarking for a sanity check (note that if you test `https://stratus.co/alex`, the routing will redirect you to the root if you don't add `www`).
2. It graphs the dataset in `./data`. Each dataset is labled by the config (page type, path, auth settings, load-balancer setting). This is also the label you will see in the graph.

If you're going to run this, make sure to set configurations in `config.yaml`. As if writing this, you should still be able to just copy the `config.yaml.samlpe`, but you should get your own session information by creating an account and inspecting the headers. You need these cookies from the headers of a valid authenticated request (because this tests authenticated requests):

        c_user: USER_ID
        xs: SESSION_KEY
        AWSALB: LOAD_BALANCING_TOKEN
        AWSALBCORS: CORS_LOAD_BALANCING_TOKEN

## Usage:
    Usage: python3 main.py [benchmark|graph]
        --overwrite_data    Delete old test data and overwrite
        --save_html         Save html copy of page tested

## Usage Examples:
    # Run the benchmark tests (if any existing benchmark data exists, it will be archived)
    $ python3 main.py benchmark
    
    # Run the benchmark and save a copy of each HTML page
    $ python3 main.py benchmark --save_html
    
    # Run the graph
    $ pythong3 main.py graph

## Configuration
Copy `config.yaml.sample` into `config.yaml` and fetch values for your own user session.
You will have to create a Stratus account, log in, and copy the session variables as well as the AWS loadbalancer variables from the cookie or request headers.

## Configuration Examples:

        base_url: https://www.stratus.co

        # LOG INTO stratus.co AND COPY THIS FROM YOUR COOKIES OR HEADERS

        c_user: USER_ID
        xs: SESSION_KEY
        AWSALB: LOAD_BALANCING_TOKEN
        AWSALBCORS: CORS_LOAD_BALANCING_TOKEN

        # DEFINE TEST SETTINGS

        num_req: NUM_REQUEST_TO_RUN
        sleep: SECONDS_BETWEEN_REQUESTS

        # DEFINE TESTS

        tests:
              - page: Homepage
                auth: Public
                load: BAL
                path: /
              - page: Homepage
                auth: Public
                load: UNBAL
                path: /
              - page: Profile
                auth: Auth
                load: BAL
                path: /alexk
              - page: Profile
                auth: Auth
                load: UNBAL
                path: /alexk
              - page: Profile
                auth: Public
                load: BAL
                path: /alexk
