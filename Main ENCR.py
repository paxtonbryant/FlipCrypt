import os, re, sys

os.makedirs('../../Downloads/flipped2', exist_ok=True)
outfilename = "flipped2" +"/" + sys.argv[1] + ".flipped2"
outfile = open(outfilename, 'w', encoding='latin-1', newline='\r\n')
sys.stdout = outfile

with open(sys.argv[1],'r',encoding='latin-1') as file:
	lines = file.readlines()
	GenEncryptFlag = False
	for index, line in enumerate(lines):
		line=line.rstrip()

# Here, we are looking for Name fields that have _ENCRYPT at the end. If we do,
# then we get ready to add genEncryption() if there are Derivation fields in this
# section.
# We only care about Derivation records when the target field is encrypted.
# So if we hit the end of the DSSUBRECORD after we have found the Name record, it's time
# to reset and ignore

#Handles case where encrypt colummn is titled "ENCR"
		if re.search("Name \"[A-Za-z_].*_ENCR\"", line):
			GenEncryptFlag = True
			DerivationFlag = False

# If we are on a field that has genDecryption on it, we need to remove that function
# (genDecryption()), and also change the other function references
# from genDecryption to genEncryption
		swapstuff = re.search('genDecryption', line)
		if swapstuff:
			x = re.search('genDecryption\(([^\)]+)\)', line)
			if x:
				myline=re.sub('genDecryption\(([^\)]+)\)', r'\1', line)
				print(myline)

			y = re.search("Transform \"genDecryption\"", line)
			if y:
				doNothing=0

			a = re.search("      Identifier \"genDecryption\"", line)
			if a:
				print("      Identifier \"genEncryption\"")
			b = re.search("      Catalog \"DSU\.genDecryption\"", line)
			if b:
				print("      Catalog \"DSU.genEncryption\"")
			c = re.search("      Identifier \"DSU\.genDecryption\"", line)
			if c:
				print("      Identifier \"DSU.genEncryption\"")

# So now, we are looking the Derivation fields and the ParsedDerivation fields, so that
# we can add the genEncryption() function to them...but only if this part of the record
# is tagged as being an _ENCRYPTED field from the first section
# They both need the same changes, so all we have to search for is the Derivation,
# and we'll apply the change to both.
# When we are adding the genEncryption() function, we also have to add a line for
# Transform, but that is always the same, and it is added before the SortKey line.
		elif GenEncryptFlag:
			gen = re.search("(Derivation \")([A-Za-z_\(\).].*)\"", line)
			if gen:
				DerivationFlag = True
				enc = re.sub("(Derivation \")([A-Za-z_\(\).].*)\"", r'\1genEncryption(\2)"', line)
				print (enc)
			else:
				d = re.search('SortKey', line)
				if d and DerivationFlag:
					print("         Transform \"genEncryption\"")
				print (line)

# If we are not removing genDecryption, or adding genEncryption, then all we have to do
# is pass the line through
		else:
			print(line)

file.close()
outfile.close()