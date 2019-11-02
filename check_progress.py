import os, shutil, sys

def check_progress():
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	count = 0
	total = len(folders)

	for folder in folders:
		check_folder = 'outputs/' + folder + '/phyloscanner_output_50_bootstrap'
		# RAxML_bestTree = data_dir + folder + '/RAxML_output/RAxML_bestTree.favites'
		# check_folder = 'outputs/' + folder + '/tnet_best_tree/bestTree.100.tnet_new'
		# check_folder = data_dir + folder + '/RAxML_output/'
		if os.path.exists(check_folder):
			# file_list = next(os.walk(check_folder))[2]
			check_file = 'outputs/' + folder + '/phyloscanner_output_50_bootstrap/favites_hostRelationshipSummary.csv'
			count += 1
			if not os.path.exists(check_file):
				print(folder)
				# shutil.remove(check_folder)
			# count += len(file_list)
		# else:
		# 	print(folder)

	print('Progress:', count, 'out of', total)


def main():
	check_progress()


if __name__ == "__main__": main()