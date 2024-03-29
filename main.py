import streamlit as st
st.set_page_config(page_title="My performance", layout="wide", initial_sidebar_state="auto")
import streamlit_authenticator as stauth
from components.firebase import get_credentials, register_user, create_user
from components.adminPage import show_admin_page

import firebase_admin
from firebase_admin import credentials

config = get_credentials()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login(location='main',
                                                            fields={'Form name': 'Войти в аккаунт',
                                                                    'Username': 'Имя пользователя',
                                                                    'Password': 'Пароль',
                                                                    'Login': 'Войти'})

if authentication_status == False:
    st.error('Имя пользователя и/или пароль введены неверно')
elif authentication_status is None:
    st.warning('Введите имя пользователя и пароль')

if authentication_status is not True:
   with st.expander(label="Зарегистрироваться"):
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                        location="main",
                        preauthorization=False)
            if email_of_registered_user:
                if register_user(config=config):
                    if create_user(email=email_of_registered_user, user=username_of_registered_user, name = name_of_registered_user):
                        st.success("User registered successfully")
                    else:
                        st.error("Could not register user")
                else:
                    st.error("Could not register user")
        except Exception as e:
            st.error(e)

if authentication_status is True:
    if username=='admin':
        with st.sidebar:
            st.write(f'Welcome *{name}*')
        show_admin_page()
    else:
        with st.sidebar:
            st.write(f'Welcome *{name}*')
    authenticator.logout(button_name='Выйти',
                         location='sidebar')



class User:
    def __init__(self, name: str, email: str, position: str, role: str, free_bonuses: int = 0, reserved_bonuses: int = 0):
        self.name = name
        self.email = email
        self.position = position
        self.free_bonuses = free_bonuses
        self.reserved_bonuses = reserved_bonuses
        self.role = role
    def __str__(self):
        return str({
            "user_name": self.name,
            "user_email": self.email,
            "user_position": self.position,
            "user_free_bonuses": self.free_bonuses,
            "user_reserved_bonuses": self.reserved_bonuses,
            "user_role": self.role
        })

    @staticmethod
    def from_dict(source):
        pass

    def to_dict(self):
        return {
            "user_name": self.name,
            "user_email": self.email,
            "user_position": self.position,
            "user_free_bonuses": self.free_bonuses,
            "user_reserved_bonuses": self.reserved_bonuses,
            "user_role": self.role
        }
tmp = User("Федоров Федор","fedorovfedor@8agency.com", "project manager", "user", 450, 0)




