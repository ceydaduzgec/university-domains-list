import json
import sys

def sort_universities_json(input_file='world_universities_and_domains.json', output_file=None):
    # If no output file is specified, use the input file
    if not output_file:
        output_file = input_file
    
    # Load the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Reorder properties in each object
    ordered_data = []
    for item in data:
        ordered_item = {
            "name": item["name"],
            "web_pages": item["web_pages"],
            "domains": item["domains"],
            "state-province": item["state-province"],
            "alpha_two_code": item["alpha_two_code"],
            "country": item["country"]
        }
        ordered_data.append(ordered_item)
    
    # Sort the list by country name, then by university name
    sorted_data = sorted(ordered_data, key=lambda x: (x["country"], x["name"]))
    
    # Write the reordered and sorted data back to the file
    with open(output_file, 'w') as f:
        json.dump(sorted_data, f, indent=2)
    
    print(f"Sorted data written to {output_file}")

if __name__ == "__main__":
    # Get the input file from command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        sort_universities_json(input_file, output_file)
    else:
        # Default to world_universities_and_domains.json if no input is given
        sort_universities_json()