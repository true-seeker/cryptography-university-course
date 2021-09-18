import unittest

from magma import Number64, CipherKey, pi_transform, modulo_addition, left_num_shift


class TestMagma(unittest.TestCase):
    def setUp(self) -> None:
        self.number = Number64(0xfedcba9876543210)
        self.key = CipherKey(0xffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff)

    def test_pi_transform(self):
        self.assertEqual(pi_transform(self.number.left_part), 0x233b57ee)

    def test_modulo_addition(self):
        self.assertEqual(modulo_addition(self.number.left_part, self.number.right_part, 2 ** 32), 0x7530eca8)

    def test_num_shift(self):
        self.assertEqual(left_num_shift(self.number.left_part, 11), 0xe5d4c7f6)

    def test_encrypt(self):
        self.assertEqual(self.number.magma_crypt(self.key, False).get_as_int(), 0x4ee901e5c2d8ca3d)

    def test_encrypt_decrypt(self):
        a = self.number.magma_crypt(self.key, False)
        b = a.magma_crypt(self.key, True)
        self.assertEqual(b.get_as_int(), self.number.get_as_int())


if __name__ == '__main__':
    unittest.main()
