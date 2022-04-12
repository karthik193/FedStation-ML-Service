'''
Firebase Credentials 
'''

'''dummy imports please remove them if found'''
from unicodedata import name
from fastapi import UploadFile
import firebase_admin
from firebase_admin import storage
import os
''''''


# Download models from firebase : Returns list of models
def downloadModels(project_id):
    ds = storage.bucket()
    file_names = list()
    L = len(project_id)
    for b in ds.list_blobs(): 
        file_names.append(b.name)
    print(file_names , L )
    
    for file_path in file_names :
        file_dir = file_path[0:L]
        print(file_dir , file_path[L+1:])
        if(file_dir == project_id and len(file_path) > L+1):
            print("matched",file_path[L+1:])
            bob = ds.blob(file_path)
            bob.download_to_filename("model-files/local/"+ file_path[L+1:])


# Upload model to firebase : Returns response object with status property
def uploadModel(project_id):
    ds = storage.bucket()
    print(ds.list_blobs)
    bob = ds.blob("globalModels/"+project_id)
    bob.upload_from_filename("model-files/globalModel.pkl")

    #removing all files in model-files/local 
    dir = 'model-files/local/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))



# dowload Global Model url from Firebase
def getGlobalModeldowloadURL(project_id):
    ds = storage.bucket()
    bob = ds.blob("globalModels/"+project_id)
    dowloadURL  = bob._get_download_url(ds.client)      
    return dowloadURL

# upload Models to Firebase
async def uploadModelToFirebase(project_id , model : UploadFile):
    ds = storage.bucket()
    bob = ds.blob(project_id+"/" + model.filename)
    try:
        bob.upload_from_file(model.file)
        return "File Uploaded"
    except Exception as e:
        print(e)
        return "Error"
    finally:
        model.file.close()
     
