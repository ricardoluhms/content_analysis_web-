from scopus_scrapper import Search_string
from text_analysisV2 import Query_Stemmer, CSVs_to_Excel
import pandas as pd
from pybliometrics.scopus.scopus_search_mod import ScopusSearch
from pybliometrics.scopus import AbstractRetrieval
import os
from habanero import Crossref

class Scrap_and_Analysis():

	def __init__(self,
				kw_list=[["kwlist_one","kwlist_two","kwlist_three"],["kwlist_one","kwlist_two","kwlist_four"]],
				tag_list=["AI_MV_IQC","AI_MV_MNGT"],
				keyword_exc_list_of_list=["exc_kwlist_one","exc_kwlist_two"],
				pub_years_list=[2018,2019,2020],
				main_folder="D:/content_analysis/",
				main_file_name="scopus_load_checkpoint_eng_lan"
				 ):

		self.kw_list=kw_list
		self.tag_list=tag_list
		self.keyword_exc_list_of_list=keyword_exc_list_of_list
		self.pub_years_list=pub_years_list
		self.main_folder=main_folder
		self.main_file_name=main_file_name
		self.search=Search_string()
		self.folder_path_list=[]
		self.search_input_pack=[]
		self.csv_filename_list=[]
		self.search_output_pack=[]
		self.merge_csv_path_list=[]

	def download_from_scopus(self,retrieve_online_data=True):

		for num,tag in enumerate(self.tag_list):
			dir_name=self.main_folder+tag+"/"
			if not os.path.exists(dir_name):
				os.mkdir(dir_name)
			self.folder_path_list.append(dir_name)
			for year in self.pub_years_list:
				file_name=dir_name+self.main_file_name+"_Year"+str(year)+".csv"
				self.csv_filename_list.append(file_name)
				core_list=self.search.combination(self.kw_list[num][0],
												  self.kw_list[num][1],
												  self.kw_list[num][2],
												  self.keyword_exc_list_of_list,
												  year-1,
												  year+1)
				self.search_input_pack.append(core_list)
				if retrieve_online_data:
					search_output=ScopusSearch(core_list, refresh=False, subscriber=False, 
					view=None, download=False, integrity_fields=None, verbose=True,
					df_fname=file_name)
					self.search_output_pack.append(search_output)
	
	def merge_tag(self,renew=False):
		if renew:
			self.merge_csv_path_list=[]
		for num,folder in enumerate(self.folder_path_list):
			csv_core=CSVs_to_Excel(csv_dirname= folder,checkpoint_folder_name="checkpoint")
			csv_merged_path=csv_core.merge_csv(output="raw_merged"+self.tag_list[num]+".xlsx")
			self.merge_csv_path_list.append(csv_merged_path)
			print(' '*2,"Tag: "+self.tag_list[num])

	def check_duplicated_tag(self,
							 checkpoint_folder_name="merged_results",
							 output='complete_scopus_data.xlsx'):

		self.csv_core=CSVs_to_Excel(self.main_folder,
										checkpoint_folder_name=checkpoint_folder_name)

		merged_path=self.csv_core.merge_excel(self.merge_csv_path_list,
										 tag_list=self.tag_list,
										 output=output)

		df=pd.read_excel(merged_path,index_col=None); 	df_resume=df[["Title","tag"]]

		df_dup=df_resume[df_resume["Title"].duplicated(keep=False)].sort_values("Title")

		check_list={}; 		skip_list=[]

		for num, title in enumerate(df_dup["Title"].tolist()):
			if num not in skip_list:
				mini_df=df_resume[df_resume["Title"]==title]
				tags=mini_df["tag"].drop_duplicates(keep="first").tolist()
				final_tag=""
				if len(tags)>1:
					for tag in tags:
						final_tag=final_tag+" + "+tag
					check_list.update({title:final_tag})
				else:
					check_list.update({title:tag})
				skip_num=len(mini_df)
				for skip in range(skip_num):
					skip_list.append(num+skip)

		dup2=df_resume["Title"].duplicated(); 	non_dup=df[~dup2]

		for title in list(check_list.keys()):
			title_mask=non_dup["Title"]==title
			non_dup.loc[title_mask,"tag"]=check_list[title]
		
		self.non_dup_path=self.main_folder+checkpoint_folder_name+"/"+output
		non_dup.to_excel(self.non_dup_path,index=False)
		print('-'*120);print(' '*2,"Non_duplicated documents saved at: "+ self.non_dup_path);print('-'*120)		

	def query_question(self,subject_list,verbs_questions_list,subject_characteristics_list, object_list=[],
						object_characteristics_list=[],additional_list=[]):
		self.qs=Query_Stemmer()
		query_question_list=[]
		
		for subject in subject_list:
			for verbs in verbs_questions_list:
				for characteristics in subject_characteristics_list:
					question=(subject+" "+verbs+" "+characteristics+" "+
					" ".join(object_list)+" "+" ".join(object_characteristics_list)+" ".join(additional_list))
					stemm_question=self.qs.stem_query(question)
					query_question_list.append(stemm_question)
		return query_question_list


