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
  sources = ['/'.join(x.split('/')[:-1]) for x in fold.namelist()]
  for source in sources:
    student_dir = '/'.join(f.split("/")[:2])
    files = os.listdir(source)
    for f in files:
      if os.path.exists(f):
        shutil.move(f, student_dir)

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
