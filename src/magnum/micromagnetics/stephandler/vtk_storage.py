from .storage_stephandler import StorageStepHandler

from magnum.micromagnetics.io import writeVTK
from magnum.micromagnetics.io.vtk import *

import os.path

class VTKStorage(StorageStepHandler):
  def __init__(self, output_dir, field_id_or_ids = []):
    super(VTKStorage, self).__init__(output_dir)

    if hasattr(field_id_or_ids, "__iter__"):
      field_ids = list(field_id_or_ids)
    else:
      field_ids = [field_id_or_ids]
    if not all(isinstance(x, str) for x in field_ids):
      raise ValueError("VTKStorage: 'field_id' parameter must be a either a string or a collection of strings.")

    def make_file_fn(field_id):
      # Create file name creating function 'file_fn'
      pattern = "%s-%%07i.vtr" % field_id
      return lambda state: pattern % state.step

    self.__groups = {}

    for field_id in field_ids:
      self.addVariable(field_id, make_file_fn(field_id))

    self.addComment("timestep", lambda state: state.t)
    self.addComment("stepsize", lambda state: state.h)
    self.addComment("step", lambda state: state.step)

  def store(self, id, path, field, comments):
    writeVTK(path, field)

    # To add the entry to the pvd group, strip the file name from path.
    self.__groups[id].addFile(filepath=os.path.basename(path), **dict(comments))

  def done(self):
    for group in self.__groups.values():
      group.save()

  def addVariable(self, var_id, file_fn, field_fn = None):
    super(VTKStorage, self).addVariable(var_id, file_fn, field_fn)
    pvd_filename = "Group-%s.pvd" % var_id
    self.__groups[var_id] = VtkGroup(self.getOutputDirectory(), pvd_filename)