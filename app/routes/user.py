from flask import Blueprint, request, url_for, render_template_string, jsonify
from flask_jwt_extended import create_access_token
from app.utils.database import db
from app.utils import responses as resp
from app.utils.responses import response_with
from app.models.user import User, UserSchema
from app.utils.mail import send_email
from app.utils.token import confirm_verification_token, generate_verification_token

user_routes = Blueprint("user_routes", __name__)


@user_routes.route('', methods=['POST'])
def create_user():
   try:
      data = request.get_json()
      if User.find_by_username(data['username']) is not None:
         return response_with(
            resp.INVALID_INPUT_422,
            value={"detail": "Username " + data['username'] + " is already taken"}
         )
      elif User.find_by_email(data['email']) is not None:
         return response_with(
            resp.INVALID_INPUT_422,
            value={"detail": "Email " + data['email'] + " is already taken"}
         )
      else:
         data['password'] = User.generate_hash(data['password'])
         schema = UserSchema()
         user = schema.load(data)

         # mail
         token = generate_verification_token(data['email'])
         verification_email = url_for('user_routes.verify_email', token=token, _external=True)
         html = render_template_string(
            "<p>Welcome! Thanks for signing up. "
            "Please follow this link to activate your account:</p> "
            "<p><a href='{{ verification_email }}'>{{ verification_email }}</a></p> <br> "
            "<p>Thanks!</p>",
            verification_email=verification_email)
         subject = "Please Verify your email"
         send_email(user.email, subject, html)
         # execute schema
         schema.dump(user.create())
         return response_with(resp.SUCCESS_201)
   except ValueError as e:
      return response_with(resp.INVALID_INPUT_422)


@user_routes.route('/confirm/<token>', methods=['GET'])
def verify_email(token):
   try:
      email = confirm_verification_token(token)
   except Exception as e:
      print(e)
      return response_with(resp.SERVER_ERROR_404)
   user = User.query.filter_by(email=email).first_or_404()
   if user.verified:
      return response_with(resp.INVALID_INPUT_422)
   else:
      user.verified = True
      db.session.add(user)
      db.session.commit()
      return response_with(
         resp.SUCCESS_200,
         value={'message': 'E-mail verified, you can proceed to login now.'}
      )


@user_routes.route('/login', methods=['POST'])
def authenticate_user():
   try:
      data = request.get_json()
      if data.get('email'):
         current_user = User.find_by_email(data['email'])
      elif data.get('username'):
         current_user = User.find_by_username(data['username'])

      if not current_user:
         return response_with(resp.SERVER_ERROR_404)
      if current_user and not current_user.verified:
         return response_with(resp.BAD_REQUEST_400)

      if User.verify_hash(data['password'], current_user.password):
         access_token = create_access_token(identity=data['username'])
         return response_with(
            resp.SUCCESS_201,
            value={'message': 'Logged in as {}'.format(current_user.username), 'access_token': access_token}
         )
      else:
         return response_with(resp.UNAUTHORIZED_401)
   except Exception as e:
      print(e)
      return response_with(resp.UNAUTHORIZED_401)
