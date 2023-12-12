# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    headeryfactor.py                                   :+:    :+:             #
#                                                      +:+                     #
#    By: kwchu <kwchu@student.codam.nl>               +#+                      #
#                                                    +#+                       #
#    Created: 2023/12/12 17:22:54 by kwchu         #+#    #+#                  #
#    Updated: 2023/12/12 17:23:16 by kwchu         ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

from math import ceil
import re, sys

def get_current_indent(function):
	for i, char in enumerate(function):
		if char == "\t":
			break
		current_indent = i
	current_indent += 4 - current_indent % 4
	return (current_indent)

def format_function_indents(functions):
	offset = 0
	for i, function in enumerate(functions):
		current_indent = get_current_indent(function[0])
		if current_indent < max_indent:
			for j, char in enumerate(function[0]):
				if char == "\t":
					offset = j + 1
					break
			indent_diff = ceil((max_indent - current_indent) / 4)
			functions[i][0] = function[0][:offset] + "\t"*indent_diff + function[0][offset:]

def compare_function_name(line, name):
	match = re.fullmatch(r"^(\w+\t+\**(\w+)\(.*\));\n$", line)
	if not match:
		return False
	if name == match[2]:
		return True
	return False

def find_max_indent(functions):
	max_indent = 0
	for function in functions:
		current_indent = get_current_indent(function[0])
		max_indent = max(max_indent, current_indent)
	return max_indent

def get_function_prototypes(files):
	for i, file in enumerate(files):
		with open("src/" + files[i]) as file:
			lines = file.read()
		temp = re.findall(r"^(\w+\t+\**(\w+)\(.*\))$", lines, re.MULTILINE)
		functions.append(list(map(list, temp)))

def update_function_prototypes(lines, functions):
	for i, line in enumerate(lines):
		for j, function in enumerate(functions):
			if compare_function_name(line, functions[j][1]) == True:
				lines[i] = functions[j][0] + ";\n"
				functions.pop(j)
	last_endif = 0
	for i, line in enumerate(lines):
		if line.startswith("#endif"):
			last_endif = i
	lines = lines[:last_endif - 1] + [function[0] + ";\n" for function in functions] + lines[last_endif - 1:]

files = sys.argv[1:]
functions = get_function_prototypes(files[:-1])
max_indent = find_max_indent(functions)
format_function_indents(functions)
with open("include/" + files[1], "r") as file:
	lines = file.readlines()
update_function_prototypes(lines, functions)
with open("include/" + files[1], "w+") as file:
	file.writelines(lines)
