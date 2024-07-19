from django.db import models

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	username=models.CharField(max_length=100)
	mobile=models.PositiveIntegerField()
	email=models.EmailField()
	password=models.TextField(max_length=100)

	def __str__(self):
		return self.fname+" "+self.lname


class InsuranceApplication(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    insurance_type = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

class PolicyHolder(models.Model):
    INSURANCE_TYPES = [
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
        ('auto', 'Auto Insurance'),
        ('home', 'Home Insurance'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insurance_type = models.ForeignKey(InsuranceApplication, on_delete=models.CASCADE)
    insurance_type = models.CharField(max_length=50, choices=INSURANCE_TYPES)
    approved = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('disapproved', 'Disapproved'), ('pending', 'Pending')], default='pending')
    insurance_applications = models.ManyToManyField(InsuranceApplication)
    def __str__(self):
        return self.user.username + self.get_insurance_type_display()
    def get_absolute_url(self):
        return f"/policyholder/{self.id}/"
