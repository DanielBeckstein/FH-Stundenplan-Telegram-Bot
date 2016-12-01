
import pickle as pkl

##############################
#   Customize pkl functions   
##############################

def read(fname):
   f = open(fname,'rb')
   data = pkl.load(f)
   f.close()   
   return data
   
def write(data,fname):
   f = open(fname, 'wb')
   pkl.dump(data, f, pkl.HIGHEST_PROTOCOL)
   f.close()