import serial
import time
import hashlib
import binascii
import math
import socket
import json
import struct

USER_AGENT = "TestMiner"
VERSION = [0, 1]

hexlify = binascii.hexlify
unhexlify = binascii.unhexlify


def sha256d(message):
    return hashlib.sha256(hashlib.sha256(message).digest()).hexdigest()


def swap_endian_word(hex_word):
    message = unhexlify(hex_word)
    if len(message) != 4:
        print('Must be 4-byte word')
    return message[::-1]


def swap_endian_words(hex_words):
    message = unhexlify(hex_words)
    if len(message) % 4 != 0: print('Must be 4-byte word aligned')
    return b''.join([message[4 * i: 4 * i + 4][::-1] for i in range(0, len(message) // 4)])


def fpga_mine(prefix, difficulty):
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = 'COM4'
    ser.open()
    if ser.is_open:
        ser.write((prefix + '%02x' % difficulty + '\r').encode('utf-8'))
        print('Calculating hash with prefix ' + prefix)
        print('and difficulty ' + str(difficulty))
        time.sleep(0.5)
        t0 = time.time()
        while ser.in_waiting < 156:
            time.sleep(0.25)
        ser.read(155)
        result = ser.read(8)
        ser.reset_input_buffer()
        hash_check = sha256d(unhexlify((prefix + result.decode('utf-8')).encode('utf-8')))
        print('checked hash is ' + hash_check)
        dt = time.time() - t0;
        # print('used time ' + str(dt) + ' s')
        print('hash rate is %f' % (2 ** 32 / dt))
        difficulty_tmp = math.floor(difficulty / 4)
        if ('0' * difficulty_tmp == hash_check[:difficulty_tmp]):
            return [result, True]

    ser.close()
    '''Try to decrease difficulty by sending false result'''
    if difficulty > 45:
        return ['0'.encode('utf-8'), True]
    return ['0'.encode('utf-8'), False]


class server_handler:
    def __init__(self, url, port, username, password):
        self._url = url
        self._port = port
        self._username = username
        self._password = password
        self._requests = dict()
        self._socket = None
        self._message_id = 1
        self._difficulty = 0
        self._target = 0
        self._worker_name = None
        self._accepted_shares = 0
        self._extranounce1 = 0
        self._extranounce2_size = 0

    def set_difficulty(self, difficulty):
        if difficulty < 0:
            print('Difficulty must be non-negative')
            return

        if difficulty == 0:
            target = 2 ** 256 - 1
        else:
            target = min(int((0xffff0000 * 2 ** (256 - 64) + 1) / difficulty - 1 + 0.5), 2 ** 256 - 1)

        self._difficulty = math.floor(math.log2(difficulty)) + 32
        self._target = '%064x' % target

    def send(self, method, params):
        request = dict(id=self._message_id, method=method, params=params)
        message = json.dumps(request)
        self._socket.send((message + '\n').encode('utf-8'))
        self._requests[self._message_id] = request
        self._message_id += 1

    def mine(self, job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime):
        for extranounce2 in range(0, 0x7fffffff):
            extranounce2_bin = struct.pack('<I', extranounce2)
            coinbase_bin = unhexlify(coinb1.encode('utf-8')) + unhexlify(
                self._extranounce1.encode('utf-8')) + extranounce2_bin + unhexlify(coinb2.encode('utf-8'))
            coinbase_hash_bin = sha256d(coinbase_bin)
            merkle_root_bin = coinbase_hash_bin
            for branch in merkle_branches:
                merkle_root_bin = sha256d(unhexlify(merkle_root_bin) + unhexlify(branch))
            header_prefix_bin = swap_endian_word(version) + swap_endian_words(
                prevhash) + unhexlify(merkle_root_bin) + swap_endian_word(ntime) + swap_endian_word(nbits)
            header_prefix_bin = hexlify(header_prefix_bin).decode('utf-8')
            print('send prefix %s and difficulty %d to FPGA' % (header_prefix_bin, self._difficulty))
            result_nounce = fpga_mine(header_prefix_bin, self._difficulty)
            if result_nounce[1]:
                print('nounce result from FPGA: %s' % result_nounce[0].decode('utf-8'))
                result = dict(
                    job_id=job_id,
                    extranounce2=hexlify(extranounce2_bin).decode('utf-8'),
                    ntime=str(ntime),
                    nounce=result_nounce[0][::-1].decode('utf-8')
                )
                params = [self._worker_name] + [result[k] for k in ('job_id', 'extranounce2', 'ntime', 'nounce')]
                self.send(method='mining.submit', params=params)
                print('Found share: ' + str(params))
                return

    def handle_reply(self):
        data = ""
        while True:
            # Get the next line if we have one, otherwise, read and handle the response
            if '\n' in data:
                (line, data) = data.split('\n', 1)
            else:
                chunk = self._socket.recv(2048)
                print('receive from server: ' + chunk.decode('utf-8'))
                data += chunk.decode('utf-8')
                continue

            reply = json.loads(line)
            if 'id' in reply and reply['id'] in self._requests:
                request = self._requests[reply['id']]

            if reply.get('method') == 'mining.notify':
                if 'params' not in reply or len(reply['params']) != 9:
                    print('Malformed mining.notify message')
                    continue

                (job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime, clean_jobs) = reply['params']
                print('New job %s', job_id)
                self.mine(job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime)
                time.sleep(0.25)


            elif reply.get('method') == 'mining.set_difficulty':
                if 'params' not in reply or len(reply['params']) != 1:
                    print('Malformed ming.set_difficulty message')
                    continue

                (difficulty,) = reply['params']
                self.set_difficulty(difficulty)
                print('Change difficulty to %s' % difficulty)

            elif request:

                if request.get('method') == 'mining.subscribe':
                    if 'result' not in reply or len(reply['result']) != 3 or len(reply['result'][0]) != 2:
                        print('Reply to mining.subscribe is malformed')
                        continue
                    ((mining_notify, subscription_id), extranounce1, extranounce2_size) = reply['result']
                    print('Authorize with username %s' % self._username)
                    print('Password %s' % self._password)
                    self.send(method='mining.authorize', params=[self._username, self._password])
                    self._extranounce1 = extranounce1
                    self._extranounce2_size = extranounce2_size

                elif request.get('method') == 'mining.authorize':
                    if 'result' not in reply or not reply['result']:
                        print('Failed to authenticate worker')

                    self._worker_name = request['params'][0]
                    print('Authorized worker name = %s' % self._worker_name)

                elif request.get('method') == 'mining.submit':
                    if 'result' not in reply or not reply['result']:
                        print('Failed to accept submit')

                    self._accepted_shares += 1
                    print('Accepted shares: %d' % self._accepted_shares)

                else:
                    print('Unhandled message')

            else:
                print('Bad message state')

    def subscribe(self):
        method = 'mining.subscribe'
        params = ["%s/%s" % (USER_AGENT, '.'.join(str(p) for p in VERSION))]
        self.send(method, params)

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._url, self._port))


if __name__ == '__main__':
    url = 'auto.c3pool.org'
    port = 13333
    username = 'user'
    password = 'x'

    sh = server_handler(url, port, username, password)
    sh.connect()
    sh.subscribe()
    sh.handle_reply()

