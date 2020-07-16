import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt

import nltk 
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from sklearn import feature_extraction
import scipy
#nltk.download('stopwords')

    
class CSVs_to_Excel():
    def __init__(self,csv_dirname = "D:/content_analysis/csv/",checkpoint_in=True, checkpoint_folder_name="checkpoint"):
        self.csv_dirname = csv_dirname
        if checkpoint_in:
            final_p=csv_dirname+checkpoint_folder_name+"/"
        else:
            aa,a=csv_dirname.split(":/")
            b=a.split("/")
            if b[-1]=="":
                b.remove(b[-1])
            if len(b)>2:
                final_p=aa+":/"
                for num,fold in enumerate(b):
                    if num<(len(b)-1):
                        final_p+=fold+"/"
                final_p=final_p+checkpoint_folder_name+"/"
            else:
                final_p=aa+":/"+b[0]+"/"+checkpoint_folder_name+"/"
        if not os.path.exists(final_p):
            os.makedirs(final_p)
        self.checkpt_dirname=final_p

    def merge_csv(self,output="raw_merged.xlsx"):
        path_output=self.checkpt_dirname+output
        if not os.path.exists(path_output):
            print('-'*120);print(' '*2,"Merging CSV Files into one xlsx path:  ")
            count=0
            for num,file in enumerate(os.listdir(self.csv_dirname)):
                if len(file.split(".csv"))>1:
                    file_path=os.path.join(self.csv_dirname,file)
                    if num==count:
                        df=pd.read_csv(file_path)
                    else:
                        df1=pd.read_csv(file_path)
                        frames=[df, df1]
                        df= pd.concat(frames)
                else:
                    count+=1
            df.to_excel(path_output,index=False)
        print('-'*120);print(' '*2,"Merged CSV Files saved at: "+ path_output)
        return path_output
    
    def merge_excel(self,file_list,tag_list,output):
        path_output=self.checkpt_dirname+output
        if not os.path.exists(path_output):
            for num,file in enumerate(file_list):
                if len(file.split(".xlsx"))>1:
                    if num==0:
                        df=pd.read_excel(file,index_col=None)
                        df["tag"]=tag_list[num]
                    else:
                        df1=pd.read_excel(file,index_col=None)
                        df1["tag"]=tag_list[num]
                        frames=[df, df1]
                        df= pd.concat(frames)
            df.to_excel(path_output,index=False)
        print('-'*120);print(' '*2,"Merged excel Files saved at: "+ path_output)
        return path_output
    
    def find_duplicates(self,path_input,output="non_dup_merged.xlsx"):
        path_output=self.checkpt_dirname+output
        if not os.path.exists(path_output):
            print('-'*120);print(' '*2,'Detecting Duplicate documents')
            df=pd.read_excel(path_input)
            print(" - Initial number of documents - With Potential duplicates",len(df))
            mask1=df.duplicated(keep=False)
            print(mask1.sum()," duplicate values found - Initial Stage")
            df2=df[~mask1]
            mask2=df2["Title"].duplicated(keep=False)
            print(mask2.sum()," duplicate values found - Second Stage - Titles")
            df3=df2[~mask2]
            df3.to_excel(path_output,index=False)
            print(" - Final number of documents - Without Potential duplicates",len(df3))
        print('-'*120);print(' '*2,'Non-duplicated documents saved at: ',path_output)     
        return path_output
    

    def group_content(self,path_input,output="ind_content.xlsx"):
        path_output=self.checkpt_dirname+output
        if not os.path.exists(path_output):
            print('-'*120);print(' '*2,'Grouping Data from Title, Abstract, Author Keywords and Index Keywords')
            df=pd.read_excel(path_input)
            raw_titles=df["Title"].tolist();             raw_absts=df["Abstract"].tolist()
            raw_authorKW=df["Author Keywords"].tolist(); raw_indexKW=df["Index Keywords"].tolist()
            spacer=" "
            title_arr=np.char.array(raw_titles);     abstract_arr=np.char.array(raw_absts)
            author_arr=np.char.array(raw_authorKW);  index_arr=np.char.array(raw_indexKW)

            spacer_arr=np.ones(title_arr.shape).astype('object')
            spacer_arr[spacer_arr==1]=spacer
            ind_content_array=title_arr+spacer_arr+abstract_arr+spacer_arr+author_arr+spacer_arr+index_arr+spacer_arr
            df["ind_content"]=ind_content_array
            df.to_excel(path_output, index=False)
        print('-'*120);print(' '*2,'Grouped Content saved at: ',path_output)  
        return path_output
    
    @staticmethod
    def load_content(path_input):
        spacer=" "
        if not os.path.exists(path_input):
            print("Error!! ",path_input," not found.")
            print("Please run group_content first")
        else:
            df=pd.read_excel(path_input)
            ind_content=df["ind_content"].tolist()
            all_content=spacer.join(ind_content)
        return ind_content, all_content

    @staticmethod
    def word_type_filter(path_input,
                         non_noun_list=['$', "''", '(', ')', ',', '.', ':', 'CC', 'CD', 'DT', 'EX',
                                        'IN', 'JJ', 'JJR', 'JJS', 'MD', 'POS','PRP', 'PRP$', 'RB', 'RBR', 'RBS',
                                        'SYM', 'TO', 'UH', 'WP$', '``']):
        print('-'*120);print(' '*2,'Removing Non-Verb or Non-noun words')
        df=pd.read_excel(path_input)
        contents=df["ind_content"].tolist()
        for num,content in enumerate(contents):
            spacer=" "
            tokens=word_tokenize(content);  tags=nltk.pos_tag(tokens)
            array=np.array(tags)
            all_word_types=array[:,1]
            for elem, non_noun in enumerate(non_noun_list):
                if elem==0:
                    mask=array[:,1]==non_noun
                else:
                    mask=np.logical_or(mask,array[:,1]==non_noun)
            mask=np.logical_not(mask)
            series=array[:,0]
            series=series[mask].tolist()
            filtered_content=spacer.join(series)
            df.loc[num,"ind_content"]=filtered_content
        df.to_excel(path_input,index=False)#return filtered_content
        print('-'*120);print(' '*2,"Updated File ", path_input, " with filtered Ind. Content")

    " Code will look for stop words only in english"
    @staticmethod
    def standard_word_filter(path_input,min_text=2, max_text=30):
        
        
        print('-'*120);print(' '*2,'Removing stopwords, symbols, keywords smaller than '+str(min_text)+' or higher than '+str(max_text))
        df=pd.read_excel(path_input)
        df2=df["ind_content"].copy()
        spacer=" "
        excludes = [',',';',':','{','}',r"\[.",r"\].",r"\(.",r"\).",
                    '0','1','2','3','4','5','6','7','8','9',
                    '!','@','#','$','%','¨','&',r"\*.",r"\+.",r"\=.",
                    '|','/','-','NaN','nan',r"\..",'   ','  ']

        stop_words = set(stopwords.words('english'))
        document_numb=df2.shape[0]
        ### change to lowercase
        df2=df2.str.lower()
        ### Remove symbols
        for exc in excludes:

            if (((exc=='-' or exc=='   ')or exc=='  ') or exc==r"\.."):
                df2=df2.str.replace(exc,spacer, case = False)
            else:
                df2=df2.str.replace(exc,"", case = False)

        for sword in stop_words:
            if sword=="d":
                pass
            else:
                df2=df2.str.replace(exc,"", case = False)
        
        ### Apply lenght filter
        for doc in range(document_numb):
            valid_text=[]
            text=str(df2[doc]).split(" ")
            for txt in text:
                if (len(txt)<max_text and len(txt)>min_text):
                    valid_text.append(txt)
            df2[doc]=spacer.join(valid_text)
        df2.to_excel(path_input, index=False)
        print('-'*120);print(' '*2,"Updated File ", path_input, " with filtered Ind. Content")   

    def user_tag_word_filter(self,filter_path_input,content_path_input, output="word_filter_Stage2.xlsx",
                             tag_list_filter=["med_out","others_out"],word_stemm=True):
        path_output=self.checkpt_dirname+output
        if not os.path.exists(path_output):
            print("Prefilter documents which contains specific keywords")
            complete_df=pd.read_excel(content_path_input)
            print(" - Starting documents from file: "+filter_path_input+" - "+len(complete_df))
            ### get excel with valid keywords, word count, stemm word, tag, filter
            words_df=pd.read_excel(filter_path_input)
            for num,tag in enumerate(tag_list_filter):
                mask=words_df["tag"]==tag
                if num==0: 
                    maskF=mask
                else:
                    maskF=maskF|mask
            if word_stemm:
                filter_words=words_df["substitute_word"][maskF]
            else:
                filter_words=words_df["word"][maskF]
            filter_words=filter_words.drop_duplicates() 
            fword_ls=filter_words.to_list()
            for num, filtword in enumerate(fword_ls):
                a=complete_df["ind_content"].str.contains(filtword)
                if num==0:
                    b=a
                else:
                    b=a|b
            filtered_df=complete_df[~b] 
            print(" - Resulting documents saved at file: ",+path_output+" - ",len(filtered_df))
            print(" based on file: ",filter_path_input)
        filtered_df.to_excel(path_output, index=False)

        return path_output
    
    def get_stem(self,path_input,output="word_count_stemm.xlsx"):
        
        path_output=self.checkpt_dirname+output
        if not os.path.exists(path_output):
            print('-'*120);print(' '*2,'Identifying words to transform into stemmed words')
            ind_content, all_content=self.load_content(path_input)
            words = nltk.word_tokenize(str(all_content))
            tags = nltk.pos_tag(words)
            words_filtered=[]
            for word, tag in tags:
                if tag[0]=='N':
                    words_filtered.append(word)
            noun_words = words_filtered
            pack=["word","count","substitute_word","replace"]
            df=pd.DataFrame(columns=pack)
            ps = PorterStemmer()
            freq = nltk.FreqDist(noun_words)
            for word, n in freq.most_common():
                substitute = ps.stem(word)
                if word==substitute:
                    df = df.append(	pd.Series([word, n,substitute,"No"],
                                    index=pack), 
                                    ignore_index=True)
                else:
                    df = df.append(	pd.Series([word, n,substitute,"Yes"],
                                    index=pack), 
                                    ignore_index=True)
            df.to_excel(path_output,index=False)
        print('-'*120);print(' '*2,'Stemmed Words saved at: ',path_output)    
        return path_output

    def apply_stem(self,stemm_input,content_input,output="stemmed_content.xlsx"):
        
        path_output=self.checkpt_dirname+output
        if not os.path.exists(path_output):
            print('-'*120);print(' '*2,'Replacing non-stemmed words')    
            df1=pd.read_excel(stemm_input)
            df2=pd.read_excel(content_input)
            ser2=df2["ind_content"]
            print("Words: ",len(df1))
            df1=df1[((df1["count"].astype("int32")>3) & (df1["replace"]=="Yes"))]
            print("Words to replaced: ",len(df1))

            count=0
            df1=df1.reset_index(drop=True)
            for num,rep_word in enumerate(df1["substitute_word"]):
                if num//500>count:
                    print(" --", round(100*num/len(df1),2),"/","100")
                    count+=1
                #from IPython import embed; embed()
                ser2=ser2.str.replace(df1.loc[num,"word"],rep_word, case = False)
            df2["ind_content"]=ser2
            df2.to_excel(path_output, index=False)
        print('-'*120);print(' '*2,'Stemmed Content saved at: ',path_output)   
        return path_output
    
    def create_corpus(self,path_input,ngram_range=(1, 2)):
        print('-'*120);print(' '*2,'Creating corpus based on selected files content')
        ind_content, all_content=self.load_content(path_input)
        words = nltk.word_tokenize(str(all_content))
        documents=ind_content
        unigram = feature_extraction.text.TfidfVectorizer(ngram_range=ngram_range)
        unigram = unigram.fit(words)
        unicorpus = unigram.transform(documents)
        uninames = unigram.get_feature_names()
        dictionary = {'%s'%name:i for i, name in enumerate(uninames)}
        self.dictionary=dictionary
        self.uninames=uninames
        self.unicorpus=unicorpus
        print('-'*120);print(' '*2,'Corpus created')

    def question_2_query(self,query_questions_list,mode="AuBuC"):
            print('-'*120);print(' '*2,'Converting Keywords of Question Queries Valid Stemm Queries')
            qs=Query_Stemmer(mode=mode)
            qs.set_uni_dict(self.uninames,self.dictionary)
            queries_final=[]
            query_idxs_exist=[]
            for q_question in query_questions_list:
                query_idxs,not_valid_query=qs.query_2id_arr(q_question)
                if query_idxs.tolist() not in query_idxs_exist:
                    query_idxs_exist.append(query_idxs.tolist())
                    queries_final.append([q_question,query_idxs,mode,not_valid_query])
            print("Not repeated queries: ", len(queries_final),
                  " from potential queries: ", len(query_questions_list))    
            print('-'*120);print(' '*2,"Question Queries converted into Valid Stemm Queries")
            self.queries_final=queries_final
            return queries_final

    def search_string_2_queries(self,keywords_pack1=[],keywords_pack2=[],keywords_pack3=[],mode="AuBuC"):
        print('-'*120);print(' '*2,'Converting Search String with Keywords into Queries')
        qs=Query_Stemmer(mode="AuBuC")
        qs.set_uni_dict(self.uninames,self.dictionary)
        queries_final,comb=qs.macro_group(keywords_pack1,keywords_pack2,keywords_pack3)
        """queries_final = combined_queries,query_idxs,match,not_valid_query"""
        print('-'*120);print(' '*2,"Search String with Keywords converted into Queries")
        self.queries_final=queries_final
        return queries_final

    def topic_modelling(self):
        print('-'*120);print(' '*2,'Topic modelling Start')
        # A ou M = Matrix =  Documentos x Keywords;  # u = Documentos x Tópico;
        # Σ ou s = Tópico x Tópico;  # v = Tópico x Keywords
        
        A = scipy.sparse.csc_matrix(self.unicorpus, dtype='double') 

        u, s, v = scipy.sparse.linalg.svds(A, k=2);#print(s)
        s = np.diag(s)
        documents_topic_space = np.dot(u, np.linalg.inv(s))
        words_topic_space = np.dot(v.transpose(), np.linalg.inv(s)).transpose()
        # print("Doc X Key= ", A.shape,"Doc X Topic= ", u.shape,
        #     "Topic X Topic= ", s.shape,"Topic X Key= ", v.shape)
        print(' '*2,"Topic Modelling  Complete");print('-'*120)

        self.documents_topic_space=documents_topic_space
        self.words_topic_space=words_topic_space
        return documents_topic_space,words_topic_space

    def document_dimens_reduction(self,queries_final,max_v=1,angle_range=1):
        print('-'*120);print(' '*2,'Document Space Dimensionality Reduction')
        centroid_pack=[] ### Store the centroid coordinate given a query vector
        centroid_names=[] ### Store the name/query_string of the centroid coordinate
        
        
        query_vector_pack=[] ### Stores the query vector
        # The main input queries_final is list containing: 
        ## all stemmed queries; stemmed queries dict values; query mode which is not relevant for this def; valid stemmed queries
        ## valid stemmed queries consist in keywords which are present in the word dictionary which is save in the unicorpus
        ### if stemmed word is not present in the dict it will not be used for the analysis
        angles_pack=[]

        for i in range(2): 
            # this loop is used to keep the query vector with a similar size of the document coordinates.
            # if this loop is not used, the scale of the plot will be affected. Used for visual matters

            
            if i==0:
                #start the code with a value of one
                startV=1
            else:
                #during i==1 the previously 
                queries_array=np.array(query_vector_pack)
                centroidX = np.dot(queries_array.max(axis=0), self.words_topic_space.transpose()).ravel()
                m_a=np.array(
                    [centroidX[0]/np.absolute(self.documents_topic_space[:,0]).max(),
                     centroidX[1]/np.absolute(self.documents_topic_space[:,1]).max()]
                            )
                m_a=np.absolute(m_a)
                max_v=m_a.max()
                startV=1/max_v
            for cent in queries_final:
                # creates a query vector based on the size of the words topic space with values equals zero
                query_vector = np.zeros((self.words_topic_space.shape[1], 1))
                # update the query vector values using the start value
                query_vector[cent[1], :] = startV
                # gets the centroid name of valid stemm 

                all_query=list(dict.fromkeys(cent[0]))
                for not_query in cent[3]:
                    all_query.remove(not_query)    
                centroid_name= all_query
                #saves the query vector
                query_vector_pack.append(query_vector.ravel())
                #converts the query vector into a query centroid give the weights from the world_topic_space
                query_centroid = np.dot(query_vector.transpose(), self.words_topic_space.transpose()).ravel()
                # get the angle the query centroid forms with the (0,0) point in the document space
                angle=self.tan_check(query_centroid)
                # stores the angle in a pack
                angles_pack.append(angle)
                # stores the centroid coord in a pack
                centroid_pack.append(query_centroid)
                # stores the centroid name in a pack
                centroid_names.append(centroid_name)
        
        # saves the pack into the class values for further uses
        self.query_vector=query_vector_pack
        self.centroid_pack=centroid_pack
        self.centroid_names=centroid_names

        # determine the recommended documents based on angle similarity
        self.max_v=max_v

        ang_range=np.array([np.array(angles_pack).min()-angle_range,np.array(angles_pack).max()+angle_range])
        print("min: ",ang_range[0]," max: ", ang_range[1], " delta: ", ang_range[1]-ang_range[0])
        # get angles from the document space coordinates
        doc_angles=self.tan_check_array(self.documents_topic_space)
        # if documents are within the angle range they will treated as valid documents
        g_docs=np.logical_and(doc_angles<=ang_range[1],doc_angles>=ang_range[0])
        self.g_docs=g_docs
        

    def plot_document_space(self,mask_recommended=[],mask_has_words=[], plot_queries=False):
        if len(mask_recommended)==0:
            mask_recommended=self.g_docs
        fig, ax1 = plt.subplots()
        fig.set_size_inches(26, 20)
        k = self.documents_topic_space.shape[1]
        ax1.scatter(0, 0, color='black', marker='o',label='vector',s=15)

        if len(mask_has_words)==0:
            svd_recommended=(self.documents_topic_space)[mask_recommended]*self.max_v
            non_svd_recommended=(self.documents_topic_space)[np.logical_not(mask_recommended)]*self.max_v


                    
            ax1.scatter(non_svd_recommended[:,0], non_svd_recommended[:,1], 
                        color='gray', marker='x',label='Not recommended',s=8)

            ax1.scatter(svd_recommended[:,0], svd_recommended[:,1], 
                        color='green', marker='x',label='SVD Recommended',s=8)
        else:
            
            mask_rec_and_has = mask_recommended & mask_has_words # rec and has - Green
            rec_and_has=(self.documents_topic_space)[mask_rec_and_has]*self.max_v

            mask_rec_and_has_not = mask_recommended & ~mask_has_words # rec and does_not_has - Blue
            rec_and_has_not=(self.documents_topic_space)[mask_rec_and_has_not]*self.max_v

            mask_rec_not_and_has = ~mask_recommended & mask_has_words # not_rec and has - Orange
            rec_not_and_has=(self.documents_topic_space)[mask_rec_not_and_has]*self.max_v

            mask_rec_not_and_has_not = ~mask_recommended & ~mask_has_words # not_rec and does_not_has - Verm
            rec_not_and_has_not=(self.documents_topic_space)[mask_rec_not_and_has_not]*self.max_v

            #from IPython import embed; embed()
            ax1.scatter(rec_and_has[:,0], rec_and_has[:,1], 
                        color='green', marker='x',label='SVD recommended and contain main keywords',s=8)

            ax1.scatter(rec_and_has_not[:,0], rec_and_has_not[:,1], 
                        color='yellow', marker='x',label='SVD recommended and do not contain main keywords',s=8)
            
            ax1.scatter(rec_not_and_has[:,0], rec_not_and_has[:,1], 
                        color='orange', marker='x',label='SVD not recommended and contain main keywords',s=8)

            ax1.scatter(rec_not_and_has_not[:,0], rec_not_and_has_not[:,1], 
                        color='gray', marker='x',label='SVD not recommended and do not contain main keywords',s=8)


        if plot_queries:
            cmap = plt.cm.get_cmap('tab20')
            colors = cmap(np.arange(len(self.queries_final)))
            for q_num in range(len(self.queries_final)):
                color_num=q_num
                if q_num>20 and q_num<=40:
                    color_num=q_num-20
                    cmap = plt.cm.get_cmap('tab20b')
                    colors = cmap(np.arange(20))
                elif q_num>40:
                    
                    color_num=q_num-40
                    cmap = plt.cm.get_cmap('cool')
                    colors = cmap(np.arange(len(self.queries_final)))
                #print(q_num,color_num)
                ax1.plot(self.centroid_pack[q_num][0], self.centroid_pack[q_num][1], 
                        color=colors[color_num], marker='o',label=self.centroid_names[q_num][:10],markersize=7)
        
        box = ax1.get_position()
        print(box.x0, box.y0, box.width, box.height*0.75)
        ax1.set_position([box.x0, box.y0, box.width, box.height*0.75])
        #ax1.legend(loc='upper right',bbox_to_anchor=(1, 1.55))
        plt.show()
        print('-'*120);print(' '*2,'Plot Best Matches')
    
    @staticmethod
    def tan_check(coordinate2d):

        coord_angle=np.arctan(coordinate2d[1]/coordinate2d[0])*180/np.pi

        if (coordinate2d[1]>=0 and coordinate2d[0]>=0):#q1
            coord_angle=coord_angle
        elif (coordinate2d[1]>=0 and coordinate2d[0]<0):#q2
            coord_angle=coord_angle+180
        elif (coordinate2d[1]<0 and coordinate2d[0]<0):#q3
            coord_angle=coord_angle+180
        elif (coordinate2d[1]<0 and coordinate2d[0]>=0):#q4
            coord_angle=coord_angle+360

        return coord_angle

    @staticmethod
    def tan_check_array(coordinate2d_array):
        #from IPython import embed;embed()
        doc_angles=np.zeros(coordinate2d_array.shape[0])
        c1=coordinate2d_array[:,0]>=0; c2=coordinate2d_array[:,0]<0 #c1 positive X values, c2 negative X values
        c3=coordinate2d_array[:,1]>=0; c4=coordinate2d_array[:,1]<0 #c3 positive Y values, c4 negative Y values

        c5=np.logical_and(c1,c3); c6=np.logical_and(c2,c3) #c5 pos. X values and pos. Y values, #c6 neg. X values and pos. Y values
        c7=np.logical_and(c2,c4); c8=np.logical_and(c1,c4) #c7 neg. X values and neg. Y values, #c8 pos. X values and neg. Y values

        angles1=np.arctan(coordinate2d_array[:,1]/coordinate2d_array[:,0])*180/np.pi
        #c9 line which can be in c5 and c7 // #c10 line which can be in c6 and c8
        c9=angles1>=0; c10=angles1<0 

        #c11 check if angle is located at c5 // #c12 check if angle is located at c7
        #c13 check if angle is located at c6 // #c14 check if angle is located at c8
        
        c11=np.logical_and(c9,c5); c12=np.logical_and(c9,c7); c13=np.logical_and(c10,c6) 
        c14=np.logical_and(c10,c8) 

        doc_angles=c11*angles1+(c12*(angles1+180))+(c13*(angles1+180))+(c14*(angles1+360))
        return doc_angles
        
