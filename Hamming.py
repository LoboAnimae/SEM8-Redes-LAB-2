class Hamming:
    """
    According to tutorialspoint.com/error-correcting-codes-hamming-codes
        Step 1 - Calculation of the number of redundant bits
        Step 2 - Positioning the redundant bits
        Step 3 - Calculating the values of each redundant bit
    """
    def __init__(self, bit):
        self.bitarray = bit
        self.length = len(bit)
        self.redundant_bits = self.get_redundant_bits()

    '''
    Redundancy Bits -> 2 ** P = n + P + 1
        Where:
            P -> Number of redundant bits
            n -> Number of information / Data bits
    '''
    def get_redundant_bits(self) -> int:
        """
        Finds P in the formula
        2^P = n + P + 1

        :return:
            The Number of Redundant Bits
        """
        n = self.length
        for P in range(n):
            if pow(2, P) >= n + P + 1:
                return P

    def init_bit( self ):
        final = 0
        n = self.length
        for i in range(n):
            value = 0
            for j in range(1, n + 1):
                if j & pow( 2, i ) == pow( 2, i ):
                    value = value ^ int(self.bitarray[-j])

    # Positions that are powers of two get a redundancy bit
    def implement_redundant_bits(self, original_bitarray):
        temporal_bitarray = ''
        m = 0
        n = self.length
        P = self.get_redundant_bits()

        # DEPRECATED: Length of new won't be this size
        # for index, bit in enumerate(original_bitarray):
        for i in range(1, n + P + 1):
            if pow(2, m) == i:
                # Shift the current power
                m += 1
                # Insert a 0
                temporal_bitarray += 0
                continue
            temporal_bitarray += original_bitarray[i]

        pass
