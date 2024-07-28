import json

def convert_jsonl_to_json(jsonl_filepath, json_filepath):
    data = []
    max_length = 0
    # Open the JSON Lines file and read each line
    with open(jsonl_filepath, 'r') as file:
        for line in file:
            # Each line is a complete JSON object
            if line.strip():
                line_data = json.loads(line)
                line_data["content_length"] = len(line_data["article_content"])
                max_length = max(max_length,line_data["content_length"] )
                data.append(line_data)
        print("max_length: ",max_length)
        print("length ", len(data))
    
    # Write the data as a JSON array to a new file
    with open(json_filepath, 'w') as file:
        json.dump(data, file, indent=4)
        
    
if __name__ == "__main__":
    jsonl_filepath = './knowledge_base_results_all.jsonl'  # Path to your JSON Lines file
    json_filepath = './knowledge_base_results_all.json'    # Path to the JSON file you want to create
    convert_jsonl_to_json(jsonl_filepath, json_filepath)
