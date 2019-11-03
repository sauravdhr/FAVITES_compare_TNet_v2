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
	F1_file = open('results/best_tree.prec.rec.f1.tnet.csv', 'w+')
	F1_file.write('dataset,prec_50,rec_50,f1_50,prec_60,rec_60,f1_60,prec_70,rec_70,f1_70,prec_80,rec_80,f1_80,prec_90,rec_90,f1_90,prec_100,rec_100,f1_100\n')

	for folder in folders:
		print('inside folder: ',folder)

		F1 = []
		for th in thresholds:
			real = set(ge.get_real_edges('dataset/' + folder + '/transmission_network.txt'))
			tnet = set(ge.get_mul_tnet_edges(data_dir + folder + '/tnet_best_tree/bestTree.100.tnet_new', th))

			temp = get_prec_rec_f1(real, tnet)
			F1.extend(temp)

		F1_file.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(folder,F1[0],F1[1],F1[2],F1[3],F1[4],F1[5]
						,F1[6],F1[7],F1[8],F1[9],F1[10],F1[11],F1[12],F1[13],F1[14],F1[15],F1[16],F1[17]))

def main():
	compare_tnet_best_tree()

	



if __name__ == "__main__": main()