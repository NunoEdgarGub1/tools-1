
#!/usr/bin/env python2
# 
"""

@author: Cristian Bonato

Class that allows to save all variables in HDF5 files
One can also save the code in specific modules, listed in self._called_modules

Classes that need to load/save data from HDF5 files can inherit this class

"""
import numpy as np
import datetime
import h5py
import os, sys

class TimeStampObject ():

	def __init__ (self, data_folder):
		self._called_modules = []
		self._data_folder = data_folder

	def _fill_datetime_str (self, value):
		if (len(value) == 4):
			value += '01'
		if (len(value) == 6):
			value += '01'
		if (len(value) == 8):
			value += '_'
		
		return value.ljust (15, '0')

	def parse_datetime_str (self, value, fill_void_in = True):

		if fill_void_in:
			value = self._fill_datetime_str (value)

		try:
			time_stamp = datetime.datetime.strptime (value, '%Y%m%d_%H%M%S')
			return time_stamp
		except:
			print ("String not valid as time tag")
			return None

	def folder_is_valid (self, folder):
		'''
		This methods will be overloaded by the specific object
		and will tell whether the folder content fulfills 
		what is expected by the specific type of dataset

		Returns:
			bool -- [description]
		'''
		return True


	def get_file_list (self, folder=None):

		if (folder == None):
			folder = self._data_folder

		file_list = [f for f in os.listdir(folder) 
				if (os.path.isfile(os.path.join(folder, f)))]
		return file_list

	def get_folder_list (self, folder=None):

		if (folder == None):
			folder = self._data_folder

		folder_list = [f for f in os.listdir(folder) 
				if (os.path.isdir(os.path.join(folder, f)))]
		return folder_list

	def get_data_folder_list (self, folder=None):

		folder_list = self.get_folder_list (folder = folder)
		data_folder_list = []
		time_stamp_list = []

		for f in folder_list:
			try:
				tag = f[:15]
				time_tag = self.parse_datetime_str (value = tag, fill_void_in = False)
				valid_tag = True
			except:
				valid_tag = False

			if valid_tag:
				if self.folder_is_valid (f):
					data_folder_list.append(f)
					time_stamp_list.append(time_tag)

		return data_folder_list, time_stamp_list

	def get_data_with_tag (self, tag_list = [], logic_operator = 'all'):

		tag_data_list = []

		if (logic_operator in ['all', 'any']):

			data_folder_list, time_stamp_list = self.get_data_folder_list ()

			for f in data_folder_list:

				if self.folder_is_valid (f):

					bool_list = [(t in f) for t in tag_list]

					if (logic_operator == 'all'):
						valid = all(bool_list)
					elif (logic_operator == 'any'):
						valid = any (bool_list)

					if valid:
						tag_data_list.append (f)
		
		else:
			print ("Allowed logic operators: all, any")

		return tag_data_list


	def get_data_between_stamps (self, later_than, earlier_than):

		f_list = []

		if ((later_than != None) and (earlier_than != None)):
			t1 = self.parse_datetime_str (later_than, fill_void_in = True)
			t2 = self.parse_datetime_str (earlier_than, fill_void_in = True)

			f_list = []
			t_list = []

			if ((t1 != None) and (t2 != None)):

				data_folder_list, time_stamp_list = self.get_data_folder_list ()

				for idx, t in enumerate(time_stamp_list):

					if ((t<=t2) and (t>=t1)):
						f_list.append (data_folder_list[idx])

		return f_list



class DataObjectHDF5 (TimeStampObject):
	
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
				try:
					# there's some problems when saving lists of strings
					b = [type (s) for s in obj.__dict__[k]]
					c = [s is str for s in b]
					if (any(c)):
						pass
					else:
						file_handle.create_dataset (k, data = getattr (obj, k))
				except:
					pass
					
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



