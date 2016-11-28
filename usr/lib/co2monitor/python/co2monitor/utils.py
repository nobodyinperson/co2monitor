#!/usr/bin/env python3
import os
import re

# split a path into its components
def splitpath(path):
    res = []
    # split the path
    while True:
        base, subject = os.path.split(path)
        if path == base:
            break
        else:
            if subject: res.append(subject) 
        path = base
    res.reverse()
    return res


# convert a device file path to a DBus object name last part
def devicefile2objectname(devicefile):
    return "_".join(splitpath(os.path.realpath(devicefile)))


# # convert a DBus object name last part to a device file path
# def objectname2devicefile(objectname):
#     s = objectname.split("-")
#     print("full split of -: {}".format(s))
#     res = ["/"]
#     c = False
#     for e in s:
#         print("element is '{}'".format(e))
#         if e:
#             if c:
#                 print("appending element '{}' to last element of res {}".format(e,res[len(res)-1],res))
#                 res[len(res)-1] = "{}{}".format(res[len(res)-1],e)
#                 c = False
#             else:
#                 print("appending element '{}' to res {}".format(e,res))
#                 res.append(e)
#         else:
#             print("appending a '-' to last element '{}' of res {}".format(res[len(res)-1],res))
#             res[len(res)-1] = "{}-".format(res[len(res)-1])
#             c = True
#         print("---------------")
#     return os.path.join(*res)



