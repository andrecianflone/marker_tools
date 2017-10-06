# author: andre cianflone
# usage:
# python prepare.py archive.zip a1

import os, zipfile, shutil, sys
archive = sys.argv[1]
dest = sys.argv[2]

# Setup root dir
if os.path.exists(dest):
  shutil.rmtree(dest)
os.makedirs(dest)

# Keep list of (id, user_name)
users = []

# Extract original archive
print('extracting assignments')
with zipfile.ZipFile(archive) as zip_f:
  # Get unique user dirs
  temp = []
  for path in zip_f.namelist():
    temp.append(path.split("/")[1])
  temp = set(temp)
  for user in temp:
    # build list of (id, user_name)
    users.append(user.split("-"))

  # Go through items in zip
  for item in zip_f.namelist():
    filename = os.path.basename(item)
    # skip directories
    if not filename:
      continue

    # Prepare student dir
    student_dir = item.split("/")[1].split("-")[1]
    student_dir = os.path.join(dest, student_dir)
    if not os.path.exists(student_dir):
      os.makedirs(student_dir)

    # Copy file
    source = zip_f.open(item)
    with open(os.path.join(student_dir, filename), "wb") as target:
      with source, target:
        shutil.copyfileobj(source, target)

# Extract individual student archives
for st_dir in os.listdir(dest):
  st_dir = os.path.join(dest,st_dir)
  for fi in os.listdir(st_dir):
    fi_path = os.path.join(st_dir, fi)
    if fi.endswith('.zip'):
      assignment = zipfile.ZipFile(fi_path)
      assignment.extractall(st_dir)
      os.remove(fi_path)
    if fi.endswith('.7z'):
      os.system( '7z x ' + fi_path + ' -o' + st_dir)
      os.remove(fi_path)

# Student ID file
id_file = os.path.join(dest, 'students.csv')
with open(id_file, 'w') as f:
  for st_id, user_name in users:
    f.write(user_name + ',' + st_id + '\n')
print('created student id file: ', id_file)


