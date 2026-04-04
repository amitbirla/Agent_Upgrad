from openai import OpenAI
from dotenv import load_dotenv
import os
import platform
import json
import sys

# Fix Windows console encoding for emojis
if platform.system() == "Windows":
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Create output directory
output_dir = "maersk_outputs"
os.makedirs(output_dir, exist_ok=True)

print("🔧 Investment Calculator with gpt-4o")
print("=" * 60)

# Send request to LLM
response = client.responses.create(
    model="gpt-4o-mini",
    tools=[
        {
            "type": "code_interpreter",
            "container": {"type": "auto"}
        }
    ],
    input="""
Calculate simple interest and create a bar chart.

Principal: $1000
Rate: 10% per annum
Time: 10 years

Write Python code to:
1. Calculate the interest values
2. Create a matplotlib bar chart
3. Save it as a PNG file
4. Return the image file

Execute the code using the code interpreter.
""",
    max_output_tokens=2000,
)

print("\n✅ Model Response:")
print(response.output_text)

print("\n📁 Searching for generated files...")

files_found = False

# Parse response output safely
if hasattr(response, "output"):

    for item in response.output:

        item_dict = item.model_dump()

        # Check if this is a message type with content
        if item_dict.get("type") == "message":
            
            # Look through content for annotations
            content_items = item_dict.get("content", [])
            
            for content in content_items:
                
                # Check for file annotations
                annotations = content.get("annotations", [])
                
                for annotation in annotations:
                    
                    if annotation.get("type") == "container_file_citation":
                        
                        files_found = True
                        file_id = annotation.get("file_id")
                        filename = annotation.get("filename", f"{file_id}.png")
                        container_id = annotation.get("container_id")

                        print(f"✅ Found file: {filename}")
                        print(f"   Container ID: {container_id}")
                        print(f"   File ID: {file_id}")

                        try:
                            # Download file content using the file_id
                            print(f"   Downloading file content...")
                            
                            # Use the Files API to get the content
                            file_content = client.files.content(file_id)
                            
                            file_path = os.path.join(output_dir, filename)

                            # file_content is a response object, get the bytes
                            with open(file_path, "wb") as f:
                                f.write(file_content.content)

                            print(f"💾 Saved file to: {file_path}")

                            # Auto-open image
                            system = platform.system()

                            if system == "Darwin":  # macOS
                                os.system(f'open "{file_path}"')

                            elif system == "Windows":
                                os.system(f'start "" "{file_path}"')

                            elif system == "Linux":
                                os.system(f'xdg-open "{file_path}"')

                        except Exception as e:
                            print(f"❌ Error downloading file: {e}")
                            import traceback
                            traceback.print_exc()

# If no files found, save debug info
if not files_found:
    print("⚠️ No files returned by model. Saving debug info...")

    debug_path = os.path.join(output_dir, "debug_response.json")

    with open(debug_path, "w") as f:
        json.dump(response.model_dump(), f, indent=2, default=str)

    print(f"📄 Debug saved to: {debug_path}")

print("\n" + "=" * 60)
print("✅ Script finished")



# Second example - Sales Chart
print("\n" + "=" * 60)
print("🔧 Sales Chart Example")
print("=" * 60)

response2 = client.responses.create(
    model="gpt-4o-mini",
    tools=[
        {
            "type": "code_interpreter",
            "container": {"type": "auto"}
        }
    ],
    input="""
Create a simple bar chart showing sales for four months:
Jan=120, Feb=150, Mar=170, Apr=200.
Use matplotlib and save the image as 'sales_chart.png'.
"""
)

print("\nLLM Response:")
print(response2.output_text)

# Step 2: Look for generated files in annotations
file_ids = []

for item in response2.output:
    item_dict = item.model_dump()
    
    if item_dict.get("type") == "message":
        content_items = item_dict.get("content", [])
        
        for content in content_items:
            annotations = content.get("annotations", [])
            
            for annotation in annotations:
                if annotation.get("type") == "container_file_citation":
                    file_id = annotation.get("file_id")
                    filename = annotation.get("filename", "sales_chart.png")
                    container_id = annotation.get("container_id")
                    file_ids.append((file_id, filename, container_id))

# Step 3: Download files using file_id
for file_id, filename, container_id in file_ids:
    try:
        print(f"\n📥 Attempting to download: {filename}")
        print(f"   File ID: {file_id}")
        
        # Use the Files API to get the content
        file_content = client.files.content(file_id)
        
        save_path = os.path.join(output_dir, filename)
        
        with open(save_path, "wb") as f:
            f.write(file_content.content)

        print(f"💾 Image saved as {save_path}")
        
        # Auto-open the image
        if platform.system() == "Windows":
            os.system(f'start "" "{save_path}"')
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        import traceback
        traceback.print_exc()