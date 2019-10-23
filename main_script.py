#!/usr/bin/python3

# Library Imports
from Bio import SeqIO
import os, shutil, sys
import threading

def get_sequences_and_network():
	favites_data_main = '/home/saurav/research/Favites_data_from_sam/'
	datasets = next(os.walk(favites_data_main))[1]
	# print(datasets)

	for dataset in datasets:
		cur_dir = favites_data_main + dataset
		folders = next(os.walk(cur_dir))[1]
		# print(folders)

		for folder in folders:
			fasta_file = cur_dir+ '/' +folder+ '/FAVITES_output/error_free_files/sequence_data.fasta'
			net_file = cur_dir+ '/' +folder+ '/FAVITES_output/error_free_files/transmission_network.txt'
			new_dir = 'dataset/' +folder
			if not os.path.exists(new_dir):
				os.mkdir(new_dir)
			fasta_copy = new_dir+ '/sequence_data.fasta'
			net_copy = new_dir+ '/transmission_network.txt'
			if os.path.exists(fasta_file):
				shutil.copy(fasta_file, fasta_copy)
			if os.path.exists(net_file):
				shutil.copy(net_file, net_copy)
			# print(os.path.exists(fasta_file))

def rename_and_clean_sequences():
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	# print(folders)
	for folder in folders:
		print(folder)
		favites_fasta = data_dir + folder +'/sequence_data.fasta'
		records = list(SeqIO.parse(favites_fasta, 'fasta'))
		for record in records:
			parts = record.id.split('|')
			record.id = parts[1] + '_' + parts[0]

		SeqIO.write(records, data_dir + folder +'/sequences.fasta', 'fasta')
		os.remove(favites_fasta)

def run_script(folder, script):
	cmd = './' + folder +'/'+ script
	print(cmd)
	# os.system(cmd)

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


def main():
	# get_sequences_and_network()
	# rename_and_clean_sequences()
	create_raxml_scripts_with_bootstrap(100, 'raxml_scripts')
	# run_raxml_scripts_with_threading('raxml_scripts')
	



if __name__ == "__main__": main()