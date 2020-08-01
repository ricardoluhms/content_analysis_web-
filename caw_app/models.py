from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from caw_app.exceptions import ValidationError
from . import db, login_manager ### Check db creation, startup and update

association_table = db.Table('user_projects', db.Model.metadata,
                                db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                                db.Column('project_id', db.Integer, db.ForeignKey('projects.id'))
                            )

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    ### Table Name ###
    __tablename__ = 'users'
    ### Primary Key ###
    id = db.Column(db.Integer, primary_key=True)
    ### Data Columns ###
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    avatar_hash = db.Column(db.String(32))
    ### Foreign Keys ###
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    ### Relationship Keys - Has Children (OLD)? - YES - Post, Comments
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    ### Relationship Keys - Has Children (NEW)? - YES - Projects
    projects_PC=db.relationship('Projects', secondary=association_table, back_populates='users_CP')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()
        #self.follow(self)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api.get_user_posts', id=self.id),
            'followed_posts_url': url_for('api.get_user_followed_posts',
                                          id=self.id),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
            'comments_url': url_for('api.get_post_comments', id=self.id),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)

db.event.listen(Post.body, 'set', Post.on_changed_body)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id),
            'post_url': url_for('api.get_post', id=self.post_id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)

db.event.listen(Comment.body, 'set', Comment.on_changed_body)

class Projects(db.Model):
    ### Table Name ###
    __tablename__='projects'
    ### Primary Key ###
    id = db.Column(db.Integer, primary_key=True)
    ### Data Columns ###
    project_name=db.Column(db.String(64), index=True)
    ### Foreign Keys - Parent only ###
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ## Relationship Keys - Has Parent? - YES - Users
    users_CP=db.relationship('User', secondary=association_table, back_populates="projects_PC")
    ### Relationship Keys - Has Children? - YES - New_Group
    reviews_PC=db.relationship('Reviews', back_populates="projects_CP")

class Reviews(db.Model):
    ### Table Name ###
    __tablename__='reviews'
    ### Primary Key ###
    id = db.Column(db.Integer, primary_key=True) ### review id
    review_name=db.Column(db.String(64), index=True)
    ### Foreign Keys - Parent only ###
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))### ok - project=parent - review=children
    ### Relationship Keys - Has Parent? - YES - Projects
    projects_CP=db.relationship('Projects', back_populates="reviews_PC")
    ### Relationship Keys - Has Children? - YES - Problem_Space, Solution_Space, Manage_Groups
    problem_space_PC=db.relationship('Problem_Space', back_populates="prob_review_CP")
    solution_space_PC=db.relationship('Solution_Space', back_populates="solut_review_CP")
    manage_group_PC=db.relationship('Manage_Groups', back_populates="review_CP")

class Problem_Space(db.Model):
    ### Table Name ###
    __tablename__='problem_space'
    ### Primary Key ###
    id = db.Column(db.Integer, primary_key=True) 
    ### Data Columns ###
    problem_space_text = db.Column(db.Text)
    ### Foreign Keys - Parent only ###
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'))
    ## Relationship Keys - Has Parent? - YES - Reviews
    prob_review_CP=db.relationship('Reviews', back_populates="problem_space_PC")
    ### Relationship Keys - Has Children? - NO

class Solution_Space(db.Model):
    ### Table Name ###
    __tablename__='solution_space'
    ### Primary Key ###
    id = db.Column(db.Integer, primary_key=True) 
    ### Data Columns ###
    solution_space_text = db.Column(db.Text)
    ### Foreign Keys - Parent only ###
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'))
    ## Relationship Keys - Has Parent? - YES - Reviews
    solut_review_CP=db.relationship('Reviews', back_populates="solution_space_PC")
    ### Relationship Keys - Has Children? - NO

class Manage_Groups(db.Model):
    ### Table Name ###
    __tablename__='manage_group'
    ### Primary Key ###
    id = db.Column(db.Integer, primary_key=True)
    ### Data Columns ###
    tt_groups=db.Column(db.Integer)
    ### Foreign Keys - Parent only ###
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'))
    ### Relationship Keys - Has Parent? - YES - Reviews
    review_CP=db.relationship('Reviews', back_populates="manage_group_PC")
    ### Relationship Keys - Has Children? - YES - New_Group
    all_groups_PC=db.relationship('New_Group', back_populates="manage_group_CP")

class New_Group(db.Model):
    ### Table Name ###
    __tablename__='all_groups'
    ### Primary Key ###
    id = db.Column(db.Integer, primary_key=True)
    ### Data Columns ###
    group_name=db.Column(db.String(64), index=True)
    group_type=db.Column(db.String(16), index=True)
    ### Foreign Keys - Parent only ###
    manage_group_id = db.Column(db.Integer, db.ForeignKey('manage_group.id'))
    ### Relationship Keys - Has Parent? - YES - Manage_Groups
    manage_group_CP=db.relationship('Manage_Groups', back_populates="all_groups_PC")
    ### Relationship Keys - Has Children? - YES - Keywords
    keywords_PC=db.relationship('Keywords', back_populates="key2group_CP")
    
class Keywords(db.Model):
    ### Table Name ###
    __tablename__='keywords'
    ### Primary Key ###
    id = db.Column(db.Integer, primary_key=True)
    ### Data Columns ###
    keyword_list = db.Column(db.Text)
    ### Foreign Keys - Parent only ###
    group_id = db.Column(db.Integer, db.ForeignKey('all_groups.id'))
    ### Relationship Keys - Has Parent? - YES - New_Group
    key2group_CP = db.relationship('New_Group', back_populates="keywords_PC")
    ### Relationship Keys - Has Children? - NO