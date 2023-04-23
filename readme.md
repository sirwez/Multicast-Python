
O código é composto por dois arquivos: `sender.py` e `receiver.py`. Ambos utilizam sockets para realizar envio e recebimento de dados através do protocolo multicast.

## Receiver.py

O arquivo `receiver.py` contém o código para o receptor (ou receptor) em um ambiente multicast. Este código é executado por cada máquina na rede, permitindo a comunicação entre todas as máquinas na rede multicast. 

### `send(data, port, addr)`

Esta função é usada para enviar dados para a rede multicast. Os parâmetros `data`, `port` e `addr` são dados para enviar, o número da porta e o endereço IP de multicast, respectivamente. O `socket` é criado para enviar os dados, e o `socket` é fechado depois que os dados são enviados.

### `recvCliente(port, addr, buf_size)`

Esta função é usada para receber dados na rede multicast. Os parâmetros `port`, `addr` e `buf_size` são o número da porta, o endereço IP de multicast e o tamanho do buffer para os dados recebidos, respectivamente. O `socket` é criado para receber os dados, e é definido algumas opções para tornar o `socket` amigável para multicast. Em seguida, o `socket` é vinculado à porta e definido mais opções multicast. Os dados são recebidos e o `socket` é fechado.

### `recvOtherServers(port, addr, buf_size)`

Esta função é semelhante à `recvCliente`, mas tem um tempo limite de um segundo. Se nenhum dado for recebido dentro do tempo limite, a função retornará `None`. Caso contrário, os dados são tratados como em `recvCliente`. 

### `sinalDeVida(id_maquina)`

Esta função é executada em uma thread separada e é usada para enviar um sinal de vida periódico para a rede multicast. O parâmetro `id_maquina` é o ID da máquina. A função aguarda a recepção de um sinal de vida de outras máquinas na rede multicast, em seguida, atualiza o estado de cada máquina, adicionando-a à lista de máquinas ou atualizando seu tempo de vida. Em seguida, um sinal de vida é enviado para a rede multicast contendo o ID da máquina. 

### `calcular(data)`

Esta função é usada para avaliar uma expressão matemática que é enviada para a rede multicast. O parâmetro `data` é a expressão a ser avaliada. A expressão é analisada e avaliada, com o resultado sendo retornado. A função pode avaliar expressões que contêm adição, subtração, multiplicação e divisão. 

Essas são as funções do arquivo `receiver.py` que permitem a comunicação em uma rede multicast.

sender.py
- `send(data, port, addr)` - função responsável por enviar uma mensagem para o endereço multicast e porta especificados.
    - `data` (bytes) - mensagem a ser enviada, em formato de bytes.
    - `port` (int) - porta utilizada para envio da mensagem.
    - `addr` (str) - endereço multicast utilizado para envio da mensagem.
- `recv(port, addr, buf_size)` - função responsável por receber uma mensagem de um endereço multicast e porta especificados.
    - `port` (int) - porta utilizada para recebimento da mensagem.
    - `addr` (str) - endereço multicast utilizado para recebimento da mensagem.
    - `buf_size` (int) - tamanho máximo do buffer utilizado para receber a mensagem.

Exemplo de uso:
```python
# Enviar uma mensagem
mensagem = input('Digite a expressao: ')
send(mensagem.encode('ascii'), 5007, '224.1.1.1')

# Receber uma mensagem
data = recv(5007, "224.1.1.1", 1024).decode('ascii')
print(data)
```

O processo de envio de mensagens utiliza a porta 5007 e o endereço multicast "224.1.1.1". Já o processo de recebimento utiliza a mesma porta e endereço multicast, mas é necessário configurar algumas opções adicionais para que o socket possa receber as mensagens multicast corretamente.

O código foi escrito em Python 3. É importante ressaltar que o uso de multicast requer uma configuração adequada da rede, e nem todos os ambientes suportam essa funcionalidade.
