import socket

def getIpServer():
    # Lấy địa chỉ IPv4 của máy tính hiện tại
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print('Địa chỉ IPv4 hiện tại:', ip_address)
    return ip_address

def setIpServer(ipServer):
    # Hàm này không còn cần thiết khi không sử dụng MongoDB
    print(f'Đã nhận địa chỉ IP mới: {ipServer}')
    # Nếu cần lưu trữ địa chỉ IP vào file hoặc nơi khác, bạn có thể thêm logic tại đây

# Ví dụ sử dụng
#setIpServer('192.168.174.1')  # Không cần thiết nếu không lưu trữ
getIpServer()