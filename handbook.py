"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.
Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 
We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.
NOTE: We do not expect you to come up with a perfect solution. We are more interested
in how you would approach a problem like this.
""" 
import json, re
 
# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

count_or = 0

def get_all_must_completed_course(requirements_list):
    ''''
    get all the must completed course from the list
    if there is "AND" or "and", then the course besides "AND" and "and" must be completed
    '''
    pre_must_list = []  
    and_index = -1
    global count_or
    while "and" in requirements_list:
        and_index = requirements_list.index("and")
        first_must = requirements_list[and_index - 1]
        if "(" not in first_must and ")" not in first_must: 
            pre_must_list.append(first_must)
        second_must = requirements_list[and_index + 1]
        if "(" not in second_must and ")" not in second_must: 
            pre_must_list.append(second_must)  
        if "(" in first_must and ")" in second_must:
            pre_must_list.append(second_must)
            pre_must_list.append(first_must) 
            count_or += 2
        requirements_list.remove("and") 

    while "AND" in requirements_list:
        and_index = requirements_list.index("AND") 
        first_must = requirements_list[and_index - 1]
        if "(" not in first_must and ")" not in first_must: 
            pre_must_list.append(first_must) 
        second_must = requirements_list[and_index + 1]
        if "(" not in second_must and ")" not in second_must: 
            pre_must_list.append(second_must)  
        if "(" in first_must and ")" in second_must:
            pre_must_list.append(second_must.replace(")", ""))
            pre_must_list.append(first_must.replace("(", "")) 
            count_or += 2
        requirements_list.remove("AND") 
    return pre_must_list
    
def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json
    You can assume all courses are worth 6 units of credit
    """
    
    # TODO: COMPLETE THIS FUNCTION!!! 
    # satisfy pre_conditions  
    if len(courses_list) == 0 and target_course != "COMP1511":
        return False

    prerequisites = CONDITIONS[str(target_course)]

    # get all the numerics that can be units of the course code by regex
    pattern = re.compile(r"\(?\s?\,?([A-Z]*\d*)")    
    match = re.findall(pattern, prerequisites)  

    pre_list = []
    units = 0

    # get the number of units and the course code which are inserted to the pre_list
    for course in match:
        re.sub(r"[^\w\s]", '', course) 
        if len(course) != 0: 
            if course.isnumeric():
                units = int(course) 
            else:
                if (len(course) == 8):
                    pre_list.append(course) 

    requirements_list = prerequisites.split() 
    global count_or
    count_or += prerequisites.count("OR")
    count_or += prerequisites.count("or")  

    # get all the must-completed courses
    pre_must_list = get_all_must_completed_course(requirements_list)  

    # if there is no specific prerequisites code, then check whether the number of units are met 
    if len(pre_list) == 0 and units != 0:  
        if len(courses_list) * 6 >= units:
            return True   

    for c in pre_list:
        if c not in courses_list:
            if count_or <= 0:
                return False
            count_or -= 1  

    for c in pre_must_list:
        if c not in courses_list:
            return False 

    if len(courses_list) * 6 <= units and units != 0:  
        return False 
    return True 