class Query_Stemmer():

    def __init__(self,mode="AuBuC"):
        self.ps = PorterStemmer()
        if mode=="AuBuC":
            self.query_match=["AuBuC"]
        else:
            self.query_match=["AuB","AuC","BuC","AuBuC"]

    def set_uni_dict(self,uninames,dictionary):
        self.uninames=uninames
        self.dictionary=dictionary

    def stem_query(self, query):
        stemmed=[]
        if type(query)==str:
            query=query.split(" ")
        for word in query:
            stem=self.ps.stem(word)
            stemmed.append(stem)
        #from IPython import embed;embed()
        return stemmed

    def group_query(self):
        queries_final=[]
        count=0
        for match in self.query_match:
            if match!="AuBuC":
                if match=="AuB":
                    main=self.query_groupA
                    second=self.query_groupB
                elif match=="AuC":
                    main=self.query_groupA
                    second=self.query_groupC
                elif match=="BuC":
                    main=self.query_groupB
                    second=self.query_groupC
                combined_queries=main+second
            elif match=="AuBuC":
                main=self.query_groupA
                second=self.query_groupB
                third=self.query_groupC
                combined_queries=main+second+third

            #### query_idxs are coodinates arrays based on the 
            query_idxs,not_valid_query=self.query_2id_arr(combined_queries)

            queries_final.append([combined_queries,query_idxs,match,not_valid_query])
        return queries_final

    def query_2id_arr(self,combined_queries):
        """ get combined stemmed word queries and verify if they exist in the word dictionary
         - if the stemmed keyword does not exist, it will be added in the not valid query list
         - if they exist and the keyword is was not included in the valid queries, it will be used to retrieve its value in the dict.
         *** 2 outputs will be provided:
               - An array with dictionaty values of valid stemm words
               - An list with non_valid_queries stemm words
        """
        querys=[]
        not_valid_query=[]
        if type(combined_queries)==list and type(combined_queries[0])==str:
            for stem in combined_queries:
                if (stem in self.uninames and stem not in querys):
                    querys.append(self.dictionary[stem])
                else:
                    not_valid_query.append(stem)
            query_idxs = np.array(querys)

        # elif type(combined_queries)==list and type(combined_queries[0])==list:
            
        #     for stem_pack in combined_queries:
        #         query_pack=[]
        #         not_valid_query_pack=[]
        #         for stem in stem_pack:
        #             if (stem in self.uninames and stem not in querys):
        #                 query_pack.append(self.dictionary[stem])
                        
        #             else:
        #                 not_valid_query_pack.append(stem)
        #         if query_pack not in querys:
        #             querys.append(query_pack)
        #         not_valid_query.append(not_valid_query_pack)
        #     query_idxs = np.array(querys)
        # print("Not repeated queries: ", len(querys)," from potential queries: ", len(combined_queries))

        return query_idxs, not_valid_query
    
    def macro_group(self,keyword_packA,keyword_packB,keyword_packC):
        count=0
        query_comb=[]
        if len(keyword_packC)==0:
            self.query_match=["AuB"]
            for numa, query_word_a in enumerate(keyword_packA):
                for numb,query_word_b in enumerate(keyword_packB):
                    self.query_groupA=self.stem_query(query_word_a)
                    self.query_groupB=self.stem_query(query_word_b)
                    query_comb.append([numa,numb])
                    if count==0:
                        queries_final=self.group_query()
                    else:
                        queries_final=queries_final+self.group_query()
                    count+=1
        
        else:   
            for numa, query_word_a in enumerate(keyword_packA):
                for numb,query_word_b in enumerate(keyword_packB):
                    for numc,query_word_c in enumerate(keyword_packC):
                        self.query_groupA=self.stem_query(query_word_a)
                        self.query_groupB=self.stem_query(query_word_b)
                        self.query_groupC=self.stem_query(query_word_c)
                        query_comb.append([numa,numb,numc])
                        if count==0:
                            queries_final=self.group_query()
                        else:
                            queries_final=queries_final+self.group_query()
                        count+=1

        ### queries_final = combined_queries,query_idxs,match,not_valid_query
        return queries_final, query_comb

    """
    
    ---------------------- REFACTORING UNDER PROGRESS
    
    """
    # fa=(documents_topic_space)[np.logical_not(f1)]*max_v
    # fb=(documents_topic_space)[np.logical_not(f2)]*max_v

    # #from IPython import embed;embed()
    # cmap = plt.cm.get_cmap('Set1')
    # colors = cmap(np.arange(total_comb))
    # fig, ax1 = plt.subplots()
    # fig.set_size_inches(13, 10)
    # k = documents_topic_space.shape[1]
    
    # ax1.scatter(0, 0, color='black', marker='o',label='vector',s=12)
    # ax1.scatter(filt[:,0], filt[:,1], color='red', marker='x',label='filtered documents',s=8)
    # ax1.scatter(good[:,0], good[:,1], color='green', marker='x',label='valid documents',s=8)
    # ax1.scatter(fa[:,0], fa[:,1], color='purple', marker='x',label='doc_in',s=5)
    # ax1.scatter(fb[:,0], fb[:,1], color='yellow', marker='x',label='doc_out',s=5)

    # #for q_num in range(total_comb):
    # #    ax1.plot(centroid_pack[q_num][0], centroid_pack[q_num][1], color=colors[q_num], marker='o',label=centroid_names[q_num][:10],markersize=12)
    # ax1.legend()
    # plt.show()

    # dtf=pd.read_excel("D:/content_analysis/resumed.xlsx")["application"]
    # series_pack,series_name=t_anl.label_from_series(dtf,names=["KExt","Ont","Tlearn"])
    # #known_clust

    
    # fig, ax2 = plt.subplots()
    # fig.set_size_inches(13, 10)
    


    # colormap = cmapp.get_cmap("hsv")
    # space=np.linspace(0, 1, len(series_pack)+1)
    # for num, pack in enumerate(series_pack):
    #     doc_in_clust=documents_topic_space[np.array(series_pack[num]).astype("bool")]*max_v
    #     ax2.scatter(doc_in_clust[:,0], doc_in_clust[:,1], color=colormap(space[num]),
    #                     marker='o',label=series_name[num],s=12)
    # ax2.legend()
    # plt.show()
    # from IPython import embed;embed()
    # print("Step 8 - Filter Best Document  - Start")
    # t_anl.filter_docs(g_docs,dirname = "D:/content_analysis/csv")
    # print("Step 8 - Filter Best Document  - Complete")