#!/usr/bin/env python
# coding: utf-8

# In[22]:


from tqdm import tqdm

# arr = [x for x in range(1000000)]

class Pipe:
    def __init__(self):
        self.pipes = []
    
    # Applies all the functions in pipeline to each element. Returns modified array
    def __call__(self, data):
        for func in self.pipes:
            data = list(map(func, tqdm(data, desc=func.__name__)))
        return data
    
    # Adds function to Pipe.process pipeline
    def addPipe(self, func):
        # Checking for type of argument
        if type(func) is list:
            # arg func is <class 'list'>
            self.pipes += func
        elif hasattr(func, '__call__'):
            # arg func is <class 'function'>
            self.pipes.append(func)
        
# def addOne(item):
#     return item + 1

# def square(item):
#     return item ** 2

# def printItem(item):
#     print(item)
#     return item

# pipe = Pipe()
# pipe.addPipe([addOne])
# pipe.addPipe([square])
# res = pipe(arr)


# In[ ]:




