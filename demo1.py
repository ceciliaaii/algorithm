# python雪花算法的实现
import time


class InvalidSystemClock(Exception):
    pass


WORKER_ID_BITS = 5
DATA_CENTER_ID_BITS = 5
SEQUENCE_BITS = 12

MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
MAX_DATA_CENTER_ID = -1 ^ (-1 << DATA_CENTER_ID_BITS)

WORKER_ID_SHIFT = SEQUENCE_BITS
DATA_CENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATA_CENTER_ID_BITS

SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

TM_EPOCH = 1288834974657


class IdWorker(object):
    def __init__(self, worker_id, data_center_id, sequence=0):
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError("worker_id can't be greater than %d or less than 0" % MAX_WORKER_ID)
        if data_center_id > MAX_DATA_CENTER_ID or data_center_id < 0:
            raise ValueError("data_center_id can't be greater than %d or less than 0" % MAX_DATA_CENTER_ID)
        self.worker_id = worker_id
        self.data_center_id = data_center_id
        self.sequence = sequence
        self.last_timestamp = -1

    def __gen_time(self):
        return int(time.time() * 1000)

    def get_id(self):
        timestamp = self.__gen_time()
        if timestamp < self.last_timestamp:
            raise InvalidSystemClock("Clock moved backwards.  Refusing to generate id for %d milliseconds" % (
                    self.last_timestamp - timestamp))
        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self.til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        new_id = ((timestamp - TM_EPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.data_center_id << DATA_CENTER_ID_SHIFT) | (
                self.worker_id << WORKER_ID_SHIFT) | self.sequence
        return new_id

    def til_next_millis(self, last_timestamp):
        timestamp = self.__gen_time()
        while timestamp <= last_timestamp:
            timestamp = self.__gen_time()
        return timestamp


if __name__ == '__main__':
    worker = IdWorker(1, 1)
    # try:
    #     while True:
    #         print(worker.get_id())
    # except InvalidSystemClock as e:
    #     print(e)
    print(worker.get_id())
