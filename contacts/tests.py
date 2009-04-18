import unittest
from contacts import models 

class AnimalTestCase(unittest.TestCase):
  def setUp(self):
    self.lion = Animal.objects.create(name="lion", sound="roar")
    self.cat = Animal.objects.create(name="cat", sound="meow")

  def testSpeaking(self):
    self.assertEquals(self.lion.speak(), 'The lion says "roar"')
    self.assertEquals(self.cat.speak(), 'The cat says "meow"')

