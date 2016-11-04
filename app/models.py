from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from app import db
from .exceptions import ValidationError, TimestampParserError
from .utils import split_url


class User(db.Document):
    created_at = db.DateTimeField(default=datetime.utcnow().isoformat(), required=True)
#     id = db.StringField(max_length=255, required=True)
    username = db.StringField(max_length=64, required=True)
    password_hash = db.StringField(max_length=128, required=True)
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True)
#     password_hash = db.Column(db.String(128))
 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
 
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
 
    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')
 
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])
 
# 
# class Customer(db.Model):
#     __tablename__ = 'customers'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), index=True)
#     orders = db.relationship('Order', backref='customer', lazy='dynamic')
# 
#     def get_url(self):
#         return url_for('api.get_customer', id=self.id, _external=True)
# 
#     def export_data(self):
#         return {
#             'self_url': self.get_url(),
#             'name': self.name,
#             'orders_url': url_for('api.get_customer_orders', id=self.id,
#                                   _external=True)
#         }
# 
#     def import_data(self, data):
#         try:
#             self.name = data['name']
#         except KeyError as e:
#             raise ValidationError('Invalid customer: missing ' + e.args[0])
#         return self


class Sensor(db.Document):
#     __tablename__ = 'sensors'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), index=True)
#     items = db.relationship('Item', backref='sensor', lazy='dynamic')
    created_at = db.DateTimeField(default=datetime.utcnow().isoformat(), required=True)
    idd = db.StringField(max_length=255, required=True, unique=True)
    name = db.StringField(max_length=255, required=True)
    items = db.DecimalField()
    
    def __repr__(self):
        return '<Product %r>' % self.idd    
    
    def get_url(self):
        return url_for('api.get_sensor', idd=str(self.idd), _external=True)
 
    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'idd': self.idd
        }
 
    def import_data(self, data):
        try:
            self.name = data['name']
            self.idd = data['idd']
        except KeyError as e:
            raise ValidationError('Invalid sensor: missing ' + e.args[0])
        return self

class Stream(db.Document):
    def default_sensor_data():
        a = {'%02d' % x: {'%02d' % y: {} for y in range (0,60)} for x in range (0,60)}
        return(a)
    
    id = db.StringField(primary_key=True, unique=True)
    data = db.DictField(default=default_sensor_data())
    

    def __repr__(self):
        return '<Stream %r>' % self.id    
     
    def get_url(self):
        return url_for('api.get_stream', id=str(self.id), _external=True)
  
    def export_data(self):
        return {
            'self_url': self.get_url(),
            'id': self.id,
            'data':self.data,
        }
  
    def import_data(self, sensor_data):
        self.data = self.update_sensor_data(self.data, sensor_data)
        return self

    @staticmethod
    def build_id(sensor_data):
        '''
        This method constructs the ID that will be used to store data in MongoDB
        ID is constructed as follow (without brackets):
        [sensor uuid]:[yyyymmddhh]
        '''
        try:
            myid = sensor_data['sensor_id'][:8]
            #ts_obj = datetime.strptime(sensor_data['ts'], "%Y-%m-%dT%H:%M:%S.%f")
            ts_obj = datetime_parser.parse(sensor_data['ts'])
            ts = ts_obj.strftime('%Y') + ts_obj.strftime('%m') + ts_obj.strftime('%d') + ts_obj.strftime('%H') 
            return myid +':'+ts
        except KeyError as e:
            print(str(e))
            print(str(sensor_data))
            raise ValidationError('Invalid sensor data: ' + str(sensor_data), e.args[0])
            return None

    def update_sensor_data(self, local_data, sensor_data):
        try:
        #ts_obj = datetime.strptime(sensor_data['ts'], "%Y-%m-%dT%H:%M:%S.%f")
            ts_obj = datetime_parser.parse(sensor_data['ts'])
        except KeyError as e:
            raise TimestampParserError('Invalid timestamp ' + sensor_data['ts'], e.args[0])
        print(ts_obj)
        minute = ts_obj.strftime('%M')
        second = ts_obj.strftime('%S')
        print(sensor_data)
        local_data[minute][second] = sensor_data['sensor_data']
        return(local_data)



# class Product(db.Model):
#     __tablename__ = 'products'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), index=True)
#     items = db.relationship('Item', backref='product', lazy='dynamic')
# 
#     def get_url(self):
#         return url_for('api.get_product', id=self.id, _external=True)
# 
#     def export_data(self):
#         return {
#             'self_url': self.get_url(),
#             'name': self.name
#         }
# 
#     def import_data(self, data):
#         try:
#             self.name = data['name']
#         except KeyError as e:
#             raise ValidationError('Invalid product: missing ' + e.args[0])
#         return self
# 
# 
# class Order(db.Model):
#     __tablename__ = 'orders'
#     id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),
#                             index=True)
#     date = db.Column(db.DateTime, default=datetime.now)
#     items = db.relationship('Item', backref='order', lazy='dynamic',
#                             cascade='all, delete-orphan')
# 
#     def get_url(self):
#         return url_for('api.get_order', id=self.id, _external=True)
# 
#     def export_data(self):
#         return {
#             'self_url': self.get_url(),
#             'customer_url': self.customer.get_url(),
#             'date': self.date.isoformat() + 'Z',
#             'items_url': url_for('api.get_order_items', id=self.id,
#                                  _external=True)
#         }
# 
#     def import_data(self, data):
#         try:
#             self.date = datetime_parser.parse(data['date']).astimezone(
#                 tzutc()).replace(tzinfo=None)
#         except KeyError as e:
#             raise ValidationError('Invalid order: missing ' + e.args[0])
#         return self


# class Item(db.Model):
#     __tablename__ = 'items'
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), index=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), index=True)
#     sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), index=True)
#     quantity = db.Column(db.Integer)
# 
#     def get_url(self):
#         return url_for('api.get_item', id=self.id, _external=True)
# 
#     def export_data(self):
#         return {
#             'self_url': self.get_url(),
#             'order_url': self.order.get_url(),
#             'product_url': self.product.get_url(),
#             #'sensor_url': self.sensor.get_url(),
#             'quantity': self.quantity
#         }
# 
#     def import_data(self, data):
#         try:
#             endpoint, args = split_url(data['product_url'])
#             self.quantity = int(data['quantity'])
#         except KeyError as e:
#             raise ValidationError('Invalid order: missing ' + e.args[0])
#         if endpoint != 'api.get_product' or not 'id' in args:
#             raise ValidationError('Invalid product URL: ' +
#                                   data['product_url'])
#         self.product = Product.query.get(args['id'])
#         if self.product is None:
#             raise ValidationError('Invalid product URL: ' +
#                                   data['product_url'])
#         return self
