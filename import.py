import csv
import MySQLdb as mdb
import decimal
import datetime
import time
import os

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.   
# test
def importFileinDB(fileName,IDSonda):

	try:
		con = mdb.connect(host='localhost', user='root',  passwd='pentagon51$', db='TRENDS')
		cursor = con.cursor()
		print "Importazione dati da file: " + fileName + " sonda numero: " + IDSonda
		csv_data = csv.reader(file(fileName),delimiter=';')
		next(csv_data)   # skip the first line
		for row in csv_data:
			str_data=row[0].strip()
			anno=int(str_data[-4:])
			mese=int(str_data[3:5])
			giorno=int(str_data[:2])
	
			str_ora=row[1].strip()
			secondi=int(str_ora[-2:])
			minuti=int(str_ora[3:5])
			ore=int(str_ora[:2])
		
			datetime_timestamp = datetime.datetime(anno,mese,giorno,ore,minuti,secondi)
	#		print datetime_timestamp
		    	str_valore=row[2].replace(",", ".").strip()
			try:
				decimal_valore= decimal.Decimal(str_valore)
			except decimal.InvalidOperation:
				decimal_valore=0
				#print "Could not convert string to a decimal." 		
			if IDSonda > 0:
				if minuti %15 ==0:
					cursor.execute('INSERT INTO Sonda (IDSonda,VALORE_D,TimeStamp ) VALUES (%s, %s, %s )', 
(IDSonda,decimal_valore,datetime_timestamp))
					con.commit()
	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
	finally:
		if con:
#			cursor.execute('delete from Sonda where minute(timestamp) mod 15 <> 0;')
#			print "Pulizia record <> 15 minuti "
			con.commit()
			cursor.close()
			con.close()

def main():
	full_file_paths = get_filepaths("/datadrive/TRENDS")
	file_path_importati= "/datadrive/IMPORTATI/"
	for file in full_file_paths:

		if file.endswith(".CSV"):
			filename = file[file.rfind('/')+1:]
			filename_no_extension= os.path.splitext(filename)[0]
#			print(filename_no_extension.rfind('_'))
			idsonda = filename_no_extension[filename_no_extension.rfind('_')+1:len(filename_no_extension)]
			#print idsonda
			importFileinDB(file,idsonda)
			os.rename(file, file_path_importati + filename + ".OK")
			
main()
