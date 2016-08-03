import subprocess
import csv

process = subprocess.Popen(['dumpcap', '-D'], stdout=subprocess.PIPE)
stdout, stderr = process.communicate()

reader = csv.DictReader(stdout.decode('ascii').splitlines(),
                        delimiter=' ', skipinitialspace=True,
                        fieldnames=['id', 'interface'])

for row in reader:
    row['id'] = row['id'][:-1]
    print row
