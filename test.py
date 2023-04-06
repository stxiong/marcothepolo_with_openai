from langdetect import detect

a = 'this is check'
ret = detect(a)
print(ret)
print(type(ret))
