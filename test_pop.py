from socket import *
import os
import re
import json
from email import message_from_string
import email
from pathlib import Path

t='D:/Python_Store/pop3_client/work'
if not Path(t).exists():
    Path(t).mkdir()