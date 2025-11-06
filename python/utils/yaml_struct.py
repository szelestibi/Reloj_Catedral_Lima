import os

def dir_to_yaml(path, indent=0):
  lines = []
  for name in sorted(os.listdir(path)):
    fullpath = os.path.join(path, name)
    prefix = '  ' * indent + f"- {name}"
    lines.append(prefix)
    if os.path.isdir(fullpath):
      lines.extend(dir_to_yaml(fullpath, indent + 1))
  return lines

start_dir = './'

with open('./yaml_struct.yaml', 'w', encoding='utf-8') as f:
 f.write('\n'.join(dir_to_yaml(start_dir)))
