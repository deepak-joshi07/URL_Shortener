import time
from threading import Lock
from datetime import datetime , timezone


SNOWFLAKE_EPOCH = int(
    datetime(2025, 12, 1, tzinfo=timezone.utc).timestamp() * 1000
    )

class SnowflakeGenerator: 

    def __init__(self , machine_id : int): 
        self.machine_id = machine_id

        if not 0 <= machine_id <= 1023:
            raise ValueError("machine_id must be between 0 and 1023")
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = Lock()
        self.epoch = SNOWFLAKE_EPOCH

    def generate_id(self)->int:

        with self.lock:
            timestamp = (time.time_ns()//1_000_000)-self.epoch

            if timestamp < self.last_timestamp:
                raise RuntimeError("Clock moved backwards")
            
            if timestamp == self.last_timestamp:
                self.sequence += 1

                if self.sequence > 4095: 
                    while timestamp <= self.last_timestamp:
                        timestamp = (time.time_ns()// 1_000_000)-self.epoch
                    self.sequence = 0
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            snowflake = (
                (timestamp<<22)
                | (self.machine_id<<12)
                | self.sequence
            )

        return snowflake


id_generator = SnowflakeGenerator(machine_id=1)