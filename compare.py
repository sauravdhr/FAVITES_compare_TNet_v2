import shutil, os
import get_edges as ge

def get_prec_rec_f1(real_set, pred_set):
	result = []
	TP = len(real_set & pred_set)
	FP = len(pred_set - real_set)
	FN = len(real_set - pred_set)
	try:
		precision = TP/(TP+FP)
		recall = TP/(TP+FN)
		f1 = 2*(recall * precision) / (recall + precision)
	except ZeroDivisionError:
		precision = 0
		recall = 0
		f1 = 0

	result.append(round(precision,3))
	result.append(round(recall,3))
	result.append(round(f1,3))

	return result


def compare_tnet_best_tree():
	data_dir = 'outputs/'
	folders = next(os.walk(data_dir))[1]
	folders.sort()

	thresholds = [50, 60, 70, 80, 90, 100]
	F1_file = open('results/best_tree.recall.tnet.old.csv', 'w+')
	F1_file.write('dataset,50,60,70,80,90,100\n')

	for folder in folders:
		print('inside folder: ',folder)

		F1 = []
		for th in thresholds:
			real = set(ge.get_real_edges('dataset/' + folder + '/transmission_network.txt'))
			tnet = set(ge.get_mul_tnet_edges(data_dir + folder + '/tnet_best_tree/bestTree.100.tnet_old', th))

			temp = get_prec_rec_f1(real, tnet)
			F1.append(temp[1])

		F1_file.write('{},{},{},{},{},{},{}\n'.format(folder,F1[0],F1[1],F1[2],F1[3],F1[4],F1[5]))
						# ,F1[6],F1[7],F1[8],F1[9],F1[10],F1[11],F1[12],F1[13],F1[14],F1[15],F1[16],F1[17]))


def compare_phyloscanner_tnet(bootstrap, threshold):
	data_dir = 'outputs/'
	folders = next(os.walk(data_dir))[1]
	folders.sort()

	F1_file = open('results/bootstrap.'+str(bootstrap)+'.phyloscanner.tnet.new.th.'+str(threshold)+'.csv', 'w+')
	F1_file.write('dataset,phylo_prec,phylo_rec,phylo_f1,tnet_prec,tnet_rec,tnet_f1\n')

	for folder in folders:
		print('inside folder: ',folder)
		F1 = []

		real = set(ge.get_real_edges('dataset/' + folder + '/transmission_network.txt'))
		phylo = set(ge.get_phyloscanner_summary_trans_edges(data_dir + folder + '/phyloscanner_output_'+str(bootstrap)+'_bootstrap/favites_hostRelationshipSummary.csv', bootstrap//2))
		tnet = set(ge.get_tnet_summary_edges(data_dir + folder + '/tnet_new_bootstrap_summary_directed/tnet_new_'+str(bootstrap)+'_bootstrap_th_'+str(threshold)+'_summary.csv', bootstrap//2))

		F1.extend(get_prec_rec_f1(real, phylo))
		F1.extend(get_prec_rec_f1(real, tnet))
		F1_file.write('{},{},{},{},{},{},{}\n'.format(folder,F1[0],F1[1],F1[2],F1[3],F1[4],F1[5]))

	F1_file.close()

def compare_phyloscanner_tnet_best_tree(threshold):
	data_dir = 'outputs/'
	folders = next(os.walk(data_dir))[1]
	folders.sort()

	F1_file = open('results/best_tree.phyloscanner.tnet.new.th.'+str(threshold)+'.csv', 'w+')
	F1_file.write('dataset,phylo_prec,phylo_rec,phylo_f1,tnet_prec,tnet_rec,tnet_f1\n')

	for folder in folders:
		print('inside folder: ',folder)
		F1 = []

		real = set(ge.get_real_edges('dataset/' + folder + '/transmission_network.txt'))
		phylo = set(ge.get_phyloscanner_single_tree_edges(data_dir + folder + '/phyloscanner_best_tree/favites_collapsedTree.csv'))
		tnet = set(ge.get_mul_tnet_edges(data_dir + folder + '/tnet_best_tree/bestTree.100.tnet_new', threshold))

		F1.extend(get_prec_rec_f1(real, phylo))
		F1.extend(get_prec_rec_f1(real, tnet))
		F1_file.write('{},{},{},{},{},{},{}\n'.format(folder,F1[0],F1[1],F1[2],F1[3],F1[4],F1[5]))

	F1_file.close()

def main():
	# compare_tnet_best_tree()
	# compare_phyloscanner_tnet(10,50)
	compare_phyloscanner_tnet_best_tree(100)

	



if __name__ == "__main__": main()