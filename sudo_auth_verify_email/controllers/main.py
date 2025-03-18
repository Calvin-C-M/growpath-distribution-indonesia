import logging
import werkzeug
import random
import re
from werkzeug.urls import url_encode
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome, SIGN_UP_REQUEST_PARAMS
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_users import SignupError
from markupsafe import Markup

_logger = logging.getLogger(__name__)

def default_password():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(20))

SIGN_UP_REQUEST_PARAMS.add('phone')


class AuthSignupHome(AuthSignupHome):

    def get_auth_signup_config(self):
        auth_config = super(AuthSignupHome, self).get_auth_signup_config()
        auth_config['signup_enabled'] = request.env['res.users']._get_signup_invitation_scope() in ['b2c', 'b2c_verify']
        auth_config['signup_scope'] = request.env['res.users']._get_signup_invitation_scope()
        return auth_config

    def _prepare_signup_values(self, qcontext):
        values = super(AuthSignupHome, self)._prepare_signup_values(qcontext)
        values['phone'] = qcontext.get('phone')
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)[A-Za-z\d\W]{8,}$"

        # Check password verification
        if values.get('password'):
            if not re.match(password_regex, values.get('password')):
                raise SignupError(
                    _('Invalid password') +
                    Markup('<br/>') +
                    _("Password must contain:") +
                    Markup('<br/>') +
                    _("* Uppercase and lowercase letters") +
                    Markup('<br/>') +
                    _("* Special characters") +
                    Markup('<br/>') +
                    _("* More than 8 characters")
                )

        if qcontext.get('signup_scope') == 'b2c_verify' and not qcontext.get('verify_email'):
            values['password'] = default_password()
        return values

    def do_verified_signup(self, qcontext):
        values = self._prepare_signup_values(qcontext)
        request.env['res.users'].sudo().signup(values, qcontext.get('token'))
        request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                User = request.env['res.users']
                if qcontext['signup_scope'] == 'b2c_verify':
                    self.do_verified_signup(qcontext)

                    qcontext['info'] = 'Account created. Please check your email for the verification link.'

                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )

                    template = request.env.ref('sudo_auth_verify_email.verify_email_template', raise_if_not_found=False)

                    if user_sudo and template:
                        signup_token = user_sudo.partner_id.sudo()._generate_signup_token()
                        template.with_context(signup_token=signup_token).sudo().send_mail(
                            user_sudo.id,
                            force_send=True,
                        )
                else:
                    self.do_signup(qcontext)

                    # Set user to public if they were not signed in by do_signup
                    # (mfa enabled)
                    if request.session.uid is None:
                        public_user = request.env.ref('base.public_user')
                        request.update_env(user=public_user)

                    # Send an account creation confirmation email
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )

                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().send_mail(user_sudo.id, force_send=True)

                    return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search_count([("login", "=", qcontext.get("login"))], limit=1):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.warning("%s", e)
                    qcontext['error'] = _("Could not create a new account.") + Markup('<br/>') + str(e)

        elif 'signup_email' in qcontext:
            user = request.env['res.users'].sudo().search(
                [('email', '=', qcontext.get('signup_email')), ('state', '!=', 'new')], limit=1)
            if user:
                return request.redirect('/web/login?%s' % url_encode({'login': user.login, 'redirect': '/web'}))

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response

    @http.route('/web/verify', type='http', auth='public', website=True, sitemap=False)
    def verify_email(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if 'invalid_token' in qcontext and qcontext['invalid_token']:
            return werkzeug.exceptions.Forbidden()

        qcontext['verify_email'] = True

        User = request.env['res.users']
        user_rec = User.sudo().search(
            User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
        )
        if not user_rec:
            return werkzeug.exceptions.NotFound()

        qcontext['token'] = user_rec.partner_id.sudo()._generate_signup_token()
        qcontext['phone'] = user_rec.phone

        if request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)

                # Set user to public if they were not signed in by do_signup
                # (mfa enabled)
                if request.session.uid is None:
                    public_user = request.env.ref('base.public_user')
                    request.update_env(user=public_user)

                return self.web_login(*args, **kw)
            except Exception as e:
                qcontext['error'] = _(str(e))

        response = request.render('sudo_auth_verify_email.create_new_password', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response
