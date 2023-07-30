from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from io import BytesIO
from xhtml2pdf import pisa  
from cer_ser.models import Certificates,Certificate_Tokens,Certificate_Owners
from jose import JWTError, jwt
from datetime import datetime, timedelta
import math

# replace it with your 32 bit secret key
SECRET_KEY = "09d25e094faa****************f7099f6f0f4caa6cf63b88e8d3e7"
# encryption algorithm
ALGORITHM = "HS256"

def tester(request):
    template = loader.get_template('rough.html')
    context={

    }
    html  = template.render(context,request)
    return HttpResponse(html)

def home(request):
  template = loader.get_template('home.html')  
  return HttpResponse(template.render())

def builder(request):
  cers=Certificates.objects.filter(owner_email='root').values()  
  context={
    'certificates':cers
  }
  template = loader.get_template('certificate_builder.html')  
  return HttpResponse(template.render(context,request))


def verifier(request):
  context={
  }
  template = loader.get_template('certificate-verifier.html')  
  return HttpResponse(template.render(context,request))

def sign_in(request):
  context={
  }
  template = loader.get_template('sign-in.html')  
  return HttpResponse(template.render(context,request))

def sign_up(request):
  context={
  }
  template = loader.get_template('sign-up.html')  
  return HttpResponse(template.render(context,request))

def add_certs(request):
  context={
  }
  template = loader.get_template('add-certificates.html')  
  return HttpResponse(template.render(context,request))

