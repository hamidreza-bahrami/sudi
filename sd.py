import streamlit as st
import pickle
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
port_stem = PorterStemmer()
import time
from pygoogletranslation import Translator
import smtplib
from email.message import EmailMessage
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('stopwords')

from_email = "hamidrezabahrami455@gmail.com"
to_email = "hamidr.bahraami@gmail.com"
email_password = "htth eind kniy bgst"
# #subject = "شناسایی کابر متمایل به خودکشی"
# #body = (f"کاربر در حال خودکشی شناسایی شد", number)
# #em = EmailMessage()
# #em['From'] = from_email
# #em['To'] = to_email
# #em['subject'] = subject
# #em.set_content(body)

context = ssl.create_default_context()

vector = pickle.load(open('vector.pkl', 'rb'))
load_model = pickle.load(open('model.pkl', 'rb'))
translator = Translator()


def stemming(content):
  con = re.sub('[^a-zA-Z]', ' ', content)
  con = con.lower()
  con = con.split()
  con = [port_stem.stem(word) for word in con if not word in stopwords.words('english')]
  con = ' '.join(con)
  return con

def thought(text):
  text = stemming(text)
  input_text = [text]
  vector1 = vector.transform(input_text)
  prediction = load_model.predict(vector1)
  return prediction

def show_page():
    st.write("<h1 style='text-align: center; color: blue;'>مدل تشخیص تمایل به خودکشی</h1>", unsafe_allow_html=True)
    st.write("<h2 style='text-align: center; color: gray;'>تشخیص بر اساس تحلیل متن کاربر</h2>", unsafe_allow_html=True)
    st.write("<h4 style='text-align: center; color: gray;'>طراح: حمیدرضا بهرامی</h4>", unsafe_allow_html=True)
    st.link_button("Robo-Ai بازگشت به", "https://robo-ai.ir")

    number = st.text_input('لطفا شماره تماس خود را وارد کنید')
    text = st.text_area('افکار خود را با من درمیان بگذارید',height=None,max_chars=None,key=None)
    
    if st.button('تحلیل افکار'):
        if text == "":
            with st.chat_message("assistant"):
                with st.spinner('''درحال بررسی لطفا صبور باشید'''):
                    time.sleep(3)
                    st.success(u'\u2713''تحلیل انجام شد')
                    st.write("<h4 style='text-align: right; color: gray;'>لطفا افکار خود را بنویسید تا بتوانم تحلیل کنم</h4>", unsafe_allow_html=True)
        
        else:
            out = translator.translate(text)
            prediction_class = thought(out.text)
            if prediction_class == [1]:
                with st.chat_message("assistant"):
                    with st.spinner('''درحال بررسی لطفا صبور باشید'''):
                        time.sleep(3)
                        st.success(u'\u2713''تحلیل انجام شد')
                        st.write("<h4 style='text-align: right; color: gray;'>.بر اساس تحلیل من، شما به خودکشی تمایل دارید</h4>", unsafe_allow_html=True)
                        st.write("<h4 style='text-align: right; color: gray;'>.برای تسکین فوری افکار خود با فردی از نزدیکان صحبت کنید</h4>", unsafe_allow_html=True)
                        st.write("<h4 style='text-align: right; color: gray;'>.و برای درمان قطعی به روانشناس مراجعه کنید</h4>", unsafe_allow_html=True)
                        subject = number
                        body = ("کاربر در حال خودکشی شناسایی شد")
                        em = EmailMessage()
                        em['From'] = from_email
                        em['To'] = to_email
                        em['subject'] = subject
                        em.set_content(body)
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as smtp:
                            smtp.login(from_email, email_password)
                            smtp.sendmail(from_email, to_email, em.as_string())
                        
            else:
                with st.chat_message("assistant"):
                    with st.spinner('''درحال بررسی لطفا صبور باشید'''):
                        time.sleep(3)
                        st.success(u'\u2713''تحلیل انجام شد')
                        st.write("<h4 style='text-align: right; color: gray;'>.بر اساس تحلیل من، بیشتر افکار شما سالم است</h4>", unsafe_allow_html=True)
                        st.write("<h4 style='text-align: right; color: gray;'>.در صورت وجود افکار متمایل به خودکشی، به روانشناس مراجعه کنید</h4>", unsafe_allow_html=True)
    else:
        pass

    if st.button("پاکسازی حافظه"):
        st.cache_data.clear()
        st.rerun()
        

show_page()