def main():

	ai_list=["AI","Artificial Intelligence","Automatic Encoder", "ANN","Artificial Neural Network",
			"CNN", "Convolutional Neural Network", "Decision Tree","DBN","Deep Belief Network","Deep Learning",
			"ELM", "Extreme Machine Learning", "GAN", "Generative adversarial network","Genetic Algorithm",
			"MLP" ,"Multi Layer Perceptron","MultiLayer Perceptron", "Machine Learning ", "Neural Network",
			"Random Forest", "Reinforcement Learning", "RBM","Restricted Boltzmann machine", 
			"Recursive Neural Network", "R-CNN","Support Vector Machine","SVM","Swarm Intelligence","Swarm Optimization"]

	#### Solution Management specifics
	mngt_list=["GUI-based", "integrated development", "graphic user interface", "Integrated Development Environment","IDE",
			"Knowledge Transfer", "Knowledge Management","Deploy Solution","Solution Management","Pipeline Creation",
			"Pipeline Management","Pipeline Deploy","Software Management","Pipeline Management","Software Architecture"]

	#### Management specifics
	iqc_list=["Anomaly Detection","Assembly line","automated quality control", "Confusion Matrix" , "Defect Detection",
			"Fault detection", "Factory", "Factories", "Flaw Detection","Industry", "Industrial Application",
			"Industrial Inspection", "KPI", "Key Performance Indicator", "Manufact*", "Quality Control", "Quality Expert", 
			"Quality Prediction", "Product Quality", "Product Analysis", "Total Quality", "Visual Defect", "Visual Quality",
			"Visual Inspection"]

	mv_list=["computer vision","Feature Extraction","Image Classification","Image Classifier","Image Processing",
			"Imaging technology","machine vision","MTT","Multi Target Tracking","Object Detection","Object Recognition","ORB",
			"Part Detection","Pattern Recognition","Robot Vision","Shape Recognition","SIFT","SURF","Template Matching"]

	exc_hum=["balancing " , "behavioral" , "body postures" , "Celebrity" ,
			"Crowd analysis" , "crowd behaviour" , "Ear recognition" , "emotional" ,
			"face" , "facial" , "finger detection" , "gesture" , "hand gesture" ,
			"handwrit" , "Handwriting" , "human part" , "human pose" , "multi-touch" ,
			"online purchase" , "pedestrian" , "Sign language" , "speech" , "speech recognition"]

	exc_med=["Alzheimer" , "analgesic" , "auditory" ,
			"biopsy" , "blastocyst" , "blood" , "bone" , "brain tumor" , "brainstem" , "breast" , 
			"cancer" , "cardiac" , "cardiology" , "Cardiovascular" , "cartilage" , "catheter" , "cytometry" ,
			"Dermoscopy" , "diabetic" , "disease" , "DNA" , 
			"Echocardiography" , "EEG" , "Electrocardiogram" , "electroencephalogram" , 
			"electrophysiological" , "endoscopy" , "fetal" , "fluoroscopy" , 
			"gemologica" , "Genome" , 
			"health" , "hippocampus" , "histopathology" , 
			"laparoscopic " , "liver" , "lung" ,
			"mammographic" , "mammography" , "medic" , "mitotic" , "MRI" , 
			"neuroimaging" , "olfactory" , 
			"pancreatic" , "pathological" , "patient" , "pediatric" ,
			"physiotherapy" , "pneumonia" , "protein" , "proteomics" , "psychology" ,
			"radiation" , "Radiology" , "radiotherapy" , "rehabilitation" , "resonance" , "retinal" , 
			"saliva" , "skeleton" , "spinal cord" , "stroke" , "subcutaneous" ,
			"Surgery" , "Syndrome" , 
			"thyroid" , "tissue" , "tomography" , "toxicity" ,
			"tractography" , "tumor" , "white matter"]

	# exc_other=["aerial images" , "aerodynamic" , "agriculture" , "air quality" , "airborne" ,
	# 		"animal" , "archaeology" , "Astronomy" , "biological " , "broccoli" , 
	# 		"cartographic" , "cellular" , "chemical sensor" , "crack", "cultivated" , 
	# 		"dentistry" , "dried figs" , "drying" , "energy" , "engine test" , "fruit" , 
	# 		"Galactic" , "Galaxy" , "gyroscope" , "harmonic" , "horticulture" , "hydraulic" , 
	# 		"hydrological" , "impedance" , "insect" , "landslid" , "language identification" , 
	# 		"leaves" , "line balancing" , "magneto-optical" , "meteorologic" , "microscope" , 
	# 		"microscopic" , "microscopy " , "power transformer" , "rocks" , "satellite" , 
	# 		"schedule" , "seismic" , "smart grid" , "substation" , "supplying" , "transformer faults" , 
	# 		"transmission lines" , "vibration" , "wastewater" , "water distribution" , "water quality" , 
	# 		"web" , "audio" , "canvas" , "canvases" , "cinema" , "music" , "scheduling" , "soccer" , 
	# 		"sound" , "Waldo", "weld", "Welding", "underwater", "Network Traffic" ]


	sca=Scrap_and_Analysis(kw_list=[ [ai_list,mv_list,iqc_list], [ai_list,mv_list,mngt_list]], 
							tag_list=['AI_MV_IQC','AI_MV_MNGT'], 
							keyword_exc_list_of_list=[exc_hum,exc_med], 
							pub_years_list=[2018,2019,2020], 
							main_folder='D:/content_analysis/', 
							main_file_name='scopus_load_checkpoint_eng_lan')


	sca.download_from_scopus(retrieve_online_data=False)
	
	sca.merge_tag()

	sca.check_duplicated_tag(checkpoint_folder_name="merged_results",
								 output='complete_scopus_data.xlsx')
	
	group_content_path=sca.csv_core.group_content(sca.non_dup_path,output="ind_content.xlsx")

	ind_content, all_content=sca.csv_core.load_content(group_content_path)

	sca.csv_core.word_type_filter(group_content_path)

	sca.csv_core.standard_word_filter(group_content_path,min_text=1)

	stemm_path=sca.csv_core.get_stem(group_content_path,output='word_count_stemm.xlsx')

	stemmed_content_path=sca.csv_core.apply_stem(stemm_path,group_content_path,output='stemmed_content.xlsx')

	sca.csv_core.create_corpus(stemmed_content_path,ngram_range=(1,2))

	questionA=  { 'subject_list': ["Assembly line","automated quality control", "Factory", "Factories", "Industry", "Industrial Application",
	                               "Industrial Inspection", "Manufact*", "Product Quality", "Product Analysis"],

				  'verbs_questions_list': ["selecting","installing","monitoring","controlling","applying"],

				  'subject_characteristics_list': ["Robot Vision","machine vision"], 

				  'object_list': ["Confusion Matrix", "KPI", "Key Performance Indicator", "computer vision"],
				  
				  'object_characteristics_list': ["AI","Artificial Intelligence","Deep Learning","Machine Learning", "Neural Network"],
				 
				  'additional_list': ["Inspection System","Deploy Solution","Pipeline Creation","Pipeline Deploy","Quality Prediction"] }
	
	questionB=  { 'subject_list': ["Assembly line","automated quality control", "Factory", "Factories", "Industry", 
	                               "Industrial Application", "Industrial Inspection", "Manufact*", "Product Quality", "Product Analysis"],
				  
				  'verbs_questions_list': ["assess","install","implement","apply"],
				  
				  'subject_characteristics_list': ["technical requirements"," technical limitations","requisites"],
				  
				  'object_list': ["Robot Vision","machine vision"],
				  
				  'object_characteristics_list': ["AI","Artificial Intelligence","Deep Learning","Machine Learning", "Neural Network"],
	              
				  'additional_list': ["Inspection System","Deploy Solution","Interference", "existing equipment"] }

	questionC= { 'subject_list': ["Anomaly Detection" , "Anomaly Type", "Defect Detection", "Defect Type",
								  "Fault detection", "Fault type", "Flaw Detection", "Flaw type", "Visual Defect"],

				 'verbs_questions_list': ["evaluate","assess","requires"],
				 
				 'subject_characteristics_list': ["shape","features","size","complexities","background","lighting","weather"],
				 
				 'object_list': ["Robot Vision", "machine vision","Industrial Inspection"],
				 
				 'object_characteristics_list': ["AI","Artificial Intelligence","Deep Learning","Machine Learning","Neural Network"],
			
				 'additional_list': ["Inspection System","Deploy Solution", "Pipeline Deploy","Quality Prediction",
				                     "Visual Quality","Product Quality"] }

	questionD= { 'subject_list': ["Assembly line","automated quality control", "Factory", "Factories", "Industry", 
								  "Industrial Application", "Industrial Inspection", "Manufact*", "Product Quality", "Product Analysis"],

				 'verbs_questions_list': ["place","position","put","fix","install","location"],
				 
				 'subject_characteristics_list': ["moving","static","components","lens","filters","optic","illumination"],
				 
				 'object_list': ["Robot Vision","machine vision"],
				 
				 'object_characteristics_list': ["AI","Artificial Intelligence","Deep Learning","Machine Learning", "Neural Network"],
				 
				 'additional_list': ["Inspection System","Deploy Solution","Pipeline Creation","Pipeline Deploy","Quality Prediction"]}

	questionE=   { 'subject_list': ["Assembly line","automated quality control", "Factory", "Factories", "Industry",
	                                "Industrial Application", "Industrial Inspection", "Manufact*", "Product Quality",
									"Product Analysis"],
				   'verbs_questions_list': ["communication","connection","compatible"],
				   
				   'subject_characteristics_list': ["protocol","requirements"],
				   
				   'object_list': ["Robot Vision","machine vision"],
				   
				   'object_characteristics_list': ["AI","Artificial Intelligence","Deep Learning","Machine Learning", "Neural Network"], 
				   
				   'additional_list': ["Inspection System","Deploy Solution","Pipeline Creation","Pipeline Deploy","Quality Prediction"] }

	questionF1=  { 'subject_list': ["AI","Artificial Intelligence","Automatic Encoder", "ANN","Artificial Neural Network",
										"CNN", "Convolutional Neural Network", "Decision Tree","DBN","Deep Belief Network","Deep Learning",
										"ELM", "Extreme Machine Learning", "GAN", "Generative adversarial network","Genetic Algorithm",
										"MLP" ,"Multi Layer Perceptron","MultiLayer Perceptron", "Machine Learning ", "Neural Network",
										"Random Forest", "Reinforcement Learning", "RBM","Restricted Boltzmann machine", 
										"Recursive Neural Network", "R-CNN","Support Vector Machine","SVM",
										"Swarm Intelligence","Swarm Optimization"], 

					'verbs_questions_list': ["application","funcion","improve","evolution","deploy"], 
					
					'subject_characteristics_list': ["algorithm","Technique","architecture","pipeline"], 
					
					'object_list': ["Robot Vision","machine vision","computer vision"], 
					
					'object_characteristics_list': ["Industrial Inspection","Industrial Application","Industrial Application",
													"Product Quality", "Product Analysis"], 
					
					'additional_list': [] }

	questionF2=  { 'subject_list': ["AI","Artificial Intelligence","Automatic Encoder", "ANN","Artificial Neural Network",
										"CNN", "Convolutional Neural Network", "Decision Tree","DBN","Deep Belief Network","Deep Learning",
										"ELM", "Extreme Machine Learning", "GAN", "Generative adversarial network","Genetic Algorithm",
										"MLP" ,"Multi Layer Perceptron","MultiLayer Perceptron", "Machine Learning ", "Neural Network",
										"Random Forest", "Reinforcement Learning", "RBM","Restricted Boltzmann machine", 
										"Recursive Neural Network", "R-CNN","Support Vector Machine","SVM",
										"Swarm Intelligence","Swarm Optimization"], 

					'verbs_questions_list': ["survey","review"], 
					
					'subject_characteristics_list': ["algorithm","Technique","architecture","pipeline"], 
					
					'object_list': ["Robot Vision","machine vision","computer vision"], 
					
					'object_characteristics_list': ["Industrial Inspection","Industrial Application","Industrial Application",
													"Product Quality", "Product Analysis"], 
					
					'additional_list': [] }

	questions_group={"questF_has_tech":questionF1,"questF_is_RorS":questionF2}
	#questions_group={"questA":questionA,"questB":questionB,"questC":questionC,"questD":questionD,"questE":questionE}

	df=pd.read_excel(sca.non_dup_path)
	for group_key in questions_group.keys():
		
		group=questions_group.get(group_key)
		for subject in group.get('subject_list'):
		
			query_questions=sca.query_question( subject_list=[subject],
												verbs_questions_list=group.get('verbs_questions_list'),
												subject_characteristics_list=group.get('subject_characteristics_list'),
												object_list=group.get('object_list'),
												object_characteristics_list=group.get('object_characteristics_list'),
												additional_list=group.get('additional_list'))

			queries_final=sca.csv_core.question_2_query(query_questions)
			sca.csv_core.topic_modelling()
			sca.csv_core.document_dimens_reduction(queries_final)
			
			good_docs_mask=sca.csv_core.g_docs
			
			for num, sub_key in enumerate(group.get('subject_list')):
				if num==0:
					#from IPython import embed; embed()
					mask_sub=df["Abstract"].str.contains(sub_key)
				else:
					mask_sub= mask_sub | df["Abstract"].str.contains(sub_key)
				#print("iter: ",num, "mask_sub sum= ",mask_sub.sum())
			
			for num, verb_key in enumerate(group.get('verbs_questions_list')):
				if num==0:
					mask_verb=df["Abstract"].str.contains(verb_key)
				else:
					mask_verb= mask_verb | df["Abstract"].str.contains(verb_key)
				#print("iter: ",num, "mask_verb sum= ",mask_verb.sum())

			for num, char_key in enumerate(group.get('subject_characteristics_list')):
				if num==0:
					mask_char=df["Abstract"].str.contains(char_key)
				else:
					mask_char= mask_char | df["Abstract"].str.contains(char_key)
				#print("iter: ",num, "mask_char sum= ",mask_char.sum())
			
			mask_final=mask_sub & mask_verb & mask_char

			mask_and=mask_final & good_docs_mask

			core_column=("sl: "+"_".join(group.get('subject_list'))+
						  " vb: "+"_".join(group.get('verbs_questions_list'))+
						  " ch: "+"_".join(group.get('subject_characteristics_list')))

			column_nameA="Recommendation: "+core_column
			df[column_nameA]=" - "
			df.loc[good_docs_mask,column_nameA]="check"

			column_nameB="Has Words: "+core_column
			df[column_nameB]=" - "
			df.loc[mask_final,column_nameB]="check"

			column_nameC="Recommendation and Has Words: "+core_column
			df[column_nameC]=" - "
			df.loc[mask_and,column_nameC]="check"
			sca.csv_core.plot_document_space(mask_recommended=good_docs_mask,
			  								 mask_has_words=mask_final,
			  								 plot_queries=True)

	#df.to_excel(sca.non_dup_path,index=False)
	
	df2=pd.read_excel("D:/content_analysis/merged_results/complete_scopus_data_09_04_2020.xlsx",sheet_name="Base")
	import matplotlib.pyplot as plt
	import numpy as np
	fig, ax1 = plt.subplots()
	fig.set_size_inches(26, 20)
	eval_tag=df2['Phase and Phase2 Complete Evaluation'].drop_duplicates().sort_values()
	out_tag=eval_tag.str.contains(" out ")

	cmap = plt.cm.get_cmap('jet'); colors = cmap(np.arange(255))
	color_count=int(255/len(eval_tag))

	out_tag=out_tag.tolist()
	for num,s_eval in enumerate(eval_tag):
		mask=df2['Phase and Phase2 Complete Evaluation']==s_eval
		docs=sca.csv_core.documents_topic_space[mask]*sca.csv_core.max_v
		if out_tag[num]:
			mark='x'
			size=8
		else:
			mark='o'
			size=24
		ax1.scatter(docs[:,0], docs[:,1], 
                    color=colors[num*color_count], marker=mark,label=s_eval,s=size)
	
	box = ax1.get_position()
	print(box.x0, box.y0, box.width, box.height*0.75)
	ax1.set_position([box.x0, box.y0, box.width, box.height*0.75])
	ax1.legend(loc='upper right',bbox_to_anchor=(1, 1.55))
	plt.show()
	from IPython import embed;embed()
	

