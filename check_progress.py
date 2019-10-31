import os, shutil, sys

def check_progress():
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	count = 0
	total = len(folders)

	for folder in folders:
		output_folder = 'outputs/' + folder + '/phyloscanner_output_100_bootstrap/favites_hostRelationshipSummary.csv'
		# RAxML_bestTree = data_dir + folder + '/RAxML_output/RAxML_bestTree.favites'
		if os.path.exists(output_folder):
			count += 1
		else:
			print(folder)

	print('Progress:', count, 'out of', total)


def main():
	check_progress()


if __name__ == "__main__": main()