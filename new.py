from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
import shutil
import subprocess
import zipfile
import json
from database import *

def encrypt_file(input_path, key):
    """
    Encrypt a file using AES encryption.
    Returns the path to the encrypted file.
    """
    # Generate a random IV
    iv = get_random_bytes(16)
    
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Create output path for encrypted file
    encrypted_path = input_path + '.encrypted'
    
    # Read input file and encrypt
    with open(input_path, 'rb') as infile, open(encrypted_path, 'wb') as outfile:
        # Write IV at the beginning of the file
        outfile.write(iv)
        
        # Read and encrypt file content
        while True:
            chunk = infile.read(1024 * 16)  # Read 16KB at a time
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk = pad(chunk, 16)
            encrypted_chunk = cipher.encrypt(chunk)
            outfile.write(encrypted_chunk)
    
    return encrypted_path

def decrypt_file(input_path, key):
    """
    Decrypt a file using AES encryption.
    Returns the path to the decrypted file.
    """
    # Create output path for decrypted file
    decrypted_path = input_path.replace('.encrypted', '')
    
    with open(input_path, 'rb') as infile, open(decrypted_path, 'wb') as outfile:
        # Read IV from the beginning of the file
        iv = infile.read(16)
        
        # Create cipher
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Read and decrypt file content
        chunks = []
        while True:
            chunk = infile.read(1024 * 16)  # Read 16KB at a time
            if len(chunk) == 0:
                break
            decrypted_chunk = cipher.decrypt(chunk)
            chunks.append(decrypted_chunk)
        
        # Remove padding from the last chunk
        chunks[-1] = unpad(chunks[-1], 16)
        
        # Write all chunks to output file
        for chunk in chunks:
            outfile.write(chunk)
    
    return decrypted_path