def example2():
	folder_list=["D:/content_analysis/csv/"]
	#### Set CSV Folder that contains multiples CSVs extracted from Scopus
	for fold in folder_list:
		csv_core=CSVs_to_Excel(csv_dirname= fold)
		#### Merges All CSV files into a single xlsx file
		merged_path=csv_core.merge_csv(output='raw_merged.xlsx')
	
		#### Remove duplicate files from the merged file
		non_dup_path=csv_core.find_duplicates(merged_path,output="non_dup_merged.xlsx")

		#### Groups Title, Abstract and Author Keywords Information 
		####- This Grouped Information is located in "Ind. Content" (Individual Content of each document)
		group_content_path=csv_core.group_content(non_dup_path,output="ind_content.xlsx")

		#### Generic Function that reads a file and returns the individual content and the combined content ("All Content") of all files
		#### "All Content" is a STR output which is used in NLTK library
		ind_content, all_content=csv_core.load_content(group_content_path)

		#### Word type filer uses the NLTK word_tokenize and pos_tag to detect which type of word  (verb, noun, adjective,...)
		#### This information is used to remove undesired type of words 
		#### (a non_noun_list is automatically passed but it can be edited
		csv_core.word_type_filter(group_content_path)

		csv_core.standard_word_filter(group_content_path)
		#### If you are running the code for the first time, you must run the get_stem to find the stemming of each word
		stemm_path=csv_core.get_stem(group_content_path,output='word_count_stemm.xlsx')

		#### From this point you can either apply the stemm replacement or ...
		#### ....analyse the stemm_path file to indidually label each type of word and apply user_tag_word_filter command
		#### the second option is recommended when the user is more familiar with the most relevant keywords
		stemmed_content_path=csv_core.apply_stem(stemm_path,group_content_path,output='stemmed_content.xlsx')
		print("stemmed_content_path output: ", stemmed_content_path)
		
		csv_core.create_corpus(stemmed_content_path,ngram_range=(1,2))

		#### Applications

		#### The Document Research Recommendation Algorithm (DRRA) requires the Research Keywords as the main input 
		#### 
		app_A=["knowledge","extraction"]; app_B=["ontology","visual"]
		app_C=["transfer", "learning"]; app_D=["digital", "twin"]
		app_E=["synthetic", "dataset"]
		#app_pack=[app_A,app_B,app_C,app_D,app_E]
		app_pack=[app_A,app_B,app_C]

		#### Machine Vision
		mv_list_specific1=["time","flight","tof"]
		mv_list_specific2=["rgbd","rgd-d","stereo","vision","photogrammetry"]
		mv_list_core=["image","processing","technology","computer","vision","machine"]
		#mv_pack=[mv_list_specific1,mv_list_specific2,mv_list_core]
		mv_pack=[mv_list_core]

		#### Artificial Intelligence
		## Standard Techniques/Algorithms
		std_ai =["ensemble", "neural", "networks","decision", "tree", "dimensionality",
					"reduction","clustering","cluster","autoencoder","evolutionary","algorithms","genetic",
					"machine"] 
		## Validated State of the Art
		dl_ai=["deep","learning","convolutional","neural", "network","cnn","rcnn","r-cnn"]
		## Breakthrough techniques
		bkt_ai=["hybrid","learning","capsule", "Network",
			"deep","reinforcement", "learning","automl","automated", "machine", "learning",
			"generative", "adversarial", "network"]
		ai_pack=[std_ai,dl_ai,bkt_ai]
		
		queries_final=csv_core.search_string_2_queries(app_pack,mv_pack,ai_pack)

		csv_core.topic_modelling()

		csv_core.document_dimens_reduction(queries_final)

		csv_core.plot_document_space()


if __name__ == "__main__":
	main()

