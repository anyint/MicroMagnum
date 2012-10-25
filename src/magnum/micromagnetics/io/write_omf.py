import magnum.magneto as magneto
from magnum.logger import logger

from .io_tools import try_io_operation

OMF_FORMAT_ASCII = magneto.OMF_FORMAT_ASCII
OMF_FORMAT_BINARY_4 = magneto.OMF_FORMAT_BINARY_4
OMF_FORMAT_BINARY_8 = magneto.OMF_FORMAT_BINARY_8

def writeOMF_helper(path, vector_field, desc=[], format = OMF_FORMAT_ASCII):
  mesh = vector_field.mesh
  header = magneto.OMFHeader()
  header.Title = ""
  header.Desc.clear()
  for d in desc: header.Desc.push_back(str(d))
  header.meshunit = "m"
  header.valueunit = vector_field.value_unit or "(none)"
  header.valuemultiplier = 1.0 # this is overwritten by magneto.writeOMF
  header.xmin = 0.0
  header.ymin = 0.0
  header.zmin = 0.0
  header.xmax = mesh.num_nodes[0] * mesh.delta[0]
  header.ymax = mesh.num_nodes[1] * mesh.delta[1]
  header.zmax = mesh.num_nodes[2] * mesh.delta[2]
  header.ValueRangeMaxMag = 0
  header.ValueRangeMinMag = 0
  header.meshtype = "rectangular"
  header.xbase = mesh.delta[0] / 2.0
  header.ybase = mesh.delta[1] / 2.0
  header.zbase = mesh.delta[2] / 2.0
  header.xstepsize = mesh.delta[0]
  header.ystepsize = mesh.delta[1]
  header.zstepsize = mesh.delta[2]
  header.xnodes = mesh.num_nodes[0]
  header.ynodes = mesh.num_nodes[1]
  header.znodes = mesh.num_nodes[2]
  magneto.writeOMF(path, header, vector_field, format)
  logger.debug("Wrote file %s", path)

def writeOMF(path, vector_field, desc=[], format = OMF_FORMAT_ASCII):
  try_io_operation(lambda: writeOMF_helper(path, vector_field, desc, format))