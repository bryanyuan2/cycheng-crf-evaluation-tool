#
# CRF++ crf_test result confusion matrix
# description: crf_confusion_matrix_class
# author: bryanyuan2
# date: 20130212
#

from __future__ import division
import sys

__author__ = "bryanyuan2"
__email__ = "bryanyuan2@gmail.com"

class crf_confusion_matrix_class:
	
	#
	correct_label_pool = []
	precision_label_pool = []
	recall_label_pool = []
	
	accuracy_of_all_data = 0
	del_synbol_const = "\t"
	#
	full_confusion_matrix_const = []
	full_confusion_matrix = []
	#
	guess_correct = []
	guess_wrong = []

	def __init__(self,correct_label_pool = ["I-NP","B-NP","B-ADJP","I-ADJP"], filename = "./sample/sample_crf_output"):

		self.correct_label_pool = correct_label_pool

		# initialize confusion_matrix
		for i in range(0,len(self.correct_label_pool)*len(self.correct_label_pool)):
			self.full_confusion_matrix.append(0)
			
		# initialize full_confusion_matrix_const
		for i in range(0,len(self.correct_label_pool)):
			self.precision_label_pool.append(0)
			self.recall_label_pool.append(0)
			for j in range(0,len(self.correct_label_pool)):
				self.full_confusion_matrix_const.append(self.correct_label_pool[i] + "_" + self.correct_label_pool[j])

		#print self.precision_label_pool
		#print self.recall_label_pool

		f = open(filename,'r')

		while(1):
			line = f.readline()
			if not line:
				break
			else:
				if (line.replace("\n","")!=""):
					data_raw = line.replace("\n","")
					data = data_raw.split("\t")
					curr_correct_answer = data[len(data)-2]
					curr_guess_label = data[len(data)-1]

					if (curr_guess_label == curr_correct_answer):
						self.guess_correct.append(data_raw)
					else:
						self.guess_wrong.append(data_raw)

					for j in range(0,len(self.full_confusion_matrix_const)):
						if (self.full_confusion_matrix_const[j] == curr_correct_answer + "_" + curr_guess_label):
							self.full_confusion_matrix[j] = self.full_confusion_matrix[j] + 1
	
	# crf_result_correct_and_wrong_file_mapping
	def crf_result_correct_and_wrong_file_mapping(self):
		
		f_guess_correct = open("f_guess_correct", "w")
		for i in range(0,len(self.guess_correct)):
			f_guess_correct.write(str(self.guess_correct[i]) + "\n")
		f_guess_correct.close()

		f_guess_wrong = open("f_guess_wrong", "w")
		for i in range(0,len(self.guess_wrong)):
			f_guess_wrong.write(str(self.guess_wrong[i]) + "\n")
		f_guess_wrong.close()

	# confusion_matrix_print_func
	def confusion_matrix_print_func(self):
		
		#	ary[actual class][predicted class]
		#
		#   table				[predicted class]
		#
		#	[actual class]

		#print full_confusion_matrix

		total_data = 0
		correct_data = 0

		print("====\nConfusion Matrix\n====")
		print(self.del_synbol_const + self.del_synbol_const, end='')
		for i in range (0,len(self.correct_label_pool)):
			print(self.correct_label_pool[i] + self.del_synbol_const, end='')
		print(" [predicted class]")

		#correct_label_pool[i/len(correct_label_pool)]
		for i in range (0,len(self.full_confusion_matrix)):
			if (i%len(self.correct_label_pool)==0):
				print(self.correct_label_pool[int(i/len(self.correct_label_pool))] + str(self.del_synbol_const) + str(self.del_synbol_const), end='')

			# precision_label_pool
			self.precision_label_pool[int(i%len(self.correct_label_pool))] = self.precision_label_pool[i%len(self.correct_label_pool)] + self.full_confusion_matrix[i]
			# recall_label_pool
			self.recall_label_pool[int(i/len(self.correct_label_pool))] = self.recall_label_pool[int(i/len(self.correct_label_pool))] + self.full_confusion_matrix[i]
			# total_correct_data
			total_data = total_data + self.full_confusion_matrix[i]
			
			print(str(self.full_confusion_matrix[i]) + self.del_synbol_const, end='')
			if ((i+1)%len(self.correct_label_pool)==0):
				print("")
		print("[actual class]")
		
		print("\n====\n(Precision, Recall, F1 score)\n====")
		for i in range(0,len(self.precision_label_pool)):
			#print self.precision_label_pool[i] 
			curr_id = i*(len(self.correct_label_pool)+1)
			correct_data = correct_data + self.full_confusion_matrix[curr_id]
			self.precision_label_pool[i] =  self.full_confusion_matrix[curr_id] / self.precision_label_pool[i]
			self.recall_label_pool[i] =  self.full_confusion_matrix[curr_id] / self.recall_label_pool[i]
			
			print(self.correct_label_pool[i] + " = (" + str(self.precision_label_pool[i]) + ", " + str(self.recall_label_pool[i]) + ", " + str(2*self.precision_label_pool[i]*self.recall_label_pool[i]/(self.precision_label_pool[i]+self.recall_label_pool[i])) + ")")
			
		print("Accuracy = " + str(correct_data/total_data))
		