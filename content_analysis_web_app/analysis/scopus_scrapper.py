#import pybliometrics
#pybliometrics.scopus.utils.create_config()
import pandas as pd
from pybliometrics.scopus.scopus_search_mod import ScopusSearch

class Search_string():

    @staticmethod
    def _year_restrictions(from_year,to_year):

        name1=" AND  PUBYEAR  >  "
        name2=" AND  PUBYEAR  <  "
        final_name=name1+str(from_year)+name2+str(to_year)
        return final_name

    @staticmethod
    def _search_place(search_string,place="TITLE-ABS-KEY"):
        final_name=place+"("+search_string+")"
        return final_name

    def _year_and_s_place(self,search_string,from_year,to_year,place="TITLE-ABS-KEY"):
        name1=self._search_place(search_string)
        name2=self._year_restrictions(from_year,to_year)
        final_name = name1+name2
        return final_name

    @staticmethod
    def or_name(list1):
        for l_num,name in enumerate(list1):
            if len(name.split(" "))>1:
                #name="''"+name+"''"
                name="("+name+")"
            if l_num==0:
                #string_n="("+name+")"
                string_n=name
            else:
                #string_n=string_n+" OR "+"("+name+")"
                string_n=string_n+" OR "+name
        return string_n

    def and_3group(self,listA,listB,listC):
        string_n1=self.or_name(listA)
        string_n2=self.or_name(listB)
        string_n3=self.or_name(listC)
        string_final="("+string_n1+") AND ("+string_n2+") AND ("+string_n3+")"
        return string_final

    def and_group(self,list1,list2):
        string_n1=self.or_name(list1)
        string_n2=self.or_name(list2)
        string_final="("+string_n1+") AND ("+string_n2+")"
        return string_final

    def or_group(self,list1,list2):
        string_n1=self.or_name(list1)
        string_n2=self.or_name(list2)
        string_final="("+string_n1+") OR ("+string_n2+")"
        return string_final

    def exc_list(self,exc_list):
        for elem,list1 in enumerate(exc_list):
            if elem==0:
                exclusion_string=self.or_name(list1)
            else:
                exclusion_string=exclusion_string+" OR "+self.or_name(list1)
        return exclusion_string

    def comb_string(self,comb_lst,comb_num,from_year,to_year,exc_list=[""],place="TITLE-ABS-KEY"):
        search_string_groups=[]
        elem_list=[]
        for elem,list1 in enumerate(comb_lst):
            for elem2,list2 in enumerate(comb_lst):
                if (elem!=elem2 and comb_num[elem]!=comb_num[elem2]):
                    if (str(elem)+"_"+str(elem2)) not in elem_list:
                        search_string=self.and_group(list1,list2)
                        search_string=self.year_and_s_place(search_string,from_year,to_year,place="TITLE-ABS-KEY")
                        if (len(exc_list)>=1 and exc_list[0]!=""):
                            exclusion_string=self.exc_list(exc_list)
                            search_string=search_string+" AND NOT ("+exclusion_string+")"
                        elem_list.append((str(elem)+"_"+str(elem2)))
                        elem_list.append((str(elem2)+"_"+str(elem)))
                        search_string_groups.append(search_string)
        return search_string_groups

    def combination(self,kw_groupA,kw_groupB,kw_groupC,exc_list,from_year=2018,to_year=2020):
        search_string=self.and_3group(kw_groupA,kw_groupB,kw_groupC)
        search_string=self._year_and_s_place(search_string,from_year,to_year,place="TITLE-ABS-KEY")
        if (len(exc_list)>=1 and exc_list[0]!=""):
            exclusion_string=self.exc_list(exc_list)
            search_string=search_string+" AND LANGUAGE ( english )"
            search_string=search_string+" AND NOT ("+exclusion_string+")"
        return search_string   

def main():
    #### AI specifics

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
            "Quality Prediction", "Product Quality", "Product Analisys", "Total Quality", "Visual Defect", "Visual Quality",
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

    exc_other=["aerial images" , "aerodynamic" , "agriculture" , "air quality" , "airborne" ,
            "animal" , "archaeology" , "Astronomy" , "biological " , "broccoli" , 
            "cartographic" , "cellular" , "chemical sensor" , "crack", "cultivated" , 
            "dentistry" , "dried figs" , "drying" , "energy" , "engine test" , "fruit" , 
            "Galactic" , "Galaxy" , "gyroscope" , "harmonic" , "horticulture" , "hydraulic" , 
            "hydrological" , "impedance" , "insect" , "landslid" , "language identification" , 
            "leaves" , "line balancing" , "magneto-optical" , "meteorologic" , "microscope" , 
            "microscopic" , "microscopy " , "power transformer" , "rocks" , "satellite" , 
            "schedule" , "seismic" , "smart grid" , "substation" , "supplying" , "transformer faults" , 
            "transmission lines" , "vibration" , "wastewater" , "water distribution" , "water quality" , 
            "web" , "audio" , "canvas" , "canvases" , "cinema" , "music" , "scheduling" , "soccer" , 
            "sound" , "Waldo", "weld", "Welding", "underwater", "Network Traffic" ]

    exc_list=[exc_med,exc_hum]
    search=Search_string()
    pub_years=[2018,2019,2020]

    for year in pub_years:
        core_listA=search.combination(ai_list,mv_list,iqc_list,exc_list,year-1,year+1)
        
        #print(core_listA)
        core_listB=search.combination(ai_list,mv_list,mngt_list,exc_list,year-1,year+1)
        a=ScopusSearch(core_listA, refresh=False, subscriber=False, 
              view=None, download=False, integrity_fields=None, verbose=True,
              df_fname=("D:/content_analysis/checkpoint/scopus_load_checkpoint_AI_MV_IQC_Year"+str(year)+".csv"))
        b=ScopusSearch(core_listB, refresh=False, subscriber=False, 
              view=None, download=False, integrity_fields=None, verbose=True,
              df_fname=("D:/content_analysis/checkpoint/scopus_load_checkpoint_AI_MV_MNGT_Year"+str(year)+".csv"))

    from IPython import embed; embed() 

if __name__ == "__main__":
    main()
    