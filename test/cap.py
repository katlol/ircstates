import unittest
import ircstates, irctokens

class CapTestLS(unittest.TestCase):
    def test_one_line(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS :a b"))
        self.assertEqual(server.caps, {"a": None, "b": None})

    def test_two_lines(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS * :a b"))
        self.assertEqual(server.caps, None)
        server.parse_tokens(irctokens.tokenise("CAP * LS :c"))
        self.assertEqual(server.caps, {"a": None, "b": None, "c": None})

    def test_values(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS :a b= c=1"))
        self.assertEqual(server.caps, {"a": None, "b": None, "c": "1"})

class CapTestACK(unittest.TestCase):
    def test_one_line(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS :a b"))
        server.parse_tokens(irctokens.tokenise("CAP * ACK :a b"))
        self.assertEqual(server.agreed_caps, ["a", "b"])

    def test_two_lines(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS :a b c"))
        server.parse_tokens(irctokens.tokenise("CAP * ACK * :a b"))
        server.parse_tokens(irctokens.tokenise("CAP * ACK :c"))
        self.assertEqual(server.agreed_caps, ["a", "b", "c"])

    def test_not_ls(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS a"))
        server.parse_tokens(irctokens.tokenise("CAP * ACK b"))
        self.assertEqual(server.agreed_caps, [])

class CapTestNEW(unittest.TestCase):
    def test_no_ls(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * NEW :a"))
        self.assertEqual(server.caps, None)

    def test_one(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS :a"))
        server.parse_tokens(irctokens.tokenise("CAP * NEW :b"))
        self.assertEqual(server.caps, {"a": None, "b": None})

    def test_two(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS :a"))
        server.parse_tokens(irctokens.tokenise("CAP * NEW :b c"))
        self.assertEqual(server.caps, {"a": None, "b": None, "c": None})

class CapTestDEL(unittest.TestCase):
    def test_not_acked(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * DEL a"))

    def test_one_ls(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS :a"))
        server.parse_tokens(irctokens.tokenise("CAP * ACK :a"))
        server.parse_tokens(irctokens.tokenise("CAP * DEL :a"))
        self.assertEqual(server.caps, {})
        self.assertEqual(server.agreed_caps, [])

    def test_two_ls(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS :a b"))
        server.parse_tokens(irctokens.tokenise("CAP * ACK :a b"))
        server.parse_tokens(irctokens.tokenise("CAP * DEL :a"))
        self.assertEqual(server.caps, {"b": None})
        self.assertEqual(server.agreed_caps, ["b"])

    def test_two_del(self):
        server = ircstates.Server("test")
        server.parse_tokens(irctokens.tokenise("CAP * LS :a b"))
        server.parse_tokens(irctokens.tokenise("CAP * ACK :a b"))
        server.parse_tokens(irctokens.tokenise("CAP * DEL :a b"))
        self.assertEqual(server.caps, {})
        self.assertEqual(server.agreed_caps, [])

