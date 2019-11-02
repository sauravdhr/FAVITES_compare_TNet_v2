#!/usr/bin/python3

# Library Imports
from Bio import SeqIO
import os, shutil, sys
import threading

def run_script(folder, script):
	cmd = './' + folder +'/'+ script
	print(cmd)
	os.system(cmd)

def run_raxml_scripts_with_threading(folder):
	t=[]
	scripts = next(os.walk(folder))[2]
	for script in scripts:
		t.append(threading.Thread(target=run_script, args=(folder, script)))

	for i in range(len(t)):
		t[i].start()

	for i in range(len(t)):
		t[i].join()

def create_raxml_scripts_with_bootstrap(bootstrap, script_folder):
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	cmd_list = []

	for folder in folders:
		RAxML_folder = os.path.abspath(data_dir + folder + '/RAxML_output')
		fasta_file = os.path.abspath(data_dir + folder + '/sequences.fasta')
		if not os.path.exists(RAxML_folder):
			os.mkdir(RAxML_folder)

		cmd = 'raxmlHPC -f a -m GTRGAMMA -p 12345 -x 12345 -s {} -w {} -N {} -n favites -k'.format(fasta_file, RAxML_folder, bootstrap)
		# print(cmd)
		cmd_list.append(cmd)

	print(len(cmd_list))
	if not os.path.exists(script_folder):
		os.mkdir(script_folder)

	for i in range(len(cmd_list)):
		script = open(script_folder + '/' + str(i%60) + '.raxml_cmd.sh', 'a+')
		script.write(cmd_list[i] + '\n')
		script.close()


def multithreadings(input_file, output_dir, bootstrap):
	cmd = 'raxmlHPC -f a -m GTRGAMMA -p 12345 -x 12345 -s {} -w {} -N {} -n favites -k'.format(input_file, output_dir, bootstrap)
	# print(cmd)
	os.system(cmd)


def run_raxml_without_scripts_threading(bootstrap):
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	t = []

	for folder in folders:
		RAxML_folder = os.path.abspath(data_dir + folder + '/RAxML_output')
		fasta_file = os.path.abspath(data_dir + folder + '/sequences.fasta')
		RAxML_info = RAxML_folder + '/RAxML_info.favites'
		if os.path.exists(RAxML_info):
			continue

		t.append(threading.Thread(target=multithreadings, args=(fasta_file, RAxML_folder, bootstrap)))

	# print('len', len(t))
	for i in range(len(t)):
		t[i].start()

	for i in range(len(t)):
		t[i].join()

def root_raxml_best_tree():
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]

	for folder in folders:
		print('Inside :', folder)
		best_tree = data_dir + folder + '/RAxML_output/RAxML_bestTree.favites'
		output_folder = os.path.abspath(data_dir + folder + '/RAxML_output')
		cmd = 'raxmlHPC -f I -m GTRGAMMA -t {} -n bestTree.favites -w {}'.format(best_tree, output_folder)
		os.system(cmd)


def main():
	# get_sequences_and_network()
	# rename_and_clean_sequences()
	# create_raxml_scripts_with_bootstrap(100, 'raxml_scripts')
	# run_raxml_scripts_with_threading('raxml_scripts')
	root_raxml_best_tree()
	



if __name__ == "__main__": main()