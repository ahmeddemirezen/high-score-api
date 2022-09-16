def param_to_html(content, param, value):
    return content.replace('{{'+param+'}}', value)

def params_to_html(content, params):
    temp = content
    for param in params.keys():
        temp = temp.replace('{{'+param+'}}', params[param])
    return temp
