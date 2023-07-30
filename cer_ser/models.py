from django.db import models

# Create your models here.

class Certificate_Owners(models.Model):
  email = models.CharField(max_length=50, primary_key=True)
  password = models.CharField(max_length=50)

class Certificates(models.Model):
  image_url = models.CharField(max_length=255)
  text_color = models.CharField(max_length=50, default = 'red')
  text_pos_top = models.CharField(max_length=255, default = '0')
  text_font_size = models.CharField(max_length=255, default = '20')
  text_pos_right = models.CharField(max_length=255, default = '0')
  text_padding = models.CharField(max_length=255, default = '0')
  signature_color = models.CharField(max_length=50, default = 'red')
  signature_font_size = models.CharField(max_length=255, default = '20')
  signature_pos_top = models.CharField(max_length=255, default = '0')
  signature_pos_left = models.CharField(max_length=255, default = '0')
  signature_padding = models.CharField(max_length=255, default = '0')
  date_color = models.CharField(max_length=50, default = 'red')
  date_pos_top = models.CharField(max_length=255, default = '0')
  date_pos_left = models.CharField(max_length=255, default = '0')
  date_padding = models.CharField(max_length=255, default = '0')
  date_font_size = models.CharField(max_length=255, default = '20')
  token_color = models.CharField(max_length=50, default = 'red')
  owner_email= models.ForeignKey(Certificate_Owners, null=True, on_delete=models.CASCADE)

class Certificate_Tokens(models.Model):
  checksum = models.CharField(max_length=50)
  real_token = models.CharField(max_length=255)



