"""
    CS5001_5003 Fall 2023 SV
    final project
    Linyan Fu
"""


import unittest
import pygame
from flappybird import Bird


class TestBird(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.bird = Bird()

    def test_initial_state(self):
        """Test the initial state of the bird"""
        self.assertEqual(self.bird.rect.center, (100, 250))
        self.assertEqual(self.bird.gravity, 0)
        self.assertFalse(self.bird.flap)
        self.assertTrue(self.bird.alive)

    def test_update_no_flap(self):
        """Test the bird's update method without flapping"""
        self.bird.update({pygame.K_SPACE: False})
        self.assertGreater(self.bird.gravity, 0)
        self.assertFalse(self.bird.flap)

    def test_update_with_flap(self):
        """Test the bird's update method with flapping"""
        self.bird.update({pygame.K_SPACE: True})
        self.assertEqual(self.bird.gravity, -7)
        self.assertTrue(self.bird.flap)

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()
