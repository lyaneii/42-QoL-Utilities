import sys, os

def exit_display(CODE):
	if CODE == 1:
		print("Usage: python3 " + sys.argv[0] + " <path>\n")
		print("Use 'info' for more details.")
	elif CODE == 2:
		print("Usage: python3 " + sys.argv[0] + " <directory>\n")
		print("This script automatically looks for any directory starting named 'src' or 'srcs'")
		print("and updates the Makefile according to the new and/or deleted source files.\n")
	elif CODE == 3:
		print("Error: Path does not exist.")
	elif CODE == 4:
		print("Error: Source directory exists but does not contain any source files.")
	elif CODE == 5:
		print("Error: No source files found.")
	elif CODE == 6:
		print("Error: no source file declaration line in Makefile.")
	elif CODE == 7:
		print("Error: Makefile not found.")
	sys.exit(0)

def get_path():
	if len(sys.argv) < 2:
		exit_display(1)
	elif sys.argv[1] == "info":
		exit_display(2)
	elif os.path.exists(os.path.join(os.getcwd(), sys.argv[1])):
		path = os.path.join(os.getcwd(), sys.argv[1])
	else:
		exit_display(3)
	return (path)

def valid_src_dir(path):
	for directory in os.listdir(path):
		if directory == "src" or directory == "srcs":
			if any(file.endswith(".c") for file in (os.listdir(os.path.join(path, directory)))):
				return (True, directory)
			else:
				exit_display(4)
	return (False, 0)

def get_cfiles():
	valid, directory = valid_src_dir(path)
	if valid:
		files = os.listdir(os.path.join(path, directory))
	else:
		files = os.listdir(path)
	cfiles = []
	for file in files:
		if file.endswith(".c"):
			cfiles.append(file)
	if not cfiles:
		exit_display(5)
	cfiles.sort()
	return (cfiles)

def find_src_index(lines):
	for i, line in enumerate(lines):
		if line.startswith("SRC"):
			return (i)
	exit_display(6)

def replace_src_line(lines, cfiles, offset):
	lines[offset] = "SRC = "
	cfile_size = len(cfiles) - 1
	for i in range(len(cfiles)):
		lines[offset] += cfiles[i]
		if i == cfile_size:
			lines[offset] += "\n"
		else:
			lines[offset] += " "

def	update_sources(cfiles):
	if not os.path.exists(os.path.join(path, "Makefile")):
		exit_display(7)
	with open(os.path.join(path, "Makefile"), "r") as file:
		lines = file.readlines()
	offset = find_src_index(lines)
	replace_src_line(lines, cfiles, offset)
	with open(os.path.join(path, "Makefile"), "w+") as file:
		file.writelines(lines)

path = get_path()
cfiles = get_cfiles()
update_sources(cfiles)