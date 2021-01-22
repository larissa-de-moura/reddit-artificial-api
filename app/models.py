# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
import sys
import os
from datetime import datetime
from sqlalchemy import desc
sys.path.append('./app')
from app_init import app, db, ma


class HotPost(db.Model):


    __tablename__ = 'tb_subreddit_artificial'
    def __init___(self, title=None, author=None, ts_creation=None, num_ups=None, num_comments=None):
        self.title = title
        self.author = author
        self.ts_creation = ts_creation
        self.num_ups = num_ups
        self.num_comments = num_comments

        
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(600), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    ts_creation = db.Column(db.DateTime, nullable=False)
    num_ups = db.Column(db.Integer, nullable=False)
    num_comments = db.Column(db.Integer, nullable=False)


class HotPostSchema(ma.Schema):
    class Meta:
        fields = ('title', 'author', 'ts_creation', 'num_ups', 'num_comments')

hot_post_schema = HotPostSchema()
hot_posts_schema = HotPostSchema(many=True)