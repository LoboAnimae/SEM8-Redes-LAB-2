"""
Implements the error detection checksum algorithm
"""


def perform_reduction( r: list, w: str ) -> None:
    """
    Grabs a reference to a list and uses it to work like a c algorithm

    :param r: The list
    :param w: The input value for the first checksum. String. Taken from the literal message.
    :return: None
    """
    r[ 0 ] += ord( w )
    r[ 1 ] += r[ 0 ]
    r[ 2 ] += 1
    return None


def perform_mod( ref: list, m: int ) -> None:
    """
    Performs a mod on both of the checksums

    :param ref: The list with the checksums
    :param m: The mod
    :return:
    """
    ref[ 0 ] %= m
    ref[ 1 ] %= m
    return None


class Fletcher:
    """
    Implements the error detection checksum algorithm
    """
    def __init__( self, message: str, mod: int = 65535, preferred_length: int = 512 ):
        """
        Requires a message to work

        :param message: Message to be check-summed
        :param mod: The mod to be used. Taken from an example in GeeksforGeeks.
        :param preferred_length: The preferred length of the block.
        """
        self.length = len( message )
        self.message = message
        self.user_mod = mod
        self.block_length = preferred_length
        self.result = None

    def operate( self, ref: list, message: str, range_used: int ):
        """
        QOL function that performs a reduction and a mod on the checksums

        :param ref: The reference to a list
        :param message: The message to be checksummed
        :param range_used: The range used for the reduction
        :return:
        """
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
        # Shift based on block size (32 / 2 = 16-> Block size of the checksum)
        self.result = (o << 16 | z)
        return self
