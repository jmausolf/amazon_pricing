import os, sys
sys.path.append("pymessage-lite/")
from imessage import *

### Additional User Functions to Work with pymessage-lite
def extact_all_recipients():
    results = {}
    contacts = get_all_recipients()
    for c in contacts:
        r = str(c)
        data = r.replace("ID", "").replace("Phone or email", "").replace(" ", "").replace("+", "").replace("tel:", "").replace("mailto:", "").replace("b'", "").split(":")
        cid = data[1]
        cnumber = data[2]
        results[cid] = cnumber
    return results

def get_ids_for_number(number):
    handles = []
    contacts_dict = extact_all_recipients()
    for k, v in contacts_dict.items():
        if v == number:
            handles.append(k)
    return handles[0]

def return_amazon_code():
    ### Amazon Specific 2-Factor Codes
    message = str(get_messages_for_recipient(int(get_ids_for_number("262966")))[-1])
    code = str(message.replace("Text: ", "").split(" ")[0]).replace("b'", "")
    return code

print(return_amazon_code())
