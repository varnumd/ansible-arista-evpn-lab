#
# Simple list append filter
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from jinja2 import TemplateError

class FilterModule(object):


#
# Figure out network device OS type based on "show version" printout
#
  def lldp_list(self,show_lldp):
  	nei_list = []
  	for nei in show_lldp:
  		nei_list.append(nei['neighborDevice'])
  	return nei_list 

  def filters(self):
    return {
      'lldp_list': self.lldp_list
    }
