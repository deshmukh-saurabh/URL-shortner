import random
import string
from datetime import timedelta, datetime
from shortner.models import URL
from url_shortner.settings import DATETIME_FORMAT_STANDARD

BASE_URL = "http://{}/{}"


def generate_hash():
    """
    Helper method to generate hash of length 10 using string lower, upper case characters and digits
    """
    N = 10
    st = string.ascii_uppercase + string.digits + string.ascii_lowercase
    random_char_list = random.choices(st, k=N)
    hash = ''.join(random_char_list)
    return hash


def generate_short_url(original_url, expiration_ts, current_site):
    """
    Helper method to shorten the original url
    """
    # generate a new hash
    hash = generate_hash()

    # check  if this hash already exists
    hash_exists = URL.objects.filter(hash=hash).exists()

    # if it does not already exist, create an entry, else try generating a new hash
    if not hash_exists:
        created = URL.objects.create(hash=hash, original_url=original_url, expiration_ts=expiration_ts)
        short_url = BASE_URL.format(current_site, hash)
        return short_url
    else:
        generate_short_url(original_url, expiration_ts, current_site)


def check_hash_expiry(url):
    """
    Check if hash has expired
    """
    current_ts = datetime.now().replace(tzinfo=None).strftime(DATETIME_FORMAT_STANDARD)
    expiration_ts = str(url.expiration_ts)
    # print(timedelta(current_ts, expiration_ts).seconds)
    if current_ts >= expiration_ts:
        return False
    return True


def is_hash_valid(hash):
    """
    API view to check if hash is a valid one
    """
    # check if hash is present in DB
    url = URL.objects.filter(hash=hash)
    hash_exists = url.exists()
    if not hash_exists:
        return False
    
    # check if hash has expired
    hash_expired = check_hash_expiry(url[0])
    if hash_expired:
        return False
    
    original_url = url[0].original_url
    return True, original_url
