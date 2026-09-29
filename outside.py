from dataclasses import dataclass
from collections import defaultdict
import phonenumbers
from datetime import datetime
import termux

from data import RawCall

@dataclass
class SentMessage:
    date: str
    message: str

@dataclass
class Call:
    date: str
    incoming: bool
    duration: str

@dataclass
class Contact:
    name: str 
    phone: str
    phone_pretty: str
    calls: list[Call]
    messages: list[SentMessage]

def _gather_calls() -> list[RawCall]:
    page = 0
    raw_calls = RawCall.load()
    compare_to = raw_calls[0].date if raw_calls else None
    running = True
    while running:
        # termux.API.generic()
        params = ["termux-call-log", "-l", "100"]
        if page:
            params += ["-o", str(page * 100)]
        resp = termux.API.generic(params)[1]
        if resp:
            for x in resp:
                date = datetime.strptime(x["date"].split(".")[0], "%Y-%m-%d %H:%M:%S")
                if compare_to and compare_to >= date:
                    running = False
                    break
                x["call_type"] = x["type"]
                del x["type"]
                del x["sim_id"]
                x["date"] = date
                raw = RawCall(**x)
                raw.save()
            page += 1
        else:
            break
    return RawCall.load()

def gather_psr_data(psr_id: int):
    pass
