import json
import uuid
import requests
from flask import Flask, request

app = Flask(__name__)

global_dict = {

}

import json
import requests 




def internal_calling_set(unique_id, data):
    global_dict[unique_id] = data
def internal_calling_get(unique_id):
    return global_dict[unique_id]
def internal_calling_clear(unique_id):
    del global_dict[unique_id]

def wrapper(function_name, function_caller, function_params_extractor, function_params):
    print(function_name, function_caller)
    unique_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'nara-executor.com'))

    compiled_code = compile(f"""
{function_name}
{function_params_extractor}
_response = {function_caller}(parameters_array({json.dumps(function_params)}))
internal_calling_set(unique_id, _response)"
print(response)
""")
    exec(compiled_code)


    exec_response = internal_calling_get(unique_id)
    internal_calling_clear(unique_id)

    return exec_response

   

@app.route("/executor", methods=['POST'])
def executor():
    data = request.get_json()
    function_params = data.get("fn_params", {})
    function_name = data.get("function_name", "def hello_world():\n  return 'hello world'") or "def hello_world():\n  return 'hello world'"
    function_caller = data.get("function_caller", "hello_world()") or "hello_world()"
    function_params_extractor = data.get("function_params_extractor", "parameters_array = lambda parameters : []") or "parameters_array = lambda parameters : []"
    response = None
    try:
        response = wrapper(function_name, function_caller, function_params_extractor, function_params)
        print(response, global_dict)
    except Exception as e:
        print(e)
        return { "message": "error" }, 500
   

    return {
       "data": response
    }, 200


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=7070)