from flask import Flask, request, jsonify, session, send_file
from pymongo import MongoClient, DESCENDING
from bson import ObjectId
import hashlib, random, string
from datetime import datetime
import os

# ── Config ───────────────────────────────────────────────────
MONGO_URI  = "mongodb://localhost:27017/"
DB_NAME    = "quickeats"
SECRET_KEY = "quickeats-secret-2026"

app = Flask(__name__, static_folder='frontend', static_url_path='/static')
app.secret_key = SECRET_KEY
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ── MongoDB ───────────────────────────────────────────────────
_client = None
def get_db():
    global _client
    try:
        if _client is None:
            _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
            _client.server_info()
        return _client[DB_NAME]
    except Exception as e:
        print(f"[MONGO ERROR] {e}")
        _client = None
        return None

def hp(pw): return hashlib.sha256(pw.encode()).hexdigest()
def gc(): return 'QE' + ''.join(random.choices(string.digits, k=6))
def oid(s):
    try: return ObjectId(s)
    except: return None

from functools import wraps
def auth(f):
    @wraps(f)
    def d(*a,**k):
        if 'uid' not in session:
            return jsonify({'error':'Please login first'}),401
        return f(*a,**k)
    return d

# ── Serve frontend ────────────────────────────────────────────
@app.route('/')
def index(): return send_file('frontend/index.html')

# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════
@app.route('/api/auth/register', methods=['POST'])
def register():
    d     = request.get_json(force=True) or {}
    name  = (d.get('name') or '').strip()
    email = (d.get('email') or '').strip().lower()
    pw    = d.get('password') or ''
    phone = (d.get('phone') or '').strip()
    if not all([name,email,pw,phone]):
        return jsonify({'error':'All fields are required'}),400
    if len(pw)<6:
        return jsonify({'error':'Password must be at least 6 characters'}),400
    if '@' not in email:
        return jsonify({'error':'Invalid email address'}),400
    db = get_db()
    if db is None: return jsonify({'error':'Cannot connect to MongoDB. Is it running?'}),500
    if db.Users.find_one({'email':email}):
        return jsonify({'error':'This email is already registered'}),409
    doc = {
        'name':name,'email':email,'phone':phone,
        'password_hash':hp(pw),
        'joined_date':datetime.utcnow().strftime('%Y-%m-%d'),
        'created_at':datetime.utcnow()
    }
    res = db.Users.insert_one(doc)
    uid = str(res.inserted_id)
    session['uid'] = uid
    session['uname'] = name
    return jsonify({'success':True,'user':{'id':uid,'name':name,'email':email,'phone':phone,'joined':doc['joined_date']}})

@app.route('/api/auth/login', methods=['POST'])
def login():
    d     = request.get_json(force=True) or {}
    email = (d.get('email') or '').strip().lower()
    pw    = d.get('password') or ''
    if not email or not pw:
        return jsonify({'error':'Email and password required'}),400
    db = get_db()
    if db is None: return jsonify({'error':'Cannot connect to MongoDB. Is it running?'}),500
    user = db.Users.find_one({'email':email,'password_hash':hp(pw)})
    if not user: return jsonify({'error':'Invalid email or password'}),401
    uid = str(user['_id'])
    session['uid'] = uid
    session['uname'] = user['name']
    return jsonify({'success':True,'user':{
        'id':uid,'name':user['name'],'email':user['email'],
        'phone':user.get('phone',''),'joined':user.get('joined_date','')
    }})

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success':True})

@app.route('/api/auth/me')
def me():
    if 'uid' not in session: return jsonify({'user':None})
    db = get_db()
    if db is None: return jsonify({'user':None})
    user = db.Users.find_one({'_id':oid(session['uid'])})
    if not user: session.clear(); return jsonify({'user':None})
    return jsonify({'user':{
        'id':str(user['_id']),'name':user['name'],'email':user['email'],
        'phone':user.get('phone',''),'joined':user.get('joined_date','')
    }})

# ══════════════════════════════════════════════════════════════
# RESTAURANTS
# ══════════════════════════════════════════════════════════════
@app.route('/api/restaurants')
def restaurants():
    db = get_db()
    if db is None: return jsonify([])
    docs = list(db.Restaurant.find({'is_open':True}).sort('is_popular',DESCENDING))
    for r in docs: r['_id'] = str(r['_id'])
    return jsonify(docs)

