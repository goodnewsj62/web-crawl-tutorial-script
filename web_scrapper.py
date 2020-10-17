import requests
from bs4 import BeautifulSoup
import re
import os

url = 'https://www.facebook.com/login'

def email_validation(email):

    if not isinstance(email,str) and len(str(email)) < 8:
        raise TypeError('must be a string  and must be greater than eight character')
    elif not '@' in email:
        raise ValueError('must have "@" symbol')
    elif not email.endswith('.com'):
        raise ValueError('must end with a .com')

    return email

def login(url,email,password):
    data = {}
    response = None
    feedback = None

    try:
        with requests.Session() as session:
            # get login page with form in it
            response = session.get(url)

            # code to scrape and find csrf_token in hidden field
            sp = BeautifulSoup(response.text,'html.parser')
            sp = sp.find_all('input')
            for each in sp:


                if 'value' in str(each):
                    token = re.findall('^<.+value="(.+")', str(each))
                    name = re.findall('^<.+name="(.+\s)', str(each))

                    if name[0].startswith('email') or name[0].startswith('pass') or len(token) == 0:
                        continue
                    name = name[0]
                    name = name.replace("\"","").split()
                    token = token[0][ :-1]

                    data[name[0]] = token


            if '@' in email:
                # knows if you enter email or not
                data['email'] = email_validation(email)

            data['email'] = email
            data['pass'] = password


            # sign in with data
            response = session.post(url,data)

            # get everything on login page
            feedback = session.get('https://www.facebook.com').text
    except ConnectionError:
        print('An error occurred while connecting to url')
    except ConnectionAbortedError:
        print('Connection Aborted!')
    except ConnectionRefusedError:
        print('Connection refused!')
    except:
        print('Error')

    if response:
        print('Login successful',response.status_code)
    else:
        print('login failed')
    return feedback

a = login(url,'foo@foo.com','foo')
soup = BeautifulSoup(a,'html.parser')
# tags = soup()
#
# for tag in tags:
#     print(tag)
print(soup.prettify())