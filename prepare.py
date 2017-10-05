# author: andre cianflone
# usage:
#$ python prepare.py archive.zip
import os, zipfile, shutil
fold = zipfile.ZipFile('archive.zip')

# Extract
fold.extractall()

# Extract assignments and delete archive
print('extracting assignments and moving to student folders')
for f in fold.namelist():
  student_dir = '/'.join(f.split("/")[:2])
  if f.endswith('.zip'):
    assignment = zipfile.ZipFile(f)
    assignment.extractall(student_dir)
    os.remove(f)
  if f.endswith('.7z'):
    os.system( '7z x ' + f + ' -o' + student_dir)
    os.remove(f)

# Move up to student dir
for f in fold.namelist():
  if 'c_henneb' in f:
    a=1
  student_dir = '/'.join(f.split("/")[:2])
  source = '/'.join(f.split("/")[:-1])
  files = os.listdir(source)
  for fi in files:
    path = source + "/" + fi
    if os.path.exists(path):
      shutil.move(os.path.join(source, fi), os.path.join(student_dir, fi))

# Remove useless dirs
print('cleaning up directories')
for f in fold.namelist():
  useless = '/'.join(f.split("/")[:3])
  if os.path.exists(useless):
    shutil.rmtree(useless)

# Student ID file
id_file = fold.namelist()[0].split("/")[0] + '/' + 'students.txt'
with open(id_file, 'w') as f:
  for student in [x.split("/")[1] for x in fold.namelist()]:
    f.write(student+'\n')

print('created student id file: ', id_file)
