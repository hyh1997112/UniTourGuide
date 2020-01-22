from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Customer/Tourist: (name, email, user)
# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.id) + " " + (self.user.first_name + " " + self.user.last_name).lower()


# Guide: 
# (name, email, studentID, user, numberOfTours, rating, feedback, price(daily))
class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    studentID = models.CharField(max_length=20)
    num_of_tours = models.IntegerField(default=0)
    rating = models.FloatField(null=True, blank=True)
    # feedback by tour
    price = models.FloatField(null=True, blank=True)
    picture = models.ImageField(upload_to='pictures_gui/', default='pictures_gui/sample_guide.png')
    description = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.id) + " " + (self.user.username + " " + self.user.first_name + " " + self.user.last_name).lower()

# Manager: (name, email)
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + " " + (self.user.username + " " + self.user.first_name + " " + self.user.last_name).lower()


# School:
# (name, city, state, guides(many-to-many))
class School(models.Model):
    display = models.BooleanField(default=False)
    recommand = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    guides = models.ManyToManyField(Guide)
    description = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(upload_to='pictures_sch/', null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.name.lower()

# Tour:
# (date, school, guide(ForeignKey), customer(ManyToMany), condition(charField (‘pending’, ‘accepted’, ‘completed’, ‘cancelled’, ‘declined’))
class Tour(models.Model):
    date = models.DateField()
    school = models.ForeignKey(School, null=True, blank=True, on_delete=models.SET_NULL)
    guide = models.ForeignKey(Guide, null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    DECLINED = 'declined'
    CONDITION_CHOICES = [(PENDING, 'pending'), (ACCEPTED, 'accepted'), (COMPLETED, 'completed'), (CANCELLED, 'cancelled'), (DECLINED, 'declined')]
    condition = models.CharField(max_length=11, choices=CONDITION_CHOICES)
    feedback = models.CharField(max_length=100, null=True, blank=True)
    rating = models.FloatField(blank=True,null=True)

    def __str__(self):
        return str(self.id)

# GuideApplication
class GuideApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='application')
    email = models.EmailField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    studentID = models.CharField(max_length=20)
    document = models.ImageField(upload_to='pictures_gui/', null=True, blank=True)
    PENDING = 'pending'
    APPROVED = 'approved'
  
    CONDITION_CHOICES = [(PENDING, 'pending'), (APPROVED, 'approved')]
    condition = models.CharField(max_length=11, choices=CONDITION_CHOICES)