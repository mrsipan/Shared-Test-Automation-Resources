import json
import re

# -------  SELECT VALUE OF SOME KEY IN A DICTIONARY IF ANOTHER KEY CONTAINS A PARTICULAR VALUE  -------------

def extract_value(targetkey, source='', ifkey='', containsvalue=''):
    """ From simple JSON string like {key:value, key:value} (no substructures) returns the value of the target key if a string
    is present in the value of the condition key (ifkey).
    The value passed in should look similar to a single Python dictionary. This will not work properly on multiple-item JSON structures

    Robot Framework example usage: ${var_name} =   Extract Value   'guid'   source=${json_input}  ifkey='name'   containsvalue='python'
    this example will return the value of key named 'guid' IF the word 'python' is contained in the key called 'name'
    :rtype: object"""

    if source == '':
        raise Exception("ERROR: function extract_value received empty string as argument: source")
    if containsvalue == '' or ifkey == '' or targetkey == '':
        raise Exception("ERROR: function extract_value received empty string as argument: in either target key (from it you get the value you seek), condition key (contains value you match with your condition--ifkey), or condition value have not been passed in function call")
   # now DECODING json string 'source' passed in, it becomes a Python dictionary
    data  = json.loads(source)
   # extracting value of condition key
    condition_key_value = data[ifkey]
   # now if the value of condition key contains our condition value, the following is executed
    if containsvalue.lower() in condition_key_value.lower():
        result = data[targetkey]
        return result



# -------  SELECTING ITEM IF ONE OF ITS KEYS CONTAINS AND/OR EXCLUDES A PARTICULAR VALUE  ---------------

def conditionally_choose_item(jsonstring, bykey='', containingvalue = '',
                              excludingvalue = 'E_LK--q-+c--mbznmFFk-+b_fTMpa'):

    """
    :param jsonstring: JSON string of form {key:value, key:value}
    :param bykey: the name of key by which to filter
    :param containingvalue: value by which the item is selected
    :param excludingvalue: value by which the item is discarded
    :return: item itself if satisfies conditions

    This returns the JSON string passed in only if this JSON string satisfies specified conditions. It is a filter. Same
    logic as in extract_value, only return is different. Also you can specify a 'negative condition value', with will
    EXCLUDE anything that contains that value. Positive and negative condition values are optional arguments, but you
    should specify at least one of these to or the function will not work

    Robot Framework Exampele usage: ${var_name} =   Conditionally Choose Item    input    bykey=name    containingvalue=Python
    excludingvalue=Ruby
    This example returns the item passed in if this item's 'name' key contains the word 'Python' and DOES NOT contain 'Ruby' """

    if jsonstring == '':
        raise Exception("ERROR: function conditionally_choose_item received empty string as argument: jsonstring")
    if bykey == '':
        raise Exception("ERROR: function conditionally_choose_item received empty string as argument: bykey (they key you want to examine)")
    data = json.loads(jsonstring)
    condition_key_value = data[bykey]
    cond_key_val_lowercase = condition_key_value.lower()
    if containingvalue.lower() in cond_key_val_lowercase and excludingvalue.lower() not in cond_key_val_lowercase:
        return jsonstring




# -------  SELECT FROM INPUT, ALL THE ITEMS WHOSE SPECIFIC KEY CONTAINS A PARTICULAR VALUE AND/OR EXCLUDES ANOTHER VALUE

