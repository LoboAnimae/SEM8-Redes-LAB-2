import math
from bitarray import bitarray


class Hamming:

    def __init__(self, message):
        """
        Defining variables to use in the hamming algorithm
        """
        self.bitarray = bitarray()
        self.bitarray.frombytes(bytearray(message.encode()))
        self.length = len(self.bitarray)
        self.get_redundant_bits()
        self.result = None

    def get_redundant_bits(self) -> int:
        """
        We obtain de redundance bits and assign them to the bitarray
        """
        parityindex = 1
        for i in range(len(self.bitarray)):
            print("Insertando en: " + str(parityindex-1))
            self.bitarray.insert((parityindex-1), 0)
            parityindex *= 2
    # Positions that are powers of two get a redundancy bit

    def implement_redundant_bits(self, original_bitarray):
        parityindex = 1

        """
        Obtaining values for the redundance bits and assigning them
        """
        for i in range(int(math.sqrt(len(self.bitarray))) + 1):
            print('parityindex: ' + ' ' + str(parityindex))
            ver = 0
            print("a[" + str(i) + "] = " + str(self.bitarray[i]))

            for j in range(parityindex - 1, len(self.bitarray), parityindex*2):

                count = 0
                for k in range(parityindex):
                    if((j+count) < len(self.bitarray)):
                        print("count: " + str(j + count))
                        print("value: " + str(self.bitarray[j + count]))
                        ver = (ver + self.bitarray[(j + count)]) % 2
                        count += 1
            print('ver: ' + str(ver))
            self.bitarray[(parityindex-1)] = ver
            parityindex *= 2
            self.result = self.bitarray
            self.message = self.bitarray

        return(self)