# ══════════════════════════════════════════════════════════════
# MENU
# ══════════════════════════════════════════════════════════════
@app.route('/api/restaurants/<rid>/menu')
def menu(rid):
    db = get_db()
    if db is None: return jsonify([])
    items = list(db.Menu.find({'restaurant_id':rid,'is_available':True}))
    for i in items:
        i['_id'] = str(i['_id'])
        i['price'] = float(i.get('price',0))
    return jsonify(items)

# ══════════════════════════════════════════════════════════════
# ORDERS  (creates Order + Order_items + Payment docs)
# ══════════════════════════════════════════════════════════════
@app.route('/api/orders', methods=['GET'])
@auth
def get_orders():
    db = get_db()
    if db is None: return jsonify([])
    orders = list(db.Orders.find({'user_id':session['uid']}).sort('order_date',DESCENDING))
    result = []
    for o in orders:
        oid_str = str(o['_id'])
        o['_id'] = oid_str
        if isinstance(o.get('order_date'),datetime):
            o['order_date'] = o['order_date'].strftime('%Y-%m-%d %H:%M')
        o['total_amount'] = float(o.get('total_amount',0))
        # Fetch order items
        items = list(db.Order_items.find({'order_id':oid_str}))
        for it in items:
            it['_id'] = str(it['_id'])
            it['unit_price'] = float(it.get('unit_price',0))
        o['items'] = items
        # Fetch payment
        pay = db.Payment.find_one({'order_id':oid_str})
        if pay:
            pay['_id'] = str(pay['_id'])
            o['payment'] = pay
        result.append(o)
    return jsonify(result)

@app.route('/api/orders', methods=['POST'])
@auth
def place_order():
    d         = request.get_json(force=True) or {}
    items     = d.get('items',[])
    rid       = d.get('restaurant_id','')
    rname     = d.get('restaurant_name','')
    total     = float(d.get('total',0))
    address   = (d.get('address') or '').strip()
    pay_meth  = d.get('payment_method','cash')

    if not items or not address:
        return jsonify({'error':'Missing required order info'}),400

    db = get_db()
    if db is None: return jsonify({'error':'Database error'}),500

    code = gc()
    now  = datetime.utcnow()

    # 1. Insert into Orders
    order_doc = {
        'order_code':       code,
        'user_id':          session['uid'],
        'user_name':        session.get('uname',''),
        'restaurant_id':    rid,
        'restaurant_name':  rname,
        'total_amount':     total,
        'delivery_address': address,
        'order_status':     'pending',
        'order_date':       now,
    }
    o_res   = db.Orders.insert_one(order_doc)
    order_id = str(o_res.inserted_id)

    # 2. Insert into Order_items
    oi_docs = [{
        'order_id':   order_id,
        'order_code': code,
        'item_id':    it.get('id',''),
        'item_name':  it.get('name',''),
        'emoji':      it.get('emoji','🍽️'),
        'quantity':   int(it.get('qty',1)),
        'unit_price': float(it.get('price',0)),
        'subtotal':   float(it.get('price',0)) * int(it.get('qty',1)),
    } for it in items]
    db.Order_items.insert_many(oi_docs)

    # 3. Insert into Payment
    db.Payment.insert_one({
        'order_id':       order_id,
        'order_code':     code,
        'user_id':        session['uid'],
        'payment_method': pay_meth,
        'payment_status': 'pending',
        'amount':         total,
        'created_at':     now,
    })

    return jsonify({'success':True,'order_id':code})

# ══════════════════════════════════════════════════════════════
# PROFILE  (stats from Orders collection)
# ══════════════════════════════════════════════════════════════
@app.route('/api/profile')
@auth
def profile():
    db = get_db()
    if db is None: return jsonify({'error':'DB error'}),500
    user = db.Users.find_one({'_id':oid(session['uid'])})
    if not user: return jsonify({'error':'User not found'}),404
    pipe = [
        {'$match':{'user_id':session['uid']}},
        {'$group':{'_id':None,'count':{'$sum':1},'total':{'$sum':'$total_amount'}}}
    ]
    agg = list(db.Orders.aggregate(pipe))
    stats = {'cnt':agg[0]['count'],'total':float(agg[0]['total'])} if agg else {'cnt':0,'total':0}
    return jsonify({
        'user':{'id':str(user['_id']),'name':user['name'],'email':user['email'],
                'phone':user.get('phone',''),'joined':user.get('joined_date','')},
        'stats':stats
    })

# ══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("="*52)
    print("  ⚡ QuickEats — MongoDB Edition")
    print("  🌐 Open: http://localhost:5000")
    print("  ⏹  Stop: Ctrl+C")
    print("="*52)
    app.run(debug=True, port=5000, host='0.0.0.0')
