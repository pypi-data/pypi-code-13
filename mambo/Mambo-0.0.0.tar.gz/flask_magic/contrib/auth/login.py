
import datetime
from flask_magic import (Magic, models, set_nav, page_meta, mail, init_app,
                         route, get_config, session, request, redirect,
                         url_for, get, post, flash_success, flash_error, abort, recaptcha)
from flask_login import (LoginManager, login_user, current_user, fresh_login_required)
from . import (logout_user, is_authenticated, not_authenticated,
               require_login_allowed, require_signup_allowed, require_social_login_allowed,
               email_reset_password, email_verification_email, email_signup_welcome)
from flask_magic.exceptions import ViewError, AppError
from flask_magic import utils



def setup(**kwargs):
    """
    This plugin allow user to login to application

        - options:
            - login_view
            - logout_view
            - verify_email

    """

    options = kwargs.get("options", {})

    User = models.AuthUser
    UserLogin = models.AuthUserLogin

    login_view = options.get("login_view") or "AuthLogin:login"
    logout_view = options.get("logout_view") or "AuthLogin:login"
    verify_email = options.get("verify_email") or False

    login_manager = LoginManager()
    login_manager.login_view = login_view
    login_manager.login_message_category = "error"
    init_app(login_manager.init_app)

    @login_manager.user_loader
    def load_user(userid):
        return User.get(userid)

    class AuthLogin(Magic):
        base_route = kwargs.get("route") or "/"

        def _auth_user(self, user_login):
            """
            Auth the user
            :param user_login: UserLogin object
            :return:
            """
            user_login.user.update(last_login=datetime.datetime.now())
            login_user(user_login.user)

        @set_nav("Login", visible=not_authenticated)
        @get()
        @post()
        @require_login_allowed
        @logout_user
        def login(self):
            page_meta(title="Login")

            if request.method == "POST":
                if request.form.get("method") == "email":
                    self._post_login_email()
                elif request.form.get("method") == "social":
                    self._post_login_social()
                else:
                    abort("Invalid login method")

            return {
                "email": request.args.get("email"),
                "login_url_next": request.args.get("next", ""),
                "allow_signup": options.get("allow_signup"),
                "show_verification_message": True if request.args.get("v") == "1" else False
            }

        def _post_login_email(self):
            email = request.form.get("email").strip()
            password = request.form.get("password").strip()

            if not email or not password:
                flash_error("Email or Password is empty")
                return redirect(self.login, next=request.form.get("next"))

            userl = UserLogin.get_by_email(email)
            if userl and userl.password_hash and userl.password_matched(password):
                if verify_email and not userl.email_verified:
                    return redirect(self.login, email=email, v="1")
                else:
                    self._auth_user(userl)
                    return redirect(request.form.get("next") or login_view)
            else:
                flash_error("Email or Password is invalid")
                return redirect(self.login, next=request.form.get("next"))

        def _post_login_social(self):
            return redirect(self.login)

        @set_nav("Logout", visible=False)
        @get()
        @logout_user
        def logout(self):
            return redirect(logout_view or login_view or self.login)

        @set_nav("Lost Password", visible=False)
        @get()
        @post()
        @require_login_allowed
        @logout_user
        def lost_password(self):
            page_meta(title="Lost Password")

            if request.method == "POST":
                email = request.form.get("email")
                user_l = UserLogin.get_by_email(email)
                if user_l:
                    email_reset_password(user_l)
                    flash_success("A new password has been sent to '%s'" % email)
                    return redirect(self.login)
                else:
                    flash_error("Invalid email address")
                    return redirect(self.lost_password)

        @set_nav("Signup", visible=not_authenticated)
        @get()
        @post()
        @require_login_allowed
        @require_signup_allowed
        @logout_user
        def signup(self):
            """
            For Email Signup
            :return:
            """
            page_meta(title="Signup")
            if request.method == "POST":
                if request.form.get("method") == "email":
                    self._post_signup_email()
                elif request.form.get("method") == "social":
                    self._post_signup_social()
                else:
                    abort("Invalid signup method")

            return dict(login_url_next=request.args.get("next", ""),)

        def _post_signup_email(self):
            if not recaptcha.verify():
                flash_error("Invalid Security code")
                return redirect(self.signup, next=request.form.get("next"))
            try:
                name = request.form.get("name")
                email = request.form.get("email")
                password = request.form.get("password")
                password2 = request.form.get("password2")

                if not name:
                    raise ViewError("Name is required")
                elif not password.strip() or password.strip() != password2.strip():
                    raise ViewError("Passwords don't match")
                else:
                    new_login = UserLogin.new(login_type="email",
                                              email=email,
                                              password=password.strip(),
                                              user_info={
                                                  "name": name,
                                                  "contact_email": email
                                              })
                    if verify_email:
                        email_signup_welcome(new_login)
                        flash_success("A welcome email containing a confirmation link has been sent to %s" % email)
                    else:
                        self._auth_user(new_login)
                    return redirect(request.form.get("next") or login_view)
            except AppError as ex:
                flash_error(ex.message)
            return redirect(self.signup, next=request.form.get("next"))

        @set_nav("Reset Password", visible=False)
        @get("/reset-password/<token>/")
        @post("/reset-password/<token>/")
        @require_login_allowed
        @logout_user
        def reset_password(self, token):
            page_meta(title="Reset Password")
            user_login = UserLogin.get_by_temp_login(token)
            if user_login:
                if request.method == "POST":
                    try:
                        password = request.form.get("password", "").strip()
                        password2 = request.form.get("password2", "").strip()
                        if not password:
                            raise ViewError("Password is missing")
                        elif password != password2:
                            raise ViewError("Password don't match")

                        user_login.change_password(password)
                        user_login.clear_temp_login()
                        user_login.clear_email_verified_token()
                        
                        flash_success("Password updated successfully!")
                        return redirect(login_view)
                    except AppError as ex:
                        flash_error("Error: %s" % ex.message)
                        return redirect(self.reset_password, token=token)
                return {"token": token}
            return redirect(self.login)

        @set_nav("Confirm Email", visible=False)
        @get()
        @post()
        @require_login_allowed
        @logout_user
        def confirm_email(self):
            if not verify_email:
                return redirect(self.login)

            if request.method == "POST":
                email = request.form.get("email")
                if email and utils.is_email_valid(email):
                    userl = UserLogin.get_by_email(email)
                    if userl:
                        if not userl.email_verified:
                            email_verification_email(userl)
                            flash_success("A verification email has been sent to %s" % email)
                        return redirect(self.login, email=email)
                flash_error("Invalid account")
                return redirect(self.confirm_email, email=email)

            page_meta(title="Confirm Email")
            return {
                "email": request.args.get("email"),
            }

        @require_login_allowed
        @logout_user
        def verify_email(self, token):
            user_login = UserLogin.get_by_email_verified_token(token)
            if user_login:
                user_login.clear_email_verified_token()
                flash_success("Account verified. You can now login")
                return redirect(self.login, email=user_login.email)
            return redirect(self.login)
            
    return AuthLogin
