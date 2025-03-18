# -*- coding: utf-8 -*-
{
    'name': 'Sudo Authentication Verify Email',
    'version': '18.1.0',
    'author': 'Tilabs',
    'category': 'Tools',
    'website': 'http://tilabs.id',
    'summary': 'Allow users to sign up with email verification',
    'license': 'LGPL-3',
    'description': """
        * Add new user registration type
        * Add feature to send email verification when signing up 
    """,
    'depends': [
        'base',
        'website',
        'web',
    ],
    'data': [
        'views/auth_signup_login_template.xml',
        'data/mail_template_data.xml',
    ],
    'installable': True,
    'application': False,
}