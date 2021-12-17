import unittest
from unittest.mock import patch
import nfs
import pygame
class test(unittest.TestCase):

    @patch('pygame.key.get_pressed')
    def test(self, test_patch):
        """Патчим функцию pygame.key.get_pressed
        и заставляем его думать, что нажата стрелочка вправо

        Тест проверяет работает ли меню
        """
        test_patch.return_value = {pygame.K_ESCAPE : True, pygame.K_RETURN : False}
        with self.assertRaises(SystemExit) as exit:
            nfs.menu()
        self.assertEqual(exit.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
