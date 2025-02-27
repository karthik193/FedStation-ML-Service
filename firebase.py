'''
Firebase Credentials 
'''

'''imports'''
from unicodedata import name
from fastapi import UploadFile
import firebase_admin
from firebase_admin import storage
import os
import pickle as pkl
import json
from prophet.serialize import model_from_json
''''''


# Download models from firebase : Returns list of models
def downloadModels(project_id,special=None):
    os.mkdir('model-files/')
    os.mkdir('model-files/local')
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
    
    # uploading models onto list 
    models = list()
    files = os.listdir("model-files/local/")
    for file in files:
        filename = "model-files/local/"+file
        if special == True:
            with open(filename, 'r') as fin:
                loaded_model = model_from_json(json.load(fin))  # Load model
        else:
            loaded_model = pkl.load(open(filename, 'rb'))
        models.append(loaded_model)
    
    return models




# Upload model to firebase : Returns response object with status property
def uploadModel(finalModel, project_id):
    pkl.dump(finalModel, open("model-files/globalModel.pkl", 'wb'))
    ds = storage.bucket()
    print(ds.list_blobs)
    bob = ds.blob("globalModels/"+project_id)
    bob.upload_from_filename("model-files/globalModel.pkl")


    #removing all files in model-files/local and globalmodel.pkl

    dir = 'model-files/local/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    os.remove('model-files/globalModel.pkl')
    os.rmdir('model-files/local')
    os.rmdir('model-files')
    
    return "success"



# dowload Global Model url from Firebase
def getGlobalModeldowloadURL(project_id):
    ds = storage.bucket()
    bob = ds.blob("globalModels/"+project_id)
    dowloadURL  = bob._get_download_url(ds.client)      
    return dowloadURL

async def getGlobalModelFile(project_id):
    ds = storage.bucket()
    bob = ds.blob("globalModels/"+project_id)
    bob.download_to_filename('model-files/globalModel.pkl'); 

# upload Models to Firebase
async def uploadModelToFirebase(project_id , model : UploadFile):
    ds = storage.bucket()
    bob = ds.blob(project_id+"/" + model.filename +".pkl")
    try:
        bob.upload_from_file(model.file)
        return "File Uploaded"
    except Exception as e:
        print(e)
        return "Error"
    finally:
        model.file.close()
     