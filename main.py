import sys
sys.path.append('./resources')
sys.path.append('./app')
sys.path.append('./utils')
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from app.app_init import app, db
from models import HotPost, hot_post_schema
from funcs import *
import json


@app.route('/hot_posts', methods=['POST', 'PUT'])
def add_hot_post():

    try:
        data = request.form

        title = str(data['title'])
        author = str(data['author'])
        num_ups = int(data['num_ups'])
        num_comments = int(data['num_comments'])

        ts_creation = data['ts_creation']

        valid_dt = date_to_python(ts_creation)

        new_post = HotPost(
            title=title, 
            author=author, 
            ts_creation=valid_dt, 
            num_ups=num_ups, 
            num_comments=num_comments
            )

        db.session.add(new_post)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify(str(e)), 500

    return hot_post_schema.jsonify(new_post)

@app.route('/hot_posts/<path:args>', methods=['GET'])
def get_per_date_range(args):

    args = args.split('/')

    if len(args) <= 1:
        abort(405, message="Missing argument: final_date, or unable to parse.")

    if len(args) >= 2: 
        dt_ini = args[0]   
        dt_fin = args[1]
    
    if len(args) >= 3:
        sort_by = args[2]
    else:
        sort_by = 'ups'

    dt_ini = parse_path_to_date_str(dt_ini.replace("Z", ""))
    dt_fin = parse_path_to_date_str(dt_fin.replace("Z", ""))

    if not dt_ini or not dt_fin:
        abort(405, message="Unable to parse for dates on: /hot_posts/<dt_ini>/<dt_fin>")
    
    abort_if_date_is_invalid(dt_ini, dt_fin)
    abort_if_sorting_is_invalid(sort_by)

    try:
        if 'up' in sort_by:
            res = HotPost.query.filter(
                    HotPost.ts_creation >= date_to_python(dt_ini)
                ).filter(
                    HotPost.ts_creation <= date_to_python(dt_fin) 
                ).order_by(desc(HotPost.num_ups)).limit(100).all()

        elif 'comment' in sort_by:
            res = HotPost.query.filter(
                    HotPost.ts_creation >= date_to_python(dt_ini)
                ).filter(
                    HotPost.ts_creation <= date_to_python(dt_fin) 
                ).order_by(desc(HotPost.num_comments)).limit(100).all()

    except Exception as e:
        return jsonify(str(e)), 500

    result = [{
        'id': i.id,
        'title': i.title,
        'author': i.author,
        'ts_creation': i.ts_creation,
        'num_ups': i.num_ups,
        'num_comments': i.num_comments
        } for i in res]

    return jsonify(result), 201

@app.route('/hot_posts/<string:sort_by>', methods=['GET'])
def get_users_per_sorting(sort_by):
    
    abort_if_sorting_is_invalid(sort_by)

    try:
        if 'up' in sort_by:
            res = HotPost.query.with_entities(
                    HotPost.author, HotPost.num_ups
                ).order_by(desc(HotPost.num_ups)).limit(100).all()

            result = [{
                'author': i.author,
                'num_ups': i.num_ups
                } for i in res]

        elif 'comment' in sort_by:
            res = HotPost.query.with_entities(
                    HotPost.author, HotPost.num_comments
                ).order_by(desc(HotPost.num_comments)).limit(100).all()
            result = [{
                'author': i.author,
                'num_comments': i.num_comments
                } for i in res]
                
    except Exception as e:
        return jsonify(str(e)), 500

    
    return jsonify(result), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)