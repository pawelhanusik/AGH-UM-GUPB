class Aaa:
    def d(self, int_to_decrypt, key):
        ints = []
        while int_to_decrypt > 0:
            ints.append(int_to_decrypt & 0xff)
            int_to_decrypt >>= 8
        ints.reverse()

        seed = key

        def rc():
            nonlocal seed
            seed = (seed * 1103515245 + 12345) & 0x7fffffff
            return seed
        
        ret = ""

        for i in ints:
            ret += chr(i ^ (rc() % 255))

        return ret

    def e(self, str_to_encrypt, key):
        ints = []

        for c in str_to_encrypt:
            ints.append(ord(c))

        seed = key

        def rc():
            nonlocal seed
            seed = (seed * 1103515245 + 12345) & 0x7fffffff
            return seed
        
        ret = 0

        for i in ints:
            ret <<= 8
            ret += i ^ (rc() % 255)

        return ret

aaa = Aaa()
print(aaa.d(947871564346996264452, 32378946584))
print(aaa.e("AlphaGUPB", 32378946584))
