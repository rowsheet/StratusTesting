# Stratus Test

Performance Test for `www.stratus.co`

I'm consolidating the code to run performance benchmarks and reporting in this repo.
Evntually I will port configuration to a yaml file or something.

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
