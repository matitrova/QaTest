import os

ISPBOSS_USER = os.getenv("ISPBOSS_USER")
ISPBOSS_PASS = os.getenv("ISPBOSS_PASS")
BASE_URL = os.getenv("ISPBOSS_URL", "https://beta.test.ispboss.com")