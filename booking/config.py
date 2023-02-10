TEARDOWN = False

BASE_URL = "https://booking.com"

# use capital letter abbreviations, i.e. 'USD', 'EUR' etc.
CURRENCY = "USD"
PLACE_TO_GO = "warsaw"

# must be in 'YYYY-MM-DD' format
CHECK_IN_DATE = "2023-02-20"
CHECK_OUT_DATE = "2023-02-24"

# list of ints between 2 and 5
PREFERRED_STAR_RATINGS = [4, 5]

# to use with explicit/conditional waits, defined in seconds
SHORT_TIMEOUT = 0.5
MEDIUM_TIMEOUT = 5.
LONG_TIMEOUT = 10.

# uncomment the line below to run in fullscreen and/or add other options
CHROME_OPTIONS = [
    '--start-fullscreen'
]





