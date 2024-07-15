import db
import re
import image_analyse

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
  
def run_image_describe(userid): 
    image_list = db.empty_tags_id_extractor(userid)
    
    for image_id in image_list:
        print(f"working on {image_id}")
        response = image_analyse.image_describer(image_id)
        try:
            print(f'response for {image_id} = {response.text}')
            
            ## extract keywords from response and update to db
            keywords_list = extract_keywords(response.text)
            print('keywords updated to db = ',db.update_tags_in_db(image_id,keywords_list))
            
            add_exif_and_
                         
        except Exception as e:
            print("Exception:\n", e, "\n")
            print("Response:\n", response.candidates)
    print('completed working on image describe using vertex ai')
    


    