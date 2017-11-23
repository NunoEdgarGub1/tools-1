
#!/usr/bin/env python2
# 
"""

@author: Cristian Bonato

Class that allows to save all variables in HDF5 files
One can also save the code in specific modules, listed in self._called_modules

Classes that need to load/save data from HDF5 files can inherit this class

"""
import numpy as np

class DataObjectHDF5 ():
	
	def __init__(self):
		self.data_dict = {}
		self._called_modules=[]

	def save_dict_to_file(self, d, file_handle):
		for k in d.keys():
			if isinstance(d[k], dict):
				grp = file_handle.create_group(k)
				self.save_dict_to_file (d = d[k], file_handle = grp)
			elif (type (d[k]) in [int, float, str]):
				file_handle.attrs[k] = d[k]
			elif isinstance(d[k], np.int32):
				file_handle.attrs[k] = d[k]
			elif isinstance(d[k], np.float64):
				file_handle.attrs[k] = d[k]
			elif isinstance(d[k], np.ndarray):
				file_handle.create_dataset (k, data = d[k])

	def load_file (self, file_name):
		f = h5py.File(file_name,'r')
		for k in f.attrs.keys():
			setattr (self, k, f.attrs [k])
		
	def store_function_code (self):
		self.data_dict['code'] = {}
		for i in self._called_modules:
			try:
				self.data_dict['code'][i] = inspect.getsource(getattr(self, i))
			except:
				print "Non-existing function: ", i
		return self.data_dict['code']

	def save_object_to_file (self, obj, f):

		if type(f) is str:
			if (f[-5:] != '.hdf5'):
				f = f+'.hdf5'
			file_handle = h5py.File(f, 'w')
		else:
			file_handle = f

		for k in obj.__dict__.keys():
			if (type(obj.__dict__[k]) in [int, float, str]):
				file_handle.attrs[k] = getattr (obj, k)
			elif isinstance(obj.__dict__[k], np.float64):
				file_handle.attrs[k] = getattr (obj, k)
			elif isinstance(obj.__dict__[k], np.int32):
				file_handle.attrs[k] = getattr (obj, k)
			elif isinstance(obj.__dict__[k], np.ndarray):
				file_handle.create_dataset (k, data = getattr (obj, k))

		if type(f) is str:
			file_handle.close()




