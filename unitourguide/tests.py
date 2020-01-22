from django.test import TestCase
from .models import Guide, Manager, Tour, School, GuideApplication

# Create your tests here.
class ModelTests(TestCase):
    def setUp(self):
        guide = Guide(studentID = "123456", num_of_tours = 3, rating = 4.8, 
        price = 30, picture = 'pictures_gui/sample_guide.png', 
        description = "I am a good guide!")
        
# Guide: 
# (user, studentID, num_of_tours, rating, price, picture, description)
    def test_guide_model(self):
        guide = Guide(studentID = "123456", num_of_tours = 3, rating = 4.8, 
        price = 30, picture = 'pictures_gui/sample_guide.png', 
        description = "I am a good guide!")
        school = School(name = "New York University", city = "New York City", 
        state = "New York", description = "I am NYU")
        self.assertEqual("123456", guide.studentID)
        self.assertEqual(3, guide.num_of_tours)
        self.assertEqual(4.8, guide.rating)
        self.assertEqual(30, guide.price)
        self.assertEqual('pictures_gui/sample_guide.png', guide.picture)
        self.assertEqual("I am a good guide!", guide.description)

# School:
    def test_school_model(self):
        guide = Guide(studentID = "123456", num_of_tours = 3, rating = 4.8, 
        price = 30, picture = 'pictures_gui/sample_guide.png', 
        description = "I am a good guide!")
        school = School(name = "New York University", city = "New York City", 
        state = "New York", description = "I am NYU")
        self.assertEqual("New York University", school.name)
        self.assertEqual("New York City", school.city)
        self.assertEqual("New York", school.state)
        self.assertEqual("I am NYU", school.description)