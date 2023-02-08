def get_by_key_or_value(dict:dict, target):
    value = dict.get(target)
    if value is None:
        dict = reverse_dict(dict)
        value = dict.get(target, 0)        
   
    return value

def reverse_dict(dict:dict):
     return dict.__class__(map(reversed, dict.items()))
 
def update_dict(dict:dict, dict2:dict):
    for key, value in dict.items():
        if key in dict2:
            dict2[key] = value
    return dict2

    
    