def compress_file(file_path, output_path):
    """
    Compress a single file into a zip file.
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        arcname = os.path.basename(file_path)
        zipf.write(file_path, arcname)
    print(f"File compressed into: {output_path}")

def split_zip_file(zip_file_path):
    """
    Split a zip file into 2 equal parts.
    """
    file_size = os.path.getsize(zip_file_path)
    part_size = file_size // 2
    
    with open(zip_file_path, 'rb') as f:
        for part_num in range(1, 3):
            part_path = f"{zip_file_path}.part{part_num}"
            with open(part_path, 'wb') as part_file:
                if part_num == 2:
                    part_file.write(f.read())
                else:
                    part_file.write(f.read(part_size))
            print(f"Created: {part_path}")

def share_file(file_to_share, target_path, username, password, computer_name):
    """
    Share a file to a specified network path.
    """
    map_command = (
        f'net use Z: "{target_path}" /user:"{username}"'
        if password == ""
        else f'net use Z: "{target_path}" /user:"{username}" "{password}"'
    )
    try:
        subprocess.run('net use Z: /delete', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"Executing: {map_command}")
        subprocess.run(map_command, check=True, shell=True)
        
        destination_path = os.path.join("Z:\\", os.path.basename(file_to_share))
        shutil.copy(file_to_share, destination_path)
        
        print(f"File '{file_to_share}' successfully copied to {destination_path}")
        print(f"File saved on {computer_name} at: {target_path}\\{os.path.basename(file_to_share)}")
        
        subprocess.run('net use Z: /delete', check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error mapping network drive: {e}")
    except Exception as e:
        print(f"Error copying the file: {e}")

    return(file_to_share, computer_name, target_path)

def delete_file(file_path):
    """
    Delete a file from the local system after use.
    """
    try:
        os.remove(file_path)
        print(f"Deleted the file: {file_path}")
    except Exception as e:
        print(f"Error deleting the file {file_path}: {e}")

def upload_file(path, rts, title):
    # Generate a random encryption key
    key = get_random_bytes(32)  # 256-bit key for AES-256
    
    # Save the key to a file for later retrieval
    with open(f"{title}_key.bin", 'wb') as key_file:
        key_file.write(key)
    
    print("Encrypting file...")
    encrypted_file = encrypt_file(path.strip(), key)
    
    zip_output = f"{title}.zip".strip()
    compress_file(encrypted_file, zip_output)
    
    # Delete the encrypted file as it's now in the zip
    delete_file(encrypted_file)
    
    computer1 = rts[0]
    computer2 = rts[1]

    computer_name1 = computer1['system_name']
    computer1_shared_folder = rf"\\{computer1['system_name']}\{computer1['file_name']}"
    computer1_username = computer1['system_user_name']
    computer1_password = computer1['system_password']

    computer_name2 = computer2['system_name']
    computer2_shared_folder = rf"\\{computer2['system_name']}\{computer2['file_name']}"
    computer2_username = computer2['system_user_name']
    computer2_password = computer2['system_password']

    zip_file_to_split = zip_output.strip()
    split_zip_file(zip_file_to_split)

    part1 = f"{zip_file_to_split}.part1"
    part2 = f"{zip_file_to_split}.part2"

    print("\nSharing Part 1 to Computer 1...")
    shp1 = share_file(part1, computer1_shared_folder, computer1_username, computer1_password, computer_name1)

    print("\nSharing Part 2 to Computer 2...")
    shp2 = share_file(part2, computer2_shared_folder, computer2_username, computer2_password, computer_name2)

    print("\nDeleting temporary files...")
    delete_file(zip_file_to_split)
    delete_file(part1)
    delete_file(part2)

    return shp1, shp2

def retrieve_file(shared_folder, file_name, local_path, username, password):
    """
    Retrieve a file from a shared network folder.
    """
    map_command = f'net use Z: "{shared_folder}" /user:"{username}" "{password}"'
    try:
        subprocess.run('net use Z: /delete', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"Connecting to: {shared_folder}")
        subprocess.run(map_command, check=True, shell=True)
        
        source_path = os.path.join("Z:\\", file_name)
        shutil.copy(source_path, local_path)
        print(f"Retrieved '{file_name}' from '{shared_folder}' to '{local_path}'")
        
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

def retrieve_files(res, sd1, sd2):
    upload_data = res[0]
    print("upload_data : ", upload_data)

    qrty1 = "SELECT * FROM system_details WHERE system_details_id='%s'" % sd1
    print("qrty : ", qrty1)
    rr = select(qrty1)[0]

    computer1_shared_folder = upload_data['system_one']
    computer2_shared_folder = upload_data['system_two']
    part1_name = upload_data['part_one']
    part2_name = upload_data['part_two']

    computer1_shared_folder = computer1_shared_folder.replace("\\\\", "\\")
    computer2_shared_folder = computer2_shared_folder.replace("\\\\", "\\")

    computer1_username = rr['system_user_name']
    computer1_password = rr['system_password']

    qrty = "SELECT * FROM system_details WHERE system_details_id='%s'" % sd2
    system2_data = select(qrty)[0]
    
    computer2_username = system2_data['system_user_name']
    computer2_password = system2_data['system_password']

    local_part1 = "part1_retrieved.zip"
    local_part2 = "part2_retrieved.zip"
    
    print("\nRetrieving Part 1...")
    retrieve_file(computer1_shared_folder, part1_name, local_part1, computer1_username, computer1_password)
    
    print("\nRetrieving Part 2...")
    retrieve_file(computer2_shared_folder, part2_name, local_part2, computer2_username, computer2_password)
    
    merged_file = "merged_file.zip"
    print("\nMerging Parts...")
    merge_files(local_part1, local_part2, merged_file)
    
    # Create a temporary directory for the encrypted file
    temp_dir = "temp_encrypted"
    os.makedirs(temp_dir, exist_ok=True)
    
    print("\nUnzipping the Merged File...")
    unzip_file(merged_file, temp_dir)
    
    # Find the encrypted file in the temp directory
    encrypted_file = None
    for file in os.listdir(temp_dir):
        if file.endswith('.encrypted'):
            encrypted_file = os.path.join(temp_dir, file)
            break
    
    if encrypted_file:
        # Load the encryption key
        key_file = f"{upload_data['title']}_key.bin"
        try:
            with open(key_file, 'rb') as f:
                key = f.read()
            
            print("\nDecrypting file...")
            decrypted_file = decrypt_file(encrypted_file, key)
            print("dec :",decrypted_file)

            # decrypted_file = decrypted_file.replace(".decrypted", "")
            # print("dec :", decrypted_file)

           
            
            # Move the decrypted file to the final location
            final_location = os.path.join("extracted_files", os.path.basename(decrypted_file))
            os.makedirs("extracted_files", exist_ok=True)
            shutil.move(decrypted_file, final_location)
            
            print(f"\nFile successfully decrypted and saved to: {final_location}")
        except Exception as e:
            print(f"Error during decryption: {e}")
    else:
        print("Error: Could not find encrypted file in the merged zip")
    
    # Cleanup
    print("\nCleaning up temporary files...")
    delete_file(local_part1)
    delete_file(local_part2)
    delete_file(merged_file)
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    print("\nProcess completed.")