from datetime import datetime
from werkzeug.routing import ValidationError
from flask_restful import abort
from flask import jsonify
import re

def date_to_python(value):
    try:
        try:
            value = int(float(value))
            return datetime.utcfromtimestamp(value)
        except:
            return datetime.fromisoformat(value)

    except ValueError:
        raise ValidationError()


def date_to_str(value):
    return value.isoformat()


def parse_path_to_date_str(path):

    re_patterns = dict(
        has_ms = r'\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d{0,6}',
        has_sec = r'\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d',
        has_hour_min = r'\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d',
        date = r'\d{4}-[01]\d-[0-3]\d'
    )
    result = {}
    for key, value in re_patterns.items():
        found = re.findall(value, path)

        if found:
            parsed = found[0]

            check_ms = parsed.split('.')
            conditions_for_ms = [
                key == 'has_ms',
                len(check_ms) == 2
                ]

            if all(conditions_for_ms) and len(check_ms[1]) not in (3, 6):
                parsed = None

            result[key] = parsed

    for key in re_patterns.keys():
        res = result.get(key)
        if res:
            return res
    return
    


def abort_if_sorting_is_invalid(sort_by):

    if sort_by.rstrip('s') not in ('up', 'comment'):
        return abort(404, 'Invalid sorting. Valid options: ["ups", "comments"]')


def abort_if_date_is_invalid(dt_ini, dt_fin):

    msg = ''
    if not dt_ini or not dt_fin:
        return abort(404, message=f'Unable to find valid dates. Dt_ini = {dt_ini}. Dt_fin = {dt_fin}')

    ini_ms = dt_ini.split('.')
    fin_ms = dt_fin.split('.')

    ini_has_ms = len(ini_ms) > 1
    fin_has_ms = len(fin_ms) > 1
    
    ## acceptable: %Y-%m-%dT%H:%M:%S or %Y-%m-%d
    if len(dt_fin) != len(dt_ini):
        return abort(404, message=f'Given dates are not standardized. Length = ini: {len(dt_ini)}, fin: {len(dt_fin)}')

    elif (ini_has_ms and not fin_has_ms) or (fin_has_ms and not ini_has_ms):
        return abort(404, message=f'Given dates are not standardized. Has miliseconds = ini: {ini_has_ms}, fin: {fin_has_ms}')
    elif dt_fin < dt_ini:
       return abort(404, message=f'Initial date {dt_fin} is less than final date {dt_fin}')
