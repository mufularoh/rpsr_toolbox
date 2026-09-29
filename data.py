from typing import Self
from datetime import datetime
from dataclasses import dataclass 
import sqlite3

connection = sqlite3.connect("./database.db")
cursor = connection.cursor()

@dataclass
class RawCall:
    name: str 
    phone_number: str 
    call_type: str 
    date: datetime
    duration: str

    def save(self):
        cursor.execute("""insert into calls(
            name, phone_number, type, date, duration
        ) values(
            ?, ?, ?, ?, ?
        )""", (
                self.name, self.phone_number, self.call_type,
                self.date, self.duration
             )
        )
        connection.commit()

    @classmethod
    def load(cls) -> list[Self]:
        ret = []
        cls.ensure_db()
        cursor.execute("select name, phone_number, type, date, duration from calls")
        for row in cursor.fetchall():
            kwargs = {
                "name": row[0], "phone_number": row[1], "call_type": row[2], 
                "date": datetime.strptime(row[3].split(".")[0], "%Y-%m-%d %H:%M:%S"),
                "duration": row[4]
            }
            ret.append(cls(**kwargs))
        return sorted(ret, key=lambda x: x.date, reverse=True)
    
    @staticmethod
    def ensure_db():
        cursor.execute("""create table if not exists calls(
            date str not null primary key,
            name str,
            phone_number str,
            type str,
            duration str
        )""")
        connection.commit()

@dataclass
class PSR:
    id: int
    started: datetime 
    lat: float | None
    lng: float | None
    active: bool

    @staticmethod
    def ensure_db():
        cursor.execute("""create table if not exists psr(
            id int not null primary key,
            started datetime,
            lat float,
            lng float,
            active int
        )""")
        connection.commit()

    def save(self):
        self.ensure_db()
        cursor.execute("""insert into psr(
            id, started, lat, lng, active
        ) values( ?, ?, ?, ?, ?) 
        on conflict(id) do update 
            set started=excluded.started, lat=excluded.lat, lng=excluded.lng, active=excluded.active""", (
            self.id, self.started, self.lat, self.lng, self.active
        ))
    connection.commit()

class PSRList:
    psrs: list[PSR]

    def __init__(self):
        self.psrs = []
        self.refresh()

    def create(self, id: int, *, started: datetime | None = None, lat: float | None = None, lng: float | None = None):
        x = PSR(id, started or datetime.now(), lat, lng, True)
        x.save()
        self.refresh()

    def refresh(self):
        PSR.ensure_db()
        cursor.execute("select * from psr order by started desc")
        for row in cursor.fetchall():
            raw = list(row)
            raw[1] = datetime.strptime(raw[1].split(".")[0], "%Y-%m-%d %H:%M:%S")
            self.psrs.append(PSR(*raw))

def get_shift() -> tuple[datetime, datetime]:
    return (
        datetime(2026, 9, 28, 21, 0),
        datetime(2026, 9, 29, 21, 0)
    )