def signup_saver(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    Certificate_Owners(email=email,password=password).save()
    token_data={
      'from':email,
      'permissions':'all'
    }
    token=create_token(token_data)
    return HttpResponse(token)
  return HttpResponse('false')

def login_checker(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = Certificate_Owners.objects.filter(email=email).values() 
    if len(user)==0:
      return HttpResponse('false')
    if user[0]['password']==password:
      token_data={
        'from':email,
        'permissions':'all'
      }
      token=create_token(token_data)
      return HttpResponse(token)
    return HttpResponse('false')
      
def pdf_maker(request):
  if request.method == 'POST':
    style = request.POST.get('certificate')
    text = request.POST.get('text')
    date = request.POST.get('date')
    holder = request.POST.get('holder')
    dob = request.POST.get('dob')
    form_token = request.POST.get('token')
    signature = request.POST.get('signature')
    lines = request.POST.get('lines')
    cert_style = Certificates.objects.filter(id=style).values()[0]
    if lines=='':
      text_len=len(text) 
      text_cont_width=1056-int(cert_style['text_padding'])-int(cert_style['text_pos_right'])
      text_in_one_line=text_cont_width / int(cert_style['text_font_size']) 
      text_in_one_line=text_in_one_line + text_in_one_line/3 
      text_cont_height=math.ceil(text_len/text_in_one_line)*2*int(cert_style['text_font_size'])
    else:
      text_cont_height=int(lines)*2*int(cert_style['text_font_size'])
    if form_token !='':
      data=decode_token(form_token)
      token_data={
        'from':data['from'], 
        'to':{
          'name':holder, 
          'dob': dob 
        },
        'permissions':'none'
      }
      token=create_token(token_data)
      op=generate_checksum(token)
      Certificate_Tokens(checksum=op,real_token=token).save()
    else:
      op=''
    content={
    "text":text,
    "date":date,
    "signature":signature,
    "token":op
    }
    context={ 
        'cert_style': cert_style,
        'content':content,
        'text_height':str(text_cont_height),       
        'date_height': int(cert_style['date_font_size'])*2,
        'signature_height': int(cert_style['signature_font_size'])*2,
      }
    if style=='1':
     template = loader.get_template('rough-pdf.html')
    else:
      template = loader.get_template('certificate-pdf.html')
    html  = template.render(context)
    # return HttpResponse(html)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    return HttpResponse(result.getvalue() , content_type='application/pdf') 

def previewpdf(request):
  return pdf_maker(request)

def savepdf(request):
    response= pdf_maker(request)
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    return response


def create_token(data: dict):
  # expire = datetime.utcnow() + timedelta(minutes=15)
  # to_encode.update({"exp": expire})
  to_encode = data.copy()
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def decode_token(token: str):
  try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      return payload
  except JWTError:
      return 'false'

import hashlib
def generate_checksum(data):
    data_bytes = data.encode('utf-8')
    sha256_hash = hashlib.sha256(data_bytes)
    checksum = sha256_hash.hexdigest()
    return checksum[:8]

import json
def verify_token(request):
  if request.method == 'POST':
    token=request.POST.get('token')
    token = Certificate_Tokens.objects.filter(checksum=token).values() 
    if len(token)==0:
        return HttpResponse('false')
    return HttpResponse(json.dumps(decode_token(token[0]['real_token'])))
  else:
    return HttpResponse('false')

def style_storer(request):
  if request.method == 'POST':
    text_width = request.POST.get('text_width')  
    tfs=request.POST.get('text_font_size')
    dfs=request.POST.get('date_font_size')
    sfs=request.POST.get('signature_font_size')
    if tfs=='':
      tfs='35'
    if dfs=='':
      dfs='35'
    if sfs=='':
        sfs='35' 
    text_font_size = tfs
    date_font_size = dfs
    signature_font_size = sfs
    text_pos_top = error_eqn_res(request,'text_pos_top',tfs)
    date_pos_top = error_eqn_res(request,'date_pos_top',dfs)
    date_pos_left = error_eqn_res(request,'date_pos_left',dfs)
    signature_pos_top = error_eqn_res(request,'signature_pos_top',sfs)
    signature_pos_left = error_eqn_res(request,'signature_pos_left',sfs)    
    text_color = request.POST.get('text_color')
    date_color = request.POST.get('date_color')
    signature_color = request.POST.get('signature_color')
    text_padding=math.ceil((1092-2*int(text_width))/2)
    # signature = request.POST.get('signature') user email
    # signature = request.POST.get('signature')
    owner=Certificate_Owners.objects.filter(email='root')[0]
    Certificates(owner_email=owner, text_pos_top=text_pos_top, text_padding=text_padding, date_pos_top=date_pos_top, date_pos_left=date_pos_left, signature_pos_top=signature_pos_top, signature_pos_left=signature_pos_left,date_font_size=date_font_size, text_font_size=text_font_size, signature_font_size= signature_font_size, text_color=text_color, date_color=date_color, signature_color=signature_color, image_url="pngwing.com (1).png").save()
    return HttpResponse('saved')
    


def style_previewer(request):
    if request.method == 'POST':
      text_width = request.POST.get('text_width')
      tfs=request.POST.get('text_font_size')
      dfs=request.POST.get('date_font_size')
      sfs=request.POST.get('signature_font_size')
      if tfs=='':
        tfs='35'
      if dfs=='':
        dfs='35'
      if sfs=='':
        sfs='35'
      cert_style={
        'text_pos_top' : error_eqn_res(request,'text_pos_top',tfs),
        'date_pos_top' :  error_eqn_res(request,'date_pos_top',dfs),
        'date_pos_left' :  error_eqn_res(request,'date_pos_left',dfs),
        'signature_pos_top' :  error_eqn_res(request,'signature_pos_top',sfs),
        'signature_pos_left' :  error_eqn_res(request,'signature_pos_left',sfs),   
        'text_font_size' : tfs,
        'date_font_size' : dfs,
        'signature_font_size' : sfs,
        'text_color' : request.POST.get('text_color'),
        'date_color' : request.POST.get('date_color'),
        'signature_color' : request.POST.get('signature_color'),
        'text_padding':math.ceil((1092-2*int(text_width))/2),
        'text_pos_right':'0',
        'image_url':'pngwing.com (1).png'
        }

      content={
      "text":'I want to certify preet is good',
      "date":"2 july 2003",
      "signature":"Navpreet",
      "token":''
      }
      text_len=len(content['text']) 
      text_cont_width=1056-int(cert_style['text_padding'])-int(cert_style['text_pos_right'])
      text_in_one_line=text_cont_width / int(cert_style['text_font_size']) 
      text_in_one_line=text_in_one_line + text_in_one_line/3 
      text_cont_height=math.ceil(text_len/text_in_one_line)*2*int(cert_style['text_font_size'])
      context={ 
          'cert_style': cert_style,
          'content':content,
          'text_height':str(text_cont_height),       
          'date_height': int(cert_style['date_font_size'])*2,
          'signature_height': int(cert_style['signature_font_size'])*2,
        }
      template = loader.get_template('certificate-pdf.html')
      html  = template.render(context)
      result = BytesIO()
      pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
      return HttpResponse(result.getvalue() , content_type='application/pdf') 

def error_eqn_res(request,key,fs):  
  error=request.POST.get(key+'_error_value')
  if error=='':
    error='0'
  if(request.POST.get(key+'_error_op')=='0'):
    return 2*int(request.POST.get(key))+ float(error)*int(fs)
  else:
    return 2*int(request.POST.get(key))- float(error)*int(fs)

      

