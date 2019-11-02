import os, shutil, sys

def check_progress():
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	count = 0
	total = len(folders)

	for folder in folders:
		# check_folder = 'outputs/' + folder + '/phyloscanner_output_100_bootstrap/'
		check_folder = data_dir + folder + '/RAxML_output/'
		if os.path.exists(check_folder):
			file_list = next(os.walk(check_folder))[2]
			count += len(file_list)
		# else:
		# 	print(folder)

	print('Progress:', count, 'out of', total*7)


def main():
	check_progress()


if __name__ == "__main__": main()