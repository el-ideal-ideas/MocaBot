"""Same to py file."""

# -- el command --------------------------------------------------------------------------

# get current time as datetime.
# datetime.datetime(2020, 10, 8, 17, 16, 7, 877655)
NOW: str = '[el]#moca_now#'


# get current time as str
# '2020-10-08 17:16:13.037439'
NOW_STR: str = '[el]#moca_now_str#'


# get current date as datetime
# datetime.date(2020, 10, 8)
NOW_DATE: str = '[el]#moca_now_date#'


# get current date as str
# '2020-10-08'
NOW_DATE_STR: str = '[el]#moca_now_date_str#'


# get a random float between 0 and 1
# 0.1791335306483246
RANDOM: str = '[el]#moca_random#'


# get a random string
# %s is the value of length.
RANDOM_STRING: str = '[el]#moca_random_string<%s>#'


# get a random integer
# 0 - 9
RANDOM_INTEGER: str = '[el]#moca_random_integer#'

# get a random integer list.
# %s is the length of the list
RANDOM_INTEGER_LIST: str = '[el]#moca_random_integer_list<%s>#'


# get a random string that is consist of digits.
# %s is the length of the string.
RANDOM_INTEGER_STR: str = '[el]#moca_random_integer_str<%s>#'


# get a random bytes
# %s is the length of the bytes
RANDOM_BYTES: str = '[el]#moca_random_bytes<%s>#'


# get a random int with specific range
# first %s is start value
# second %s is end value
RANDOM_RANGE: str = '[el]#moca_random_range<%s,%s>#'


# get a uuid1 object.
# UUID('2da7333e-0941-11eb-a8e5-784f436bb288')
UUID1: str = '[el]#moca_uuid1#'


# get the hex value of uuid1
# 4d80b09a094111eba8e5784f436bb288
UUID1_HEX: str = '[el]#moca_uuid1_hex#'


# get a uuid1 as string
# 8d512fce-0941-11eb-a8e5-784f436bb288
UUID1_STR: str = '[el]#moca_uuid1_str#'

# get a uuid4 object.
# UUID('2da7333e-0941-11eb-a8e5-784f436bb288')
UUID4: str = '[el]#moca_uuid4#'


# get the hex value of uuid4
# 4d80b09a094111eba8e5784f436bb288
UUID4_HEX: str = '[el]#moca_uuid4_hex#'


# get a uuid4 as string
# 8d512fce-0941-11eb-a8e5-784f436bb288
UUID4_STR: str = '[el]#moca_uuid4_str#'


# return current process id as int
PROCESS_ID: str = '[el]#moca_process_id#'


# return the name of current process as str
PROCESS_NAME: str = '[el]#moca_process_name#'  # process name


# return the number of cpu cores as int
CPU_COUNT: str = '[el]#moca_cpu_count#'


# load a data from the json string
# %s is the json string.
JSON: str = '[el]#moca_json<%s>#'


# もっちもっちにゃんにゃん！
MOCHI: str = '[el]#moca_mochi#'


# -------------------------------------------------------------------------- el command --
