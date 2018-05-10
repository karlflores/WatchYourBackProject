class Stack(object):
    def __init__(self):
        pass

    @staticmethod
    def peek(stack):
        # return the last item in the stack
        if len(stack) > 0:
            return stack[-1]
        else:
            return None

    @staticmethod
    def pop(stack):
        # return the last item in the stack and remove it from the stack
        # if there is nothing in the stack return None -- need to check this
        if len(stack) > 0:
            return stack.pop()
        else:
            return None


    @staticmethod
    def push(stack,value):
        # add a value to the end of the stack
        stack.append(value)
        return
