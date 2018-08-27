""" Helper to generate a lua configuration for parameter sweeps.

"""

from __future__ import absolute_import

from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS
flags.DEFINE_string('sweep_file', None, 'parameter sweel file')
flags.DEFINE_string('cfg_base', None, 'Configuration basefile')


def load_sweep_file(filename):
  with open(filename, 'rb') as f:
    for line in f:
      items = line.split(' ')
      if len(items) > 1:
        yield items


def load_base_config_file(filename):
  """ Loads file into list of lines, removing the "return options" line.
  """
  with open(filename, 'r') as cfg_file:
    return [l for l in cfg_file.readlines() if not 'return options' in l]


def write_config_file(base, swept_cfgs, output_file):
  """ Writes a lua configuration file.

  First writes the base configuration lines and then the parameter overrides
  specified in the swept_cfgs dictionary, which maps parameter names to
  parameter values.
  """
  with open(output_file, 'wt') as out:
    out.writelines(base)
    for param, value in swept_cfgs.iteritems():
      out.write('{} = {}\n'.format(param, value))
    out.write('return options\n')


class ParameterSweep:
  """ Represents a sweep for a single parameter.
  """

  def __init__(self, parameter_with_values):
    self._param_name = parameter_with_values[0].strip()
    self._values = [v.strip() for v in parameter_with_values[1:]]

  def parameter_dimension(self):
    return len(self._values)

  def parameter_name(self):
    return self._param_name

  def value_for_index(self, index):
    return self._values[index]


def sweep_parameters(sweep_file_name):
  """ Sweeps through all parameter combinations.

  Yields a dictionary with <parameter_name : current_value> items in each
  iteration.
  """
  parameter_sweep = [
      ParameterSweep(x) for x in load_sweep_file(sweep_file_name)
  ]
  current_index = [0 for _ in parameter_sweep]

  while current_index[0] < parameter_sweep[0].parameter_dimension():
    config_instance = dict()
    for i, p in enumerate(parameter_sweep):
      config_instance[p.parameter_name()] = p.value_for_index(current_index[i])
    yield config_instance

    increment_next = True
    idx = len(parameter_sweep) - 1
    while increment_next and idx >= 0:
      current_index[idx] += 1
      if current_index[idx] >= parameter_sweep[idx].parameter_dimension():
        if idx != 0:
          current_index[idx] = 0
        increment_next = True
      else:
        increment_next = False
      idx -= 1


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  if FLAGS.sweep_file:
    for parameter_dict in generate_configurations(FLAGS.sweep_file):
      logging.info('Current sweep')
      for k, v in parameter_dict.iteritems():
        logging.info('%s   -->   %s', k, v)
  if FLAGS.cfg_base:
    for r in load_base_config_file(FLAGS.cfg_base):
      logging.info(r)


if __name__ == '__main__':
  app.run(main)
