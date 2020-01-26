import json
import boto3
from flask_lambda import FlaskLambda
from flask import request


app = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('students')


@app.route('/')
def index():
    return json_response({"message": "Hello, world!"})


@app.route('/students', methods=['GET', 'POST'])
def put_list_students():
    if request.method == 'GET':
        students = table.scan()['Items']
        return json_response(students)
    else:
        table.put_item(Item=request.form.to_dict())
        return json_response({"message": "student entry created"})


@app.route('/students/<id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_student(id):
    key = {'id': id}
    if request.method == 'GET':
        student = table.get_item(Key=key).get('Item')
        if student:
            return json_response(student)
        else:
            return json_response({"message": "student not found"}, 404)
    elif request.method == 'PATCH':
        attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
                             for key, value in request.form.items()}
        table.update_item(Key=key, AttributeUpdates=attribute_updates)
        return json_response({"message": "student entry updated"})
    else:
        table.delete_item(Key=key)
        return json_response({"message": "student entry deleted"})


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
