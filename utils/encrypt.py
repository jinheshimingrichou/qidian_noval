#!/usr/bin/env python
# -*- coding:utf-8 -*-
import uuid
import hashlib




def md5(string):
    """ MD5加密 """
    SECRET_KEY='njknvhghdfggbd'
    hash_object = hashlib.md5(SECRET_KEY.encode('utf-8'))
    kk=hash_object.update(string.encode('utf-8'))
    print(len(hash_object.hexdigest()))
    return hash_object.hexdigest()


def uid(string):
    data = "{}-{}".format(str(uuid.uuid4()), string)
    return md5(data)
