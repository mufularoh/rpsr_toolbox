from datetime import datetime
from dataclasses import dataclass 
import sqlite3

connection = sqlite3.connect("./database.db")
cursor = connection.cursor()

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

    def create(self, number: int, *, started: datetime | None, lat: float | None, lng: float | None)

    def refresh(self):
        PSR.ensure_db()
        cursor.execute("select * from psr order by started desc")
        for row in cursor.fetchall():
            raw = list(row)
            raw[1] = datetime.strptime(raw[1], "%Y-%m-%d %H:%M:%S")
            self.psrs.append(PSR(*raw))

def get_shift() -> tuple[datetime, datetime]:
    return (
        datetime(2026, 9, 28, 21, 0),
        datetime(2026, 9, 29, 21, 0)
    )
