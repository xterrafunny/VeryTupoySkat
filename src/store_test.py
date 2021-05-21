import unittest
from os import system
from persistent_store import KeyValueStore, KeyStore


def clean_file(file_name: str):
    with open(file_name, "w") as file:
        file.write("")


class MyTestCase(unittest.TestCase):
    def test_simple_key_value(self):
        clean_file("temp")
        kv = KeyValueStore("temp")
        kv.store("key", "value")
        self.assertEqual("value", kv.load("key"))
        del kv
        kv = KeyValueStore("temp")
        self.assertEqual("value", kv.load("key"))
        del kv
        clean_file("temp")
        system("rm temp")

    def test_simple_key(self):
        clean_file("temp")
        k = KeyStore("temp")
        k.store("key")
        self.assertTrue("key" in k)
        del k
        k = KeyStore("temp")
        self.assertTrue("key" in k)
        del k
        clean_file("temp")
        system("rm temp")


if __name__ == '__main__':
    unittest.main()
