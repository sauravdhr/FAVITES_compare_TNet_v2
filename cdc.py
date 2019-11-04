# This scripts compares Tnet and Phyloscanner on CDC detaset.
# Each outbreak is handeled separately in this script.
# We know the source of only 10 out of these outbreaks.

# Library Imports
import operator
import shutil, os
import main_script as ms

# Global Variables
known_outbreaks = ['AA', 'AC', 'AI', 'AJ', 'AQ', 'AW', 'BA', 'BB', 'BC', 'BJ']
sources = ['AA45','AC124','AI4','AJ199','AQ89','AW2','BA3','BB45','BC46','BJ28']


def run_new_tnet_cdc_multithreaded(times = 100):
	for outbreak in known_outbreaks:
		input_folder = 'CDC/'+outbreak+'/tnet_input'
		output_folder = 'CDC/'+outbreak+'/tnet_new_bootstrap'
		if not os.path.exists(output_folder):
			os.mkdir(output_folder)
			ms.run_tnet_new_single_folder(input_folder, output_folder, times)

def create_cdc_tnet_summary(th=50):
	for outbreak in known_outbreaks:
		input_folder = 'CDC/'+outbreak+'/tnet_output'
		output_folder = 'CDC/'+outbreak
		edge_dict = {}
		result = open(output_folder+'/tnet.summary.'+ str(th), 'w+')

		tnet_list = next(os.walk(input_folder))[2]
		for tnet in tnet_list:
			input_file = input_folder+'/'+ tnet
			f = open(input_file)
			for line in f.readlines():
				parts = line.rstrip().split('\t')
				edge = parts[0]
				# print(parts)
				if int(parts[1]) < th: continue
				if edge in edge_dict:
					edge_dict[edge] += 1
				else:
					edge_dict[edge] = 1

			f.close()

		edge_dict = dict(sorted(edge_dict.items(), key=operator.itemgetter(1),reverse=True))

		for x, y in edge_dict.items():
			result.write('{}\t{}\n'.format(x, y))

		result.close()

def create_cdc_tnet_summary_undirected(th=50):
	for outbreak in known_outbreaks:
		input_folder = 'CDC/'+outbreak+'/tnet_output_undirected'
		output_folder = 'CDC/'+outbreak
		edge_dict = {}
		result = open(output_folder+'/tnet.summary.undirected.'+ str(th), 'w+')

		tnet_list = next(os.walk(input_folder))[2]
		for tnet in tnet_list:
			input_file = input_folder+'/'+ tnet
			f = open(input_file)
			for line in f.readlines():
				parts = line.rstrip().split('\t')
				edge = parts[0]
				# print(parts)
				if int(parts[1]) < th: continue
				if edge in edge_dict:
					edge_dict[edge] += 1
				else:
					edge_dict[edge] = 1

			f.close()

		edge_dict = dict(sorted(edge_dict.items(), key=operator.itemgetter(1),reverse=True))

		for x, y in edge_dict.items():
			result.write('{}\t{}\n'.format(x, y))

		result.close()

def main():
	run_new_tnet_cdc_multithreaded()
	# create_cdc_tnet_summary(80)
	# create_cdc_tnet_summary_undirected(80)


if __name__ == "__main__": main()
