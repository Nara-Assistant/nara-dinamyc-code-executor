import json
import uuid
import requests
from flask import Flask, request

app = Flask(__name__)

global_dict = {

}

def internal_calling_set(unique_id, data):
    global_dict[unique_id] = data
def internal_calling_get(unique_id):
    return global_dict[unique_id]
def internal_calling_clear(unique_id):
    del global_dict[unique_id]

def wrapper(function_name, function_caller):
    print(function_name, function_caller)
    unique_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'nara-executor.com'))
    compiled_code = compile(function_name + "\ninternal_calling_set(unique_id, "+function_caller+")", '<string>', 'exec')
    exec(compiled_code)


    exec_response = internal_calling_get(unique_id)
    internal_calling_clear(unique_id)

    return exec_response

   

@app.route("/executor", methods=['POST'])
def executor():
    data = request.get_json()
    function_name = data.get("function_name", "def hello_world():\n  return 'hello world'") or "def hello_world():\n  return 'hello world'"
    function_caller = data.get("function_caller", "hello_world()") or "hello_world()"
    response = None
    try:
        response = wrapper(function_name, function_caller)
        print(response, global_dict)
    except Exception as e:
        print(e)
        return { "message": "error" }, 500
   

    return {
       "data": response
    }, 200


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=7070)