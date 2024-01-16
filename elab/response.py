from flask import jsonify



def response_message(message,result='no',code=404):
    return jsonify({
        'result':result,
        'message':message
    }),code

def response_data(data):
    return jsonify({
        'result':'ok',
        'data':data
    }),200
