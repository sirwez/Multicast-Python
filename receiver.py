import socket
import threading
import time
import sys

def send(data, port, addr):
        # Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Make the socket multicast-aware, and set TTL.
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 6)
        # Send the data
        s.sendto(data, (addr, port))
        s.close()

def recvCliente(port, addr, buf_size):
        # Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set some options to make it multicast-friendly
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to the port
        s.bind(('', port))

        # Set some more multicast options
        intf = socket.gethostbyname(socket.gethostname())
        s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))
        s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton(intf))

        # Receive the data, then unregister multicast receive membership, then close the port
        data, sender_addr = s.recvfrom(buf_size)
        s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
        s.close()
        return data

def recvOtherServers(port, addr, buf_size):
        # Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set some options to make it multicast-friendly
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.settimeout(1)

        # Bind to the port
        s.bind(('', port))

        # Set some more multicast options
        intf = socket.gethostbyname(socket.gethostname())
        s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))
        s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton(intf))

        try:
                data, sender_addr = s.recvfrom(buf_size)
        except socket.timeout:
                s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
                s.close()
                return None
        else:        
                s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
                s.close()
                return data

def sinalDeVida(id_maquina):
        while True:
                id = recvOtherServers(10000, "224.0.0.1",1024)
                servidor[int(id_maquina)] = [int(id_maquina), time.time()]
                send(id_maquina.encode('ascii'), 10000, '224.0.0.1')
                if(id != None):
                        id = int(id)
                        if(id >= len(servidor)):# adicionar novo
                                for i in range(len(servidor),id+1):
                                        if(i == id):#
                                                servidor.append([i,time.time()])
                                        else:
                                                servidor.append([i,None])
                        else:#adicionar ja existente no array
                                servidor[id] = [id,time.time()]

def calcular(data):
        expressao = []
        aux =''
        for i in data:
                if( i == '+'):
                        expressao.append(aux)
                        expressao.append('+')
                        aux = ''
                elif(i == '-'):
                        expressao.append(aux)
                        expressao.append('-')
                        aux = ''
                elif( i == '*'):
                        expressao.append(aux)
                        expressao.append('*')
                        aux = ''
                elif(i == '/'):
                        expressao.append(aux)
                        expressao.append('/')
                        aux = ''
                else:
                        aux += i
        expressao.append(aux)

        resposta = 0
        while len(expressao) > 1:
                j = -1
                if('*' in expressao):
                        for i in expressao:
                                j+=1
                                if(i == '*'  and '/' not in expressao[0:j]):
                                        resposta = int(expressao[j-1]) * int(expressao[j+1])
                                        expressao[j-1] = str(resposta)
                                        del expressao[j+1]
                                        del expressao[j]
                j = -1
                if('/' in expressao):
                        for i in expressao:
                                j+=1
                                if(i == '/' and expressao[j+1] != '0'):
                                        resposta = int(expressao[j-1]) // int(expressao[j+1])
                                        expressao[j-1] = str(resposta)
                                        del expressao[j+1]
                                        del expressao[j]
                j = -1
                if('+' in expressao):
                        for i in expressao:
                                j+=1
                                if(i == '+' and '-' not in expressao[0:j] and '*' not in expressao[j:] and '/' not in expressao[j:]):
                                        resposta = int(expressao[j-1]) + int(expressao[j+1])
                                        expressao[j-1] = str(resposta)
                                        del expressao[j+1]
                                        del expressao[j]
                j = -1
                if('-' in expressao):
                        for i in expressao:
                                j+=1
                                if(i == '-' and '*' not in expressao[0:j] and '/' not in expressao[0:j] and '*' not in expressao[j:] and '/' not in expressao[j:]):
                                        resposta = int(expressao[j-1]) - int(expressao[j+1])
                                        expressao[j-1] = str(resposta)
                                        del expressao[j+1]
                                        del expressao[j]

        return str(resposta)

id_maquina = str(sys.argv[1])
print('Server '+id_maquina+' iniciado')
servidor =  []
for i in range(int(id_maquina)+1):
        servidor.append([i,None])
threading.Thread(target=sinalDeVida,args=(id_maquina,)).start()
while True:
        #recebe dado do cliente
        data = recvCliente(5007, "224.1.1.1",1024).decode('ascii')
        
        for i in range(len(servidor)):
                if servidor[i][1] != None and (time.time() - servidor[i][1]) < 3:#alguem esta apto a responder
                        if(servidor[i][0] == int(id_maquina)):#eh esta maquina?
                                print(id_maquina+' respondeu')
                                resposta = calcular(str(data))
                                mensagem = "Maquina " +id_maquina+' - resultado: '+resposta
                                send(mensagem.encode('ascii'), 5007, '224.1.1.1')
                                break
                        else:#nao eh esta maquina
                                break