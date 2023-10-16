import unittest

from parsing_moves_gpt import extract_move_chatgpt


class TestExtractMoveMethods(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(extract_move_chatgpt("1... c5"), "c5")
        self.assertEqual(extract_move_chatgpt("1... c5 2. Nf6"), "c5")
        self.assertEqual(extract_move_chatgpt("1. e4"), "e4")
        self.assertEqual(extract_move_chatgpt("e4 e6"), "e4")
        self.assertEqual(extract_move_chatgpt("2. Ng1f3"), "Ng1f3")

    def test_ten(self):
        self.assertEqual(extract_move_chatgpt("10. Bf4"), "Bf4") # the trick is that 10 is composed of two digits
        self.assertEqual(extract_move_chatgpt("10... f7"), "f7") # the trick is that 10 is composed of two digits

    def test_hundred(self):
        self.assertEqual(extract_move_chatgpt("100. Bf4"), "Bf4") # the trick is that 100 is composed of three digits
        self.assertEqual(extract_move_chatgpt("120... Bf4"), "Bf4") # the trick is that 10 is composed of two digits

    def test_promotion(self):
        self.assertEqual(extract_move_chatgpt("75. b8=Q"), "b8=Q")
        self.assertEqual(extract_move_chatgpt("75. b8=R"), "b8=R")
        self.assertEqual(extract_move_chatgpt("79... b8=Q"), "b8=Q")
        self.assertEqual(extract_move_chatgpt("79... b8=Q Nf6"), "b8=Q")

    def test_doublenumber(self):
        self.assertEqual(extract_move_chatgpt("1...e5 1"), "e5")
        self.assertEqual(extract_move_chatgpt("1...e5 2."), "e5")
        self.assertEqual(extract_move_chatgpt("11...Nf6 2."), "Nf6")


    def test_check(self):
        self.assertEqual(extract_move_chatgpt("10... cxd2+"), "cxd2+")
        self.assertEqual(extract_move_chatgpt("10... cxd2+ 11."), "cxd2+")
        self.assertEqual(extract_move_chatgpt("10... Bd8+ 11. Nf6"), "Bd8+")
        self.assertEqual(extract_move_chatgpt("10... Bd8+ 11. Nxf6#"), "Bd8+")

    def test_checkunfinishedpromotion(self):
        self.assertEqual(extract_move_chatgpt("5. hxg8= 5."), "hxg8=Q")

    def test_checkfinishedpromotion(self):
        self.assertEqual(extract_move_chatgpt("5. hxg8=Q 6."), "hxg8=Q")

    # Test the revised implementation
    test_cases = [
        ("1... c5", "c5"),
        ("1... c5 2. Nf6", "c5"),
        ("1. e4", "e4"),
        ("e4 e6", "e4"),
        ("2. Ng1f3", "Ng1f3"),
        ("10. Bf4", "Bf4"),
        ("10... f7", "f7"),
        ("100. Bf4", "Bf4"),
        ("120... Bf4", "Bf4"),
        ("120... Bf4 121. Ng6", "Bf4"), 
        ("10. O-O", "O-O"),
        ("10. O-O-O", "O-O-O"),
         ("10... O-O-O", "O-O-O"),
    ]

    # Additional test cases
    def test_additional_cases(self):
        for test_case in self.test_cases:
            with self.subTest(test_case=test_case[0]):
                self.assertEqual(extract_move_chatgpt(test_case[0]), test_case[1])



unittest.main()