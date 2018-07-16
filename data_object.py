
#!/usr/bin/env python2
# 
"""

@author: Cristian Bonato

Class that allows to save all variables in HDF5 files
One can also save the code in specific modules, listed in self._called_modules

Classes that need to load/save data from HDF5 files can inherit this class

"""
import numpy as np
import h5py

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

	def load_all_attributes (self, obj, file_handle):
		for k in file_handle.attrs.keys():
			setattr (obj, k, file_handle.attrs [k])

	def load_all_datasets (self, obj, file_handle):
		x, nsb_datasets = self.find_groups_and_datasets (file_handle)

		for k in nsb_datasets:
			setattr (obj, k, file_handle[k].value)

	def load_all_into_object (self, obj, file_handle):
		self.load_all_attributes (obj=obj, file_handle = file_handle)
		self.load_all_datasets (obj=obj, file_handle = file_handle)

	def find_groups_and_datasets (self, file_handle):

		all_h5_objs = []
		file_handle.visit(all_h5_objs.append)
		all_groups   = [ obj for obj in all_h5_objs if isinstance(file_handle[obj],h5py.Group) ]
		all_datasets = [ obj for obj in all_h5_objs if isinstance(file_handle[obj],h5py.Dataset)]
		return all_groups, all_datasets

	def store_function_code (self):
		self.data_dict['code'] = {}
		for i in self._called_modules:
			try:
				self.data_dict['code'][i] = inspect.getsource(getattr(self, i))
			except:
				print ("Non-existing function: ", i)
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
				try:
					file_handle.attrs[k] = getattr (obj, k)
				except:
					file_handle[k] = getattr (obj, k)
			elif isinstance(obj.__dict__[k], np.float64):
				try:
					file_handle.attrs[k] = getattr (obj, k)
				except:
					file_handle[k] = getattr (obj, k)
			elif isinstance(obj.__dict__[k], np.int32):
				try:
					file_handle.attrs[k] = getattr (obj, k)
				except:
					file_handle[k] = getattr (obj, k)
			elif isinstance(obj.__dict__[k], np.ndarray):
				file_handle.create_dataset (k, data = getattr (obj, k))
			elif (type (obj.__dict__[k]) is list):
				# there's some problems when saving lists of strings
				b = [type (s) for s in obj.__dict__[k]]
				c = [s is str for s in b]
				if (any(c)):
					pass
				else:
					file_handle.create_dataset (k, data = getattr (obj, k))

		if type(f) is str:
			file_handle.close()

	def save_object_all_vars_to_file (self, obj, f):

		if type(f) is str:
			if (f[-5:] != '.hdf5'):
				f = f+'.hdf5'
			file_handle = h5py.File(f, 'w')
		else:
			file_handle = f

		for k in obj.__dict__.keys():
			if (type(obj.__dict__[k]) in [int, float, str]):
				try:
					file_handle.attrs[k] = getattr (obj, k)
				except:
					file_handle[k] = getattr (obj, k)
			elif isinstance(obj.__dict__[k], np.float64):
				try:
					file_handle.attrs[k] = getattr (obj, k)
				except:
					file_handle[k] = getattr (obj, k)
			elif isinstance(obj.__dict__[k], np.int32):
				try:
					file_handle.attrs[k] = getattr (obj, k)
				except:
					file_handle[k] = getattr (obj, k)
		if type(f) is str:
			file_handle.close()


	def save_object_params_list_to_file (self, obj, f, params_list):

		if type(f) is str:
			if (f[-5:] != '.hdf5'):
				f = f+'.hdf5'
			file_handle = h5py.File(f, 'w')
		else:
			file_handle = f

		for k in params_list:
			try:
				p = getattr (obj, k)
				if (type(p) in [int, float, str]):
					try:
						file_handle.attrs[k] = p
					except:
						file_handle[k] = p
				elif isinstance(p, np.float64):
					try:
						file_handle.attrs[k] = p
					except:
						file_handle[k] = p
				elif isinstance(p, np.int32):
					try:
						file_handle.attrs[k] = p
					except:
						file_handle[k] = p
				elif isinstance(p, np.ndarray):
					file_handle.create_dataset (k, data = p)
				elif (type (p) is list):
					# there's some problems when saving lists of strings
					b = [type (s) for s in p]
					c = [s is str for s in b]
					if (any(c)):
						pass
					else:
						file_handle.create_dataset (k, data = p)
			except Exception as e:
				print ("Variable ", k, " cannot be saved. Exception: ", e)
		if type(f) is str:
			file_handle.close()



