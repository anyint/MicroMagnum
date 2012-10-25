from .storage_stephandler import StorageStepHandler

from magnum.micromagnetics.io import writeOMF

class OOMMFStorage(StorageStepHandler):
  def __init__(self, output_dir, field_id_or_ids = []):
    super(OOMMFStorage, self).__init__(output_dir)

    if hasattr(field_id_or_ids, "__iter__"):
      field_ids = list(field_id_or_ids)
    else:
      field_ids = [field_id_or_ids]
    if not all(isinstance(x, str) for x in field_ids):
      raise ValueError("OOMMFStorage: 'field_id' parameter must be a either a string or a collection of strings.")

    def make_file_fn(field_id):
      # Create file name creating function 'file_fn'
      pattern = "%s-%%07i" % field_id
      if field_id[0] == "H":
        pattern += ".ohf"
      else:
        pattern += ".omf"
      return lambda state: pattern % state.step

    for field_id in field_ids:
      self.addVariable(field_id, make_file_fn(field_id))

    self.addComment("time", lambda state: state.t)
    self.addComment("stepsize", lambda state: state.h)
    self.addComment("step", lambda state: state.step)

  def store(self, id, path, field, comments):
    writeOMF(path, field, ["%s = %s" % (key, val) for key, val in comments])