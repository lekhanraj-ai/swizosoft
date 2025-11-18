"""Offer letter serial number manager"""
import json
import os

SERIAL_FILE = "offer_serial.json"

def get_serial(month):
    """Get and increment serial number for the month"""
    if not os.path.exists(SERIAL_FILE):
        with open(SERIAL_FILE, "w") as f:
            json.dump({"month": "", "serial": 0}, f)

    with open(SERIAL_FILE, "r") as f:
        data = json.load(f)

    if data["month"] != month:
        data["month"] = month
        data["serial"] = 1
    else:
        data["serial"] += 1

    with open(SERIAL_FILE, "w") as f:
        json.dump(data, f)

    return f"{data['serial']:03}"
