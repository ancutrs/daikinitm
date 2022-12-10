from base64 import b64encode
import socket
import struct
def DecToByte(Dec, Length):
    return int.to_bytes(Dec, length=Length, byteorder='little', signed=False)
def GetValue(T1,T2,T3,T4):
        T = int(str(T4)+str(T3)+str(T2)+str(T1))
        if T >= 255: T = -1
        return str(T)
def Temperature(T1,T2,T3,T4):
        T = str(struct.unpack('f', int(T1).to_bytes(1, 'big') + int(T2).to_bytes(1, 'big') + int(T3).to_bytes(1, 'big') + int(T4).to_bytes(1, 'big')))
        return T[1:5]
def SetTemperature(T1,T2):
        T = ((int(T2)*256+int(T1))-16840)/8+25
        return str(T)
def Power(P):
        if P=="0" : return "ON"
        if P=="1" : return "OFF"
        if P=="2" : return "Equipment Error(On)"
        if P=="3" : return "Equipment Error(Off)"
        if P=="4" : return "Communication error"
        if P=="5" : return "Maintenance"
        if P=="6" : return "Emergency Stop"
def Products(A):
        if A=="112": return "Indoor"
        if A== "24": return "Fan"
def GenAuthorization(U, P):
        token = b64encode(f"{U}:{P}".encode('utf-8')).decode("ascii")
        return token
class itm:
    def __init__(self,Host,Port,Authorization):
        self.Host = Host
        self.Port = Port
        self.Authorization = Authorization
    def Set(self, Address, Fun, Val):
        Virtual = itm(self.Host, self.Port, self.Authorization)
        Res=Virtual.Status(Address)
        Status = Res.split(",")
        if Status[3]=="Indoor":
            Response = Virtual.SetAir(Address, Fun, Val)
        elif Status[3]=="Fan":
            Response = Virtual.SetFan(Address, Fun, Val)
        else:
            Response = "NG"
        return Response
    def SetAir(self,Address,Fun,Val):
        Host = self.Host
        Port = self.Port
        Authorization = self.Authorization
        data = b""
        data = data + b"POST /cmd/ HTTP/1.1\r\n"
        data = data + b"Content-Length: 160\r\n"
        data = data + b"Authorization: Basic " + bytes(Authorization, 'ascii') + b"\r\n"
        data = data + b"Content-Type: application/octet-stream\r\n\r\n"
        data = data + DecToByte(160, 4)
        data = data + DecToByte(71006, 4)
        data = data + DecToByte(1, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(128, 4)
        data = data + DecToByte(Address, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(1, 4)
        if Fun=="P":
            data = data + DecToByte(1, 4)
            data = data + DecToByte(int(Val), 4)
        else:
            data = data + DecToByte(0, 4)
            data = data + DecToByte(0, 4)
        if Fun == "M":
            data = data + DecToByte(1, 4)
            data = data + DecToByte(int(Val), 4)
        else:
            data = data + DecToByte(0, 4)
            data = data + DecToByte(0, 4)
        if Fun == "T":
            data = data + DecToByte(1, 4)
            data = data + DecToByte(0, 2)
            data = data + DecToByte(16840+(int(Val)-25)*8, 2)
        else:
            data = data + DecToByte(0, 4)
            data = data + DecToByte(0, 2)
            data = data + DecToByte(0, 2)
        for i in range(0, 18):
            data = data + DecToByte(0, 4)
        if Fun == "F":
            data = data + DecToByte(1, 4)
            data = data + DecToByte(int(Val), 4)
        else:
            data = data + DecToByte(0, 4)
            data = data + DecToByte(1, 4)
        if Fun == "S":
            data = data + DecToByte(1, 4)
            data = data + DecToByte(int(Val), 4)
        else:
            data = data + DecToByte(0, 4)
            data = data + DecToByte(1, 4)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((Host, Port))
            s.sendall(data)
            Reply=b""
            Reply = Reply + s.recv(1024)
            s.close()

        if len(Reply) < 195:
            Response = "NG"
        else:
            if Reply[195] == 1:
                Response = "OK"
            else:
                Response = "NG"

        return Response
    def SetFan(self,Address,Fun,Val):
        Host = self.Host
        Port = self.Port
        Authorization = self.Authorization
        data = b""
        data = data + b"POST /cmd/ HTTP/1.1\r\n"
        data = data + b"Content-Length: 68\r\n"
        data = data + b"Authorization: Basic " + bytes(Authorization, 'ascii') + b"\r\n"
        data = data + b"Content-Type: application/octet-stream\r\n\r\n"
        data = data + DecToByte(68, 4)
        data = data + DecToByte(71006, 4)
        data = data + DecToByte(1, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(36, 4)
        data = data + DecToByte(Address, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(1, 4)
        if Fun=="P":
            data = data + DecToByte(1, 4)
            data = data + DecToByte(int(Val), 4)
        else:
            data = data + DecToByte(0, 4)
            data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((Host, Port))
            s.sendall(data)
            Reply=b""
            Reply = Reply + s.recv(1024)
            s.close()
        if len(Reply)<195:
            Response = "NG"
        else:
            if Reply[195]==1:
                Response="OK"
            else:
                Response="NG"
        return Response
    def Status(self,Address):
        Host = self.Host
        Port = self.Port
        Authorization = self.Authorization
        data = b""
        data = data + b"POST /cmd/ HTTP/1.1\r\n"
        data = data + b"Content-Length: 36\r\n"
        data = data + b"Authorization: Basic " + bytes(Authorization, 'ascii') + b"\r\n"
        data = data + b"Content-Type: application/octet-stream\r\n\r\n"
        data = data + DecToByte(36, 4)
        data = data + DecToByte(71004, 4)
        data = data + DecToByte(1, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        data = data + DecToByte(0, 4)
        for i in range(Address, Address+1):
            data = data + DecToByte(i, 4)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((Host, Port))
            s.sendall(data)
            Reply=b""
            Reply = Reply + s.recv(1024)
        s.close()
        data_len=0
        if len(Reply) > 191:
            if int(Reply[191])!=0:
                i = 191
            else:
                i = 192
            while i < len(Reply):
                STS = ""
                l = Reply[i]
                if l==0:
                   break
                e = i + l
                n = 0
                while i < e:
                    STS = STS + str(Reply[i]) + ","

                    n = n + 1
                    i = i + 1
                Status = STS.split(",")
                data_len =int(Status[0])
                if int(Status[4])==Address: break
                if i == len(Reply): break
        if data_len == 112:
            Response = ""
            Response = Response + str(Host)
            Response = Response + ","+str(Port)
            Response = Response + "," + str(Address)
            Response = Response + ","+Products(Status[0])
            Response = Response + ","+Power(Status[8])
            Response = Response + "," + str(Status[12])
            Response = Response + "," + Temperature(0,0,Status[18], Status[19])
            Response = Response + "," + Temperature(Status[32],Status[33],Status[34],Status[35])
            Response = Response + "," + GetValue(Status[64],Status[65],Status[66],Status[67])
            Response = Response + "," + GetValue(Status[68],Status[69],Status[70],Status[71])
        elif data_len == 24:
            Response = ""
            Response = Response + str(Host)
            Response = Response + "," + str(Port)
            Response = Response + "," + str(Address)
            Response = Response + "," + Products(Status[0])
            Response = Response + "," + Power(Status[8])
        else:
            Response = ""
            Response = Response + str(Host)
            Response = Response + "," + str(Port)
            Response = Response + "," + str(Address)
            Response = Response + "," + "Error"
        return Response




