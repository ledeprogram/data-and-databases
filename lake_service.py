from flask import Flask, request, jsonify
import pg8000

app = Flask(__name__)
conn = pg8000.connect(database='mondial')

def none_or_int(v):
    if v is not None:
        return int(v)
    else:
        return v

@app.route("/lakes")
def get_lakes():
    query = "SELECT lake.name, lake.area, lake.elevation, lake.type FROM lake"
    cursor = conn.cursor()
    query_args = []
    where_conds = []
    type_ = request.args.get('type', None)
    if type_:
        where_conds.append("lake.type = %s")
        query_args.append(type_)
    if len(where_conds) > 0:
        query += ' WHERE ' + ' AND '.join(where_conds)
    order_by = request.args.get('sort', 'name')
    if order_by not in ('area', 'name', 'elevation'):
        order_by = 'name'
    query += " ORDER BY lake." + order_by
    if order_by in ('area', 'elevation'):
        query += " DESC"
    cursor.execute(query, query_args)
    output = []
    for rec in cursor.fetchall():
        if rec[1]:
            area = int(rec[1])
        else:
            area = None
        output.append({'name': rec[0],
            'area': none_or_int(rec[1]),
            'elevation': none_or_int(rec[2]),
            'type': rec[3]
            })
    return jsonify(output)

app.run()
