import db
import re
import image_analyse
import vector_db


def extract_keywords(text):
    # Use regex to find the keywords after "Keywords:"
    match = re.search(r'Keywords:\s*(.*)', text)
    if match:
        keywords_str = match.group(1)
        # Split the keywords string by comma and strip any extra spaces
        keywords_list = [keyword.strip() for keyword in keywords_str.split(',')]
        print(f'extracted keywords list = {keywords_list}')
        
        return keywords_list
    return []
  
def add_image_id(response,image_id):
    return response + ' image_id = '+ image_id
    
def run_image_describe(username, userid): 
    image_list = db.empty_tags_id_extractor(userid)
    
    for image_id in image_list:
        print(f"working on {image_id}")
        
        message = "Describe the image in one paragraph and also give me keywords"
        response = image_analyse.image_describer(image_id,message)
        
        try:
            print(f'response for {image_id} = {response.text}')
            
            ## extract keywords from response and update to db
            keywords_list = extract_keywords(response.text)
            print('keywords updated to db = ',db.update_tags_in_db(image_id,keywords_list))
            print(type(response.text))
            final_image_describe_text = add_image_id(response.text,image_id)
            print(type(final_image_describe_text))
            print('hi - ',final_image_describe_text)
            
            #store it in vector
            if username not in vector_db.check_collections():
                print('collection creating')
                vector_db.create_collection(username)
                vector_db.insert_text(username,{'$vectorize' :final_image_describe_text})
            else:
                print(32342342)
                vector_db.insert_text(username,{'$vectorize' :final_image_describe_text})
                         
        except Exception as e:
            print("Exception:\n", e, "\n")
            print("Response:\n", response.candidates)
    print('completed working on image describe using vertex ai')
    return None

def extract_image_id(processed_result_from_vdb):
    match = re.search(r'image_id\s*=\s*(\w+)', processed_result_from_vdb)

    image_id = match.group(1) if match else None
    return image_id

def query_flow(username,user_id,query):
    
    result_from_vdb = vector_db.vector_search(username,query)
    print(result_from_vdb)
    processed_result_from_vdb = result_from_vdb['$vectorize']
    print(processed_result_from_vdb)
    
    image_id = extract_image_id(processed_result_from_vdb)
    print(image_id)
    message = f"From the image extract the information for the following question {query}"
    ai_response = image_analyse.image_describer(image_id,message)
    
    return ai_response.text,image_id