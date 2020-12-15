# -- Imports --------------------------------------------------------------------------

from .moca_utils import (
    location, caller_name, self_name, print_debug, print_info, print_warning, print_error, print_critical,
    print_license, save_license_to_file, install_modules, install_requirements_file, git_clone, wget, aio_wget, wcheck,
    aio_wget, wstatus, aio_wstatus, disk_speed, check_hash, get_time_string, print_with_color, add_extension,
    add_dot_jpg, add_dot_jpeg, add_dot_gif, add_dot_txt, add_dot_png, add_dot_csv, add_dot_rtf, add_dot_pdf,
    add_dot_md, add_dot_log, add_dot_json, add_dot_py, add_dot_cache, add_dot_pickle, add_dot_js, add_dot_css,
    add_dot_html, set_interval, set_timeout, on_other_thread, is_hiragana, is_katakana,
    is_small_hiragana, is_small_katakana, hiragana_to_katakana, katakana_to_hiragana, check_length, dump_json_beautiful,
    dumps_json_beautiful, contains_upper, contains_lower, contains_alpha, contains_digit, contains_symbol,
    only_consist_of, to_hankaku, to_zenkaku, check_email_format, moca_dumps, moca_dump, moca_aio_dump, moca_loads,
    moca_load, moca_aio_load, print_only_in_main_process, set_process_name, html_escape, html_unescape, word_block,
    get_random_string, try_to_int, create_a_big_file, get_random_bytes, get_random_string_by_digits,
    get_random_string_by_hiragana, get_random_string_by_katakana, get_random_string_by_kana, debugger,
    get_env, load_env, run_system, check_function_speed, try_print, try_pprint, aio_call, create_a_big_text_file,
    print_new_line, range_ext, loop, slice_by_keyword, print_json_beautiful, is_ujson, try_to_float, try_to_bool,
    try_to_obj, parser_str, en_faker, jp_faker, zh_faker, validate_argument, is_file, is_dir, get_text_from_url,
    aio_get_text_from_url, print_table, remove_extension, all_ascii, all_alnum, all_alpha, all_numeric,
    have_alnum, have_alpha, have_ascii, have_numeric, create_tor_deny_config_for_nginx, pm, pl, resize_img,
    get_my_public_ip, get_my_public_ip_v6, get_my_public_ip_v4, update_use_github, update_moca_modules
)
from .moca_centos_utils import (  # The functions in this file, Only supports CentOS 8 and RHEL 8.
    get_centos_cpu_info, get_centos_cpu_model_name, get_centos_cpu_vendor_id, get_centos_cpu_cores,
    get_centos_cpu_cache_size, get_centos_cpu_mhz, get_centos_ssh_login_log, get_centos_accepted_ssh_login_log,
    get_centos_failed_ssh_login_log, get_centos_invalid_ssh_login_log, get_centos_accepted_ssh_login_count,
    get_centos_failed_ssh_login_count, get_centos_invalid_ssh_login_count, get_centos_recently_login_logs,
    get_centos_kernel,
)
from .moca_system_utils import (
    get_logical_cpu_count, get_cpu_count, get_cpu_percent, get_cpu_percent_per_cpu, get_total_memory, get_free_memory,
    get_used_memory, get_memory_percent, get_memory_info, get_total_swap_memory, get_free_swap_memory,
    get_used_swap_memory, get_swap_memory_percent, get_swap_memory_info, get_disk_usage, get_self_used_memory,
    get_self_used_memory_percent, get_my_username, is_root, get_my_pid, get_my_tid, add_moca_modules_to_system,
    is_main_process
)

# -------------------------------------------------------------------------- Imports --


"""
This module provides many utilities.

Requirements
------------
GitPython
    GitPython is a python library used to interact with Git repositories
requests
    Requests is a simple, yet elegant HTTP library.
aiohttp
    Async http client/server framework
aiofiles
    aiofiles is an Apache2 licensed library, written in Python, for handling local disk files in asyncio applications.
setproctitle
    A Python module to customize the process title
psutil
    Cross-platform lib for process and system monitoring in Python
pycryptodome
    PyCryptodome is a self-contained Python package of low-level cryptographic primitives.
python-dotenv
    Reads the key-value pair from .env file and adds them to environment variable.
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
cloudpickle
    Extended pickling support for Python objects
pygments
    Pygments is a generic syntax highlighter written in Python
Faker
    Faker is a Python package that generates fake data for you.
prettytable
    A simple Python library for easily displaying tabular data in a visually appealing ASCII table format
Pillow
    The friendly PIL fork (Python Imaging Library)
"""
