import platform;
import socket;
import qrcode;

import time

def sleep(t = 1):
    def sleepT(func):
        async def sleepTs():
            time.sleep(t)
            return await func()
        return sleepTs
    return sleepT
# 获取本机信息
def get_sys_info():
    sys_info = platform.uname()._asdict();
    sys_info['platform'] = platform.platform();
    print(sys_info);
    return sys_info;

# 获取本机ip
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        s.connect(('8.8.8.8', 80));
        ip = s.getsockname()[0];
    finally:
        s.close();

    return ip

def print_ip_qrcode(port):
    ip = get_ip();
    address = f'http://{ip}:{port}';
    qr = qrcode.QRCode();
    qr.add_data(address);
    qr.print_ascii(invert=True);
