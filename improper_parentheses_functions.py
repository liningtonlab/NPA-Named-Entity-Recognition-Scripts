# Python3 program to remove invalid parenthesis using modified code from: https://www.geeksforgeeks.org/remove-invalid-parentheses/
def is_parentheses(c):
    """ Method checks if character is parenthesis(open or closed)
            :param c: character
            :return: if it is open/closed parentheses
            """
    return (c == '(') or (c == ')')


def is_valid_string(string):
    """ Method returns true if contains valid parentheses
                :param string: string
                :return: False if open bracket otherwise 0 when valid parentheses
                """
    cnt = 0
    for i in range(len(string)):
        if string[i] == '(':
            cnt += 1
        elif string[i] == ')':
            cnt -= 1
        if cnt < 0:
            return False
    return cnt == 0


def remove_invalid_parentheses(string):
    """ Method to remove invalid parenthesis
                    :param string: string
                    :return: False if open bracket otherwise 0 when valid parentheses
                    """
    if len(string) == 0:
        return

    # visit set to ignore already visited
    visit = set()

    # queue to maintain BFS
    q = []
    temp = 0
    level = 0

    # pushing given as starting node into queue
    q.append(string)
    visit.add(string)
    while len(q):
        string = q[0]
        q.pop()

        if is_valid_string(string):
            level = True  # If answer is found, make level true; so that valid of only that level are processes
            return string

        if level:
            continue
        for i in range(len(string)):
            if not is_parentheses(string[i]):
                continue

            # Removing parenthesis from str and pushing into queue,if not visited already
            temp = string[0:i] + string[i + 1:]
            if temp not in visit:
                q.append(temp)
                visit.add(temp)