def select_items_from(inputstr, bykey='', containingvalue = '',
                        excludingvalue = 'E_LK--q-+c--mbznmFFk-+b_fTMpa'):

    """
    This uses conditionally_choose_item in a loop to select a list of dictionaries (converted from JSON input)

    :param inputstr: JSON input, such as an HTTP json response content
    :param bykey: name of the key by which you filter the inputstr
    :param containsvalue: value by which you select an item
    :param excludesvalue: value by which you discard an item
    :return: list of items chosen according to values they contain or do not contain (exclude)

    Robot Framework example usage: ${var_name} =    Select Items From    myhttpresponse    bykey=name   containingvalue=Python
    excludingvalue=Ruby
    """

    if inputstr == '':
        raise Exception("ERROR: pick_from_json_list function received empty string as argument: inputstr")
    if bykey == '':
        raise Exception("ERROR: pick_from_json_list function received empty string as argument: bykey")

    json_struct = json.loads(inputstr)
    chosen_list = []
    for eachItem in json_struct:
        json_elem = json.dumps(eachItem)
        chosen_item=conditionally_choose_item(json_elem, bykey, containingvalue, excludingvalue)
        if chosen_item != None:
            chosen_list.append(chosen_item)
    return chosen_list



def extract_first_value_from_list(inputlist, targetkey=''):
    """
    :param inputlist: a list of dictionaries
    :param targetkey: the key whose value is targeted
    :return: the value of the first target key

    This takes LIST type as input argument and returns the value of the target dictionary key from the FIRST item in
      the list
     make sure any filtering for target values has been done before this method is invoked. Use select_items_from
     for that

     Robot Framework example usage: ${var_name} =   Extract Value From List   input   targetkey=guid
     This example returns the value of key 'guid' from the JSON dictionary """

    whitespace = re.compile('[ \t\n\r\f]+')
    for i in range(0, len(inputlist)):
        json_input = json.loads(inputlist[i])
        if len(json_input[targetkey])>0 and whitespace.match(json_input[targetkey]) == None:
            return json_input[targetkey]

def extract_value_from_list_of_json_dictionaries(targetkey, inputlist, ifkey='', containsvalue=''):
    """
    :param inputlist: a list of JSON dictionaries (JSON strings that look like Python dictionaries)
    :param targetkey: the key whose value is targeted
    :return: the value of the target key

    This takes LIST type as input argument and returns the value of the target dictionary key from the item in
      the list
     Make sure any filtering for target values has been done before this method is invoked. Use select_items_from
     for that, or any other method to generate your list
     The 'dictionaries' in the list are actually JSON strings resembling Python dictionaries that still require
     conversion to actual Python dictionaries by json.loads(). This occurs withing extract_value function, hence
     the reason why extract value function requires a STRING type for its 'source' parameter, not an actual dictionary

     Robot Framework example usage:
     ${var_name} =   Extract Value From List Of Json Dictionaries   targetkey=guid   input   ifkey=name    containsvalue=Bob
     This example returns the value of key 'guid' from the JSON dictionary if the 'name' key in that dictionary
    contains the string 'Bob' """

    for i in range(0, len(inputlist)):
        targetvalue = extract_value(targetkey, inputlist[i], ifkey=ifkey, containsvalue=containsvalue)
        if targetvalue != None:
            return targetvalue



















        # if len(json_input[targetkey])>0 and whitespace.match(json_input[targetkey]) == None:
        #     return json_input[targetkey]
# def pick_from_json_list(inputstr, conditionkey, positiveconditionvalue = '',
#                         negativeconditionvalue = 'E_LK--q-+c--mbznmFFk-+b_fTMpa'):
#     """ This uses conditionally_choose_item in a loop to select a list of dictionaries (converted from JSON input)
#
#      Robot Framework example usage: ${var_name} =   Pick From Json List   input   'name'   'Python'   'Ruby'
#      This example returns a list of dictionaries whose 'name' keys contain 'python' and DO NOT contain 'Ruby' """
#
#     if inputstr == '':
#         raise Exception("ERROR: pick_from_json_list function received empty string as argument: inputstr")
#     if conditionkey == '':
#         raise Exception("ERROR: pick_from_json_list function received empty string as argument: conditionkey")
#
#     json_struct = json.loads(inputstr)
#     chosen_list = []
#     for eachItem in json_struct:
#         json_elem = json.dumps(eachItem)
#         chosen_item=conditionally_choose_item(json_elem, conditionkey, positiveconditionvalue, negativeconditionvalue)
#         if chosen_item != None:
#             chosen_list.append(chosen_item)
#     return chosen_list
