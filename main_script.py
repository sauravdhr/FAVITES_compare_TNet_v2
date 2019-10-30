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

def multithreadings(input_file, output_dir, bootstrap):
	cmd = 'raxmlHPC -f a -m GTRGAMMA -p 12345 -x 12345 -s {} -w {} -N {} -n favites -k'.format(input_file, output_dir, bootstrap)
	# print(cmd)
	os.system(cmd)

def run_raxml_with_threading(bootstrap):
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	t = []

	for folder in folders:
		RAxML_folder = os.path.abspath(data_dir + folder + '/RAxML_output')
		fasta_file = os.path.abspath(data_dir + folder + '/sequences.fasta')
		RAxML_info = RAxML_folder + '/RAxML_info.favites'
		if not os.path.exists(RAxML_folder):
			os.mkdir(RAxML_folder)
		if os.path.exists(RAxML_info):
			continue

		t.append(threading.Thread(target=multithreadings, args=(fasta_file, RAxML_folder, bootstrap)))

	# print('len', len(t))
	for i in range(len(t)):
		t[i].start()

	for i in range(len(t)):
		t[i].join()

def create_bootstrap_trees():
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]

	for folder in folders:
		print('Inside',folder)
		bootstrap_file = data_dir + folder + '/RAxML_output/RAxML_bootstrap.favites'
		bootstrap_folder = data_dir + folder + '/RAxML_output/bootstrap_trees'
		if not os.path.exists(bootstrap_file):
			continue
		if not os.path.exists(bootstrap_folder):
			os.mkdir(bootstrap_folder)

		f = open(bootstrap_file)
		tree_list = f.readlines()

		for i in range(len(tree_list)):
			file = open(bootstrap_folder + '/' + str(i) + '.bootstrap.tree', 'w')
			file.write(tree_list[i])

		# break

def root_bootstrap_trees():
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]

	for folder in folders:
		bootstrap_folder = data_dir + folder + '/RAxML_output/bootstrap_trees'
		rooted_bootstrap_folder = data_dir + folder + '/rooted_bootstrap_trees'
		bootstrap_trees = next(os.walk(bootstrap_folder))[2]
		output_folder = os.path.abspath(rooted_bootstrap_folder)
		if not os.path.exists(output_folder):
			os.mkdir(output_folder)

		for tree in bootstrap_trees:
			input_tree = bootstrap_folder + '/' + tree
			i = int(tree.split('.')[0])
			cmd = 'raxmlHPC -f I -m GTRGAMMA -t {} -n {} -w {}'.format(input_tree, str(i), output_folder)
			# print(cmd)
			os.system(cmd)
			try:
				os.remove(output_folder + '/RAxML_info.' + str(i))
			except:
				print('RAxML_info does not exist')
		# break

def create_phyloscanner_input():
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]

	for folder in folders:
		print('Inside',folder)
		input_folder = data_dir + folder + '/rooted_bootstrap_trees'
		output_folder = data_dir + folder + '/phyloscanner_input'
		tree_list = next(os.walk(input_folder))[2]
		if not os.path.exists(output_folder):
			os.mkdir(output_folder)

		for tree in tree_list:
			i = int(tree.rstrip().split('.')[1])
			rooted_tree = input_folder + '/' + tree
			rename_tree = output_folder + '/bootstrap.InWindow_'+ str(1000+i*100) +'_to_'+ str(1099+i*100) +'.tree'
			shutil.copy(rooted_tree, rename_tree)

def run_phyloscanner(bootstrap = 0):
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]

	for folder in folders:
		print('Inside',folder)
		input_folder = data_dir + folder + '/phyloscanner_input'
		if bootstrap == 0:
			output_folder = 'outputs/' + folder + '/phyloscanner_output_100_bootstrap'
			input_file = input_folder + '/bootstrap.InWindow_'
		else:
			output_folder = 'outputs/' + folder + '/phyloscanner_output_' + str(bootstrap) + '_bootstrap'
			input_file = input_folder + '/bootstrap.InWindow_'
			print('Complete the input_file code')

		if not os.path.exists(output_folder):
			os.mkdir(output_folder)

		cmd = 'PhyloScanner/phyloscanner_analyse_trees_old.R {} favites -ct -od {} s,0 --overwrite --tipRegex="^(.*)_(.*)$"'.format(input_file, output_folder)
		# print(cmd)
		os.system(cmd)

		# break

def check_and_clean():
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	count = 0

	for folder in folders:
		print('Inside',folder)
		check_folder = data_dir + folder + '/phyloscanner_input'
		trees = next(os.walk(check_folder))[2]
		count += len(trees)
		print(count)
		# os.mkdir('outputs/' + folder)
		output_folder = 'outputs/' + folder + '/phyloscanner_output_100_bootstrap'
		if os.path.exists(output_folder):
			os.rmdir(output_folder)

def main():
	# get_sequences_and_network()
	# rename_and_clean_sequences()
	# run_raxml_with_threading(100)
	# create_bootstrap_trees()
	# root_bootstrap_trees()
	# create_phyloscanner_input()
	run_phyloscanner()
	# check_and_clean()




if __name__ == "__main__": main()