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

st.set_page_config(page_title='پیشگیری از خودکشی - RoboAi', layout='centered', page_icon='🩺')

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
    st.write("<h3 style='text-align: center; color: gold;'>سامانه تشخیص و پیشگیری از خودکشی 🩺</h3>", unsafe_allow_html=True)
    st.write("<h6 style='text-align: center; color: white;'>RoboAi طراحی شده توسط</h6>", unsafe_allow_html=True)
    st.link_button("Robo-Ai.ir بازگشت به", "https://robo-ai.ir")
    with st.sidebar:
        st.write("<h4 style='text-align: center; color: white;'>تشخیص و پیشگیری از خودکشی</h4>", unsafe_allow_html=True)
        st.write("<h4 style='text-align: center; color: white;'>با تحلیل متن کاربر</h4>", unsafe_allow_html=True)
        st.divider()
        st.write("<h6 style='text-align: center; color: white;'>طراحی و توسعه</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: center; color: white;'>حمیدرضا بهرامی</h6>", unsafe_allow_html=True)

    container = st.container(border=True)
    container.write("<h6 style='text-align: right; color: white;'>تشخیص احتمال بروز خودکشی از متن 💬</h6>", unsafe_allow_html=True)

    number = st.text_input('لطفا شماره تماس خود را وارد کنید')
    text = st.text_area('افکار خود را با من درمیان بگذارید',height=None,max_chars=None,key=None)
    
    if st.button('تحلیل افکار'):
        if text == "":
            with st.chat_message("assistant"):
                with st.spinner('''درحال تحلیل'''):
                    time.sleep(2)
                    st.success(u'\u2713''تحلیل انجام شد')
                    text1 = 'لطفا متن را وارد کنید'
                    def stream_data1():
                        for word in text1.split(" "):
                            yield word + " "
                            time.sleep(0.09)
                    st.write_stream(stream_data1)
        
        else:
            out = translator.translate(text)
            prediction_class = thought(out.text)
            if prediction_class == [1]:
                with st.chat_message("assistant"):
                    with st.spinner('''درحال تحلیل ، لطفا صبور باشید'''):
                        time.sleep(2)
                        st.success(u'\u2713''تحلیل انجام شد')
                        text1 = 'بر اساس تحلیل من ، علائمی از خطر خودکشی در متن موردنظر دیده می شود'
                        text2 = 'متن شما به همراه اطلاعات تکمیلی به سرور اصلی ارسال گردید'
                        def stream_data1():
                            for word in text1.split(" "):
                                yield word + " "
                                time.sleep(0.09)
                        st.write_stream(stream_data1)
                        def stream_data2():
                            for word in text2.split(" "):
                                yield word + " "
                                time.sleep(0.09)
                        st.write_stream(stream_data2)
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
                    with st.spinner('''درحال تحلیل ، لطفا صبور باشید'''):
                        time.sleep(2)
                        st.success(u'\u2713''تحلیل انجام شد')
                        st.success(u'\u2713''تحلیل انجام شد')
                        text3 = 'بر اساس تحلیل من ، علائمی از خطر خودکشی در متن موردنظر دیده نمی شود'
                        def stream_data3():
                            for word in text3.split(" "):
                                yield word + " "
                                time.sleep(0.09)
                        st.write_stream(stream_data3)
    else:
        pass

    if st.button("پاکسازی حافظه"):
        st.cache_data.clear()
        st.rerun()
show_page()
