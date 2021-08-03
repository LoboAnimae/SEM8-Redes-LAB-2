from bitarray import bitarray


def perform_reduction( r: list, w: str ):
    r[ 0 ] += ord( w )
    r[ 1 ] += r[ 0 ]
    r[ 2 ] += 1
    return None


def perform_mod( ref: list, m ):
    ref[ 0 ] %= m
    ref[ 1 ] %= m
    return None


class Fletcher:
    def __init__( self, message: str, mod: int = 65535, preferred_length: int = 512 ):
        self.length = len( message )
        self.message = message
        self.user_mod = mod
        self.block_length = preferred_length
        self.result = None

    def operate( self, ref, message, range_used ):
        [ perform_reduction( ref, message[ ref[ 2 ] ] ) for _ in range( range_used ) ]
        perform_mod( ref, self.user_mod )

    # Fletcher 32 bit
    # Based on tutorial on https://www.tutorialspoint.com/fletcher-s-checksum
    def get_fletcher( self ):
        # First, grab the length and initialize the checksums in local
        n = self.length
        # To pass by reference, create a list
        ref_list = [ 0, 0, 0 ]
        # For each data block, add bi to c1
        while True:
            if n < self.block_length:
                break
            self.operate( ref_list, self.message, self.block_length )
            n -= self.block_length
        self.operate( ref_list, self.message, n )

        z, o, c = ref_list
        self.result = (o << 16 | z)
        return self
