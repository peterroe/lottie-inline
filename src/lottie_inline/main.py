import os
import json
import base64
import argparse

def convert_image_to_base64(image_path):
    """
    Convert image file to base64 string
    """
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_file_size_kb(file_path):
    """
    Get file size in KB
    """
    return os.path.getsize(file_path) / 1024

def process_lottie_json(input_json_path, output_json_path, max_size_kb=None):
    """
    Process Lottie JSON file to inline image resources as base64
    max_size_kb: Maximum file size in KB to convert to base64
    """
    
    # Read input JSON
    with open(input_json_path, 'r', encoding='utf-8') as file:
        lottie_data = json.load(file)
    
    is_same_path = os.path.abspath(input_json_path) == os.path.abspath(output_json_path)
    # Get directory of input JSON to resolve relative paths
    json_dir = os.path.dirname(input_json_path)
    print(json_dir)
    # Process assets
    if 'assets' in lottie_data:
        for asset in lottie_data['assets']:
            if 'u' in asset and 'p' in asset:
                # Construct full image path
                image_path = os.path.join(json_dir, asset['u'], asset['p'])
                
                if os.path.exists(image_path):
                    # Check file size if max_size_kb is specified
                    if max_size_kb is not None:
                        file_size_kb = get_file_size_kb(image_path)
                        if file_size_kb > max_size_kb:
                            print(f"Skipping {image_path} ({file_size_kb:.2f}KB > {max_size_kb}KB)")
                            # Create the output path if input and output paths are different
                            if not is_same_path:
                                output_image_path = os.path.join(os.path.dirname(output_json_path), asset['u'], asset['p'])
                                os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
                                with open(output_image_path, 'wb') as out_file:
                                    out_file.write(open(image_path, 'rb').read())
                            continue
                    
                    # Convert image to base64
                    base64_data = convert_image_to_base64(image_path)
                    extension = os.path.splitext(image_path)[1].lstrip('.')
                    # Replace path with base64 data
                    asset['u'] = ""
                    asset['p'] = f"data:image/{extension};base64,{base64_data}"
                    # Set the asset to be embedded
                    asset['e'] = 1
                else:
                    print(f"Warning: Image not found at {image_path}")
    
    # Write output JSON
    with open(output_json_path, 'w', encoding='utf-8') as file:
        json.dump(lottie_data, file)

def main():
    parser = argparse.ArgumentParser(description='Convert Lottie JSON images to base64')
    parser.add_argument('input', help='Input JSON file path')
    parser.add_argument('output', help='Output JSON file path')
    parser.add_argument('--max-size', type=float, help='Maximum file size in KB to convert to base64')
    
    args = parser.parse_args()
    
    process_lottie_json(args.input, args.output, args.max_size)

if __name__ == '__main__':
    main()
