# Code Structure

## HTML:
1. First Page:
* Header:
 * User/Site Mini Icon  - Site Big Icon - Site Title - Login/Logout
  * not logged
  * logged  
----
2. Sign Up/In:
  * Main Block:
    * Sign in/up form
    * Login Sucess (redirect)
    * Login Failed (password or user error)
    * Forgot Username/Password    
    * Create new user
    * User Recovery
    * Confirmation Email (Success)
    * Email do not exist (Fail)
    * User exist (Fail)     
----        
3. Sys Review Start Page:
  * Header: import logged header
  * Left Menu: Disabled
  * Main Block:
    * Start New Review
    * Project name
    * Load Review (get from database)
    * Share with users   
----      
4. Sys Review Questionnaire:
  * a. Blocks:
    * BUTTONs (Store Text) (Update Text) (Delete Text)
    * Problem and Solution Space: (Filling not Mandatory)    

   
  * b. Problem Space:
    * q - Describe what is the problem your research will need to solve. 
    * Which are the benefits that will come after solving this problem?
    * q ex: Projects restrictions/Limitations of existing technologies
    * from POST label - Write down the problem space  

  * c. Solution Space:
    * q - Define which are the solutions for that problem
    * Which are the key technologies that will be used?
    * q ex: Projects restrictions/Limitations of existing technologies
    * from POST label - Write down the solution space    
        
  * d. Define Main Groups - BUTTONs:
    * (Add Relationship - Ex: Group X with Group Y) 
    * (Remove Relationship) **Mandatory 

  * e. Create Venn Diagram- BUTTONs:
    * (Generate Diagram/ Update Diagram) 
    * (Save Diagram) *Mandatory  

  * f. Keyword by Group
        * Group Block (Hide) (Expand)
        * (Add Keyword - Single or Multiple use CSV format)
        * (Load Keywords - Excel/CSV)
        * (Delete Keywords - Checkbox and Confirm delete)  

  * g. Select Language 
    * (List Dropdown)
    * (Add button) 
    * (Remove Button) *Mandatory  

  * h. Select Year Range (From) (To) *Mandatory  
  * i. Select Doc Type (List Dropdown) (Add button) (Remove Button) *Mandatory  

  * j. Non Related Keywords:
    * Create Non related Group - Same as Define Main Group
    * Add Non related keywords - Same as Keyword by Group  

  * k. Create Search String - BUTTONs:
    * (Generate Search String)
    * (Copy Text)
    * (Auto Search) (*Mandatory)  

  * l. Search Results - BUTTONs:
    * (Generate Search String) 
    * (Copy Text)
    * (Auto Search) (*Mandatory)
----         
## Python:
1. __init__.py - Start Server, Start Database  
2.  Web Functions, Server Functions and Buttons  
* routes.py:
    * *** to be listed  
* config.py:
    - server create 
    - server update  
* login.py: 
    - Login
    - Logout
    - Login 
    - Sign in
    - Create New User 
    - Email or User recobery 
    - Confirm Email
    - Check User 
    - Check password  
* question.py 
    - save_text
    - update_text 
    - remove_text 
    - save_item 
    - remove_item 
    - update_item 
    - save_to_group 
    - remove_from_group  

* venns.py 
    -  *** to be listed  

3. Database Functions
    * user:
        | username | email | password | profile | image user_id | sysrev_projects_list |  
    * sysrev_project:
        | project_name | project_id | userlist | problem_space | solution_space | group_list | Language | Year_range |doc_type | search_string_list | search_results_list | venn_image |  
    * group: 
        | project_id | keyword_list | group_id | keyword_id | group_type |      


