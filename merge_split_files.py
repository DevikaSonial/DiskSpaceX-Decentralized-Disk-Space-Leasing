import os
import shutil
import zipfile
import subprocess

from database import *

import os
import shutil
import zipfile
import subprocess

from database import *

def retrieve_file(shared_folder, file_name, local_path, username, password):
    """
    Retrieve a file from a shared network folder.
    """
    map_command = f'net use Z: "{shared_folder}" /user:"{username}" "{password}"'
    try:
        # Disconnect any existing mapping for Z:
        subprocess.run('net use Z: /delete', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"Connecting to: {shared_folder}")
        subprocess.run(map_command, check=True, shell=True)
        
        # Copy the file from the shared folder to local path
        source_path = os.path.join("Z:\\", file_name)
        shutil.copy(source_path, local_path)
        print(f"Retrieved '{file_name}' from '{shared_folder}' to '{local_path}'")
        
        # Disconnect the mapped network drive
        subprocess.run('net use Z: /delete', check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to shared folder: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' does not exist in '{shared_folder}'")

def merge_files(part1_path, part2_path, output_path):
    """
    Merge two parts into a single file.
    """
    with open(output_path, 'wb') as output_file:
        with open(part1_path, 'rb') as part1:
            shutil.copyfileobj(part1, output_file)
        with open(part2_path, 'rb') as part2:
            shutil.copyfileobj(part2, output_file)
    print(f"Merged files into: {output_path}")

def unzip_file(zip_file_path, extract_to):
    """
    Unzip the combined zip file.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        zipf.extractall(extract_to)
    print(f"Extracted contents to: {extract_to}")

def delete_file(file_path):
    """
    Delete a file from the local system after use.
    """
    try:
        os.remove(file_path)
        print(f"Deleted the file: {file_path}")
    except Exception as e:
        print(f"Error deleting the file {file_path}: {e}")

# if __name__ == "__main__":

def retrieve_files(res,sd1,sd2):
    # print(res, "888888888888888888888888888888888")

    # Extract details from the first record
    upload_data = res[0]
    print("upload_data : ",upload_data)

    qrty1 = "SELECT * FROM system_details WHERE system_details_id='%s'" % sd1
    print("qrty : ",qrty1)
    rr=select(qrty1)[0]

    # Network details for retrieving parts using data from res
    computer1_shared_folder = upload_data['system_one']
    computer2_shared_folder = upload_data['system_two']
    part1_name = upload_data['part_one']
    part2_name = upload_data['part_two']

    print("computer1_shared_folder : ",computer1_shared_folder)
    print("computer2_shared_folder : ",computer2_shared_folder)

    computer1_shared_folder = computer1_shared_folder.replace("\\\\", "\\")
    print("cleaned_path1 : ",computer1_shared_folder)

    computer2_shared_folder = computer2_shared_folder.replace("\\\\", "\\")
    print("cleaned_path2 : ",computer2_shared_folder)

    print("part1_name : ",part1_name)
    print("part2_name : ",part2_name)
    
    # System 1 credentials
    computer1_username = rr['system_user_name']
    computer1_password = rr['system_password']

    print("computer1_username : ",computer1_username)
    print("computer1_password : ",computer1_password)
    
    # Get System 2 credentials from database
    qrty = "SELECT * FROM system_details WHERE system_details_id='%s'" % sd2
    print("qrty : ",qrty)
    system2_data = select(qrty)[0]
    print("system2_data : ",system2_data)
    
    computer2_username = system2_data['system_user_name']
    computer2_password = system2_data['system_password']

    print("computer2_username : ",computer2_username)
    print("computer2_password : ",computer2_password)

    # Local paths to save the retrieved parts
    local_part1 = "part1_retrieved.zip"
    local_part2 = "part2_retrieved.zip"
    
    # Retrieve the files
    print("\nRetrieving Part 1...")
    retrieve_file(computer1_shared_folder, part1_name, local_part1, computer1_username, computer1_password)
    
    print("\nRetrieving Part 2...")
    retrieve_file(computer2_shared_folder, part2_name, local_part2, computer2_username, computer2_password)
    
    # Merge the parts
    merged_file = "merged_file.zip"
    print("\nMerging Parts...")
    merge_files(local_part1, local_part2, merged_file)
    
    # Unzip the merged file
    extraction_folder = "extracted_files"
    print("\nUnzipping the Merged File...")
    unzip_file(merged_file, extraction_folder)
        
    # Delete the parts after merging
    print("\nDeleting merged_file, Part 1 and Part 2 from local system...")
    delete_file(local_part1)
    delete_file(local_part2)
    delete_file(merged_file)

    # # Optionally, delete the parts from the shared folders (if you have permission):
    # print("\nDeleting Part 1 and Part 2 from the shared folder on Computer 1 and Computer 2...")
    # delete_file(os.path.join(computer1_shared_folder, part1_name))
    # delete_file(os.path.join(computer2_shared_folder, part2_name))


    print("\nProcess completed.")
