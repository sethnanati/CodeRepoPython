import pickle

# it is used to serialize and deserialize objects.
# a serialized object can be saved and loaded frorm the disk
#

#SERIALIZATION OR SAVING AN OBJECT
objtosave = {'python': 3, 'KDE': 5, 'Windows': 10, 'testing': 20}

fileObj = open('data.obj', 'wb')
pickle.dump(objtosave, fileObj)
fileObj.close()

#DESERIALIZATION OR READING A SAVED OBJECT
fileObj = open('data.obj', 'rb')
objtoread = pickle.load(fileObj)
fileObj.close()
print(objtoread)
