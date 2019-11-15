import pickle

dict_api_key = {'gcp_api_key': 'AIzaSyCALNrMHjCXqOfOITmuOt0rcvCHxGnsdvw'}


with open('gcp_api_key.pkl', 'wb') as handle:
    pickle.dump(dict_api_key, handle, protocol=pickle.HIGHEST_PROTOCOL)