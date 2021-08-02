# import random
# import socket
#
# from bitarray import bitarray
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((socket.gethostname(), 3000))
#
# s.listen(5)
#
# msg = ''
#
# # 01100010 01100001
# # 00100010 01100001
#
#
#
# while True:
#     client_socket, address = s.accept()
#     print(f"Connection from {address} has been established!")
#     client_socket.send(bytes("welcome to the server!", "utf-8"))
#
# ENCODING = 'utf8'
# NOISE_MINMAX = [0, 10000]
# NOISE_PROBABILITY = 0.01
#
#
# class Emisor:
#     def __init__(self):
#         self.functions = [
#             self.enviar_cadena,
#             self.enviar_cadena_segura,
#             self.agregar_ruido,
#             # self.enviar_objeto
#         ]
#         previous_result = ''
#
#         for index, function in enumerate(self.functions):
#             previous_result = function(previous_result) if index != 0 else function()
#             print(previous_result or '')
#
#         b = previous_result.tobytes()
#         print(b)
#
#     def enviar_cadena(self) -> str:
#         '''
#         Grabs a string from the user and accepts it as long as it is not empty. Passes it along to the next function
#
#         :return:
#             None
#         '''
#         to_be_sent = ''
#         while len(to_be_sent) == 0:
#             to_be_sent = input('Your message:\n>>> ')
#         return to_be_sent
#
#     def enviar_cadena_segura(self, message) -> bitarray:
#         a = bitarray()
#         a.frombytes(bytes(message, ENCODING))
#         return a
#
#     def agregar_ruido(self, bitarray_arg) -> bitarray:
#         minimum, maximum = NOISE_MINMAX
#         percent = int(maximum * NOISE_PROBABILITY)
#         temp = bitarray_arg.copy()
#         for index, bit in enumerate(bitarray_arg):
#             chance = random.randint(minimum, maximum)
#             if chance <= percent:
#                 temp[index] = not temp[index]
#         return temp
#
#     def enviar_objeto(self, message) -> bool:
#         pass
#
#
# Emisor()
#
#
# class Receptor:
#     def __init__(self):
#         pass
#
#     def recibir_objeto(self):
#         pass
#
#     def recibir_cadena_segura(self):
#         pass
#
#     def recibir_cadena(self):
#         pass
