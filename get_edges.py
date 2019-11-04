def get_real_edges(real_file):
	real_edges = []
	f = open(real_file)
	f.readline()
	for line in f.readlines():
		parts = line.split('\t')
		if not parts[0] == parts[1]:
			real_edges.append(parts[0]+'->'+parts[1])

	f.close()
	return real_edges


def get_phyloscanner_single_tree_edges(phylo_file):
	phyloscanner_edges = []
	f = open(phylo_file)
	f.readline()
	for line in f.readlines():
		parts = line.rstrip().split(',')
		if parts[2].isdigit() and parts[3].isdigit():
			phyloscanner_edges.append(parts[3]+'->'+parts[2])
		# print(parts)

	f.close()
	return phyloscanner_edges

def get_phyloscanner_summary_trans_edges(phylo_file, cutoff):
	phyloscanner_edges = []
	f = open(phylo_file)
	f.readline()
	for line in f.readlines():
		parts = line.rstrip().split(',')
		# print(parts)
		if parts[2] == 'trans' and int(parts[3]) >= cutoff:
			phyloscanner_edges.append(parts[0]+'->'+parts[1])
		# print(parts)

	f.close()
	return phyloscanner_edges


def get_phyloscanner_multi_tree_edges_with_complex(phylo_file, cutoff):
	phyloscanner_edges = []
	edge_dict = {}
	f = open(phylo_file)
	f.readline()
	for line in f.readlines():
		parts = line.rstrip().split(',')
		if parts[2] == 'trans':
			edge = parts[0]+'->'+parts[1]
			edge_dict[edge] = int(parts[3])

	for line in f.readlines():
		parts = line.rstrip().split(',')
		if parts[2] == 'complex':
			edge = parts[0]+'->'+parts[1]
			rev_edge = parts[1]+'->'+parts[0]
			if edge in edge_dict:
				edge_dict[edge] += int(parts[3])
			elif rev_edge in edge_dict:
				edge_dict[rev_edge] += int(parts[3])

	f.close()
	for x, y in edge_dict.items():
		if y >= cutoff: phyloscanner_edges.append(x)

	return phyloscanner_edges


def get_tnet_single_tree_edges(tnet_file):
	tnet_edges = []
	f = open(tnet_file)
	f.readline()
	for line in f.readlines():
		parts = line.rstrip().split('\t')
		tnet_edges.append(parts[0]+'->'+parts[1])

	f.close()
	return tnet_edges


def get_mul_tnet_edges(tnet_file, cutoff):
	tnet_edges = []
	f = open(tnet_file)
	for line in f.readlines():
		parts = line.rstrip().split('\t')
		if int(parts[1]) >= cutoff:
			tnet_edges.append(parts[0])
		# print('M',parts)

	f.close()
	return tnet_edges


def get_tnet_summary_edges(tnet_file, cutoff):
	tnet_edges = []
	f = open(tnet_file)
	for line in f.readlines():
		parts = line.rstrip().split(',')
		if int(parts[1]) >= cutoff:
			tnet_edges.append(parts[0])

	f.close()
	return tnet_edges
