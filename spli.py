import os
import shutil
import subprocess
import zipfile



from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
import shutil
import subprocess
import zipfile
import json
from database import *


def compress_folder(folder_path, output_path):
    """
    Compress a folder into a zip file.
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(f"Folder compressed into: {output_path}")

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
    part_size = file_size // 2  # Divide file size by 2
    
    with open(zip_file_path, 'rb') as f:
        for part_num in range(1, 3):
            part_path = f"{zip_file_path}.part{part_num}"
            with open(part_path, 'wb') as part_file:
                # Write the appropriate amount of bytes (part_size)
                if part_num == 2:  # Write all remaining data to the last part
                    part_file.write(f.read())
                else:
                    part_file.write(f.read(part_size))
            print(f"Created: {part_path}")


def share_file(file_to_share, target_path, username, password, computer_name):
    """
    Share a file to a specified network path with improved error handling.
    """
    try:
        # Format the network command based on password presence
        map_command = (
            f'net use Z: "{target_path}" /user:"{username}"'
            if password == ""
            else f'net use Z: "{target_path}" /user:"{username}" "{password}"'
        )

        # First ensure Z: drive is disconnected
        print("Cleaning up any existing Z: drive mapping...")
        subprocess.run('net use Z: /delete', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Try to connect to the network share
        print(f"Executing: {map_command}")
        result = subprocess.run(map_command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Failed to map network drive: {result.stderr}")
        
        # Verify the drive is mapped
        if not os.path.exists('Z:'):
            raise Exception("Z: drive not found after mapping")
            
        # Copy the file to the shared folder
        destination_path = os.path.join("Z:\\", os.path.basename(file_to_share))
        
        # Verify source file exists
        if not os.path.exists(file_to_share):
            raise Exception(f"Source file not found: {file_to_share}")
            
        # Copy with verification
        shutil.copy2(file_to_share, destination_path)
        
        # Verify the file was copied successfully
        if not os.path.exists(destination_path):
            raise Exception("File was not copied to destination")
            
        # Verify file sizes match
        if os.path.getsize(file_to_share) != os.path.getsize(destination_path):
            raise Exception("Copied file size does not match source file")
        
        print(f"File '{file_to_share}' successfully copied to {destination_path}")
        print(f"File saved on {computer_name} at: {target_path}\\{os.path.basename(file_to_share)}")
        
    except Exception as e:
        print(f"Error during file sharing: {str(e)}")
        raise
        
    finally:
        try:
            # Always try to disconnect the drive in the finally block
            print("Disconnecting Z: drive...")
            subprocess.run('net use Z: /delete', shell=True, check=True)
            print("Z: drive disconnected successfully")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not disconnect Z: drive: {e}")
    
    return (os.path.basename(file_to_share), computer_name, target_path)
def delete_file(file_path):
    """
    Delete a file from the local system after use.
    """
    try:
        os.remove(file_path)
        print(f"Deleted the file: {file_path}")
    except Exception as e:
        print(f"Error deleting the file {file_path}: {e}")


# def upload_file(path,rts):  
#     # choice = input("Do you want to compress a file or folder? (file/folder): ").strip().lower()
#     # choice = path.strip().lower()
#     # if choice == 'folder':
#     #     folder_to_compress = input("Enter the folder path: ").strip()
#     #     zip_output = input("Enter the output zip file path: ").strip()
#     #     compress_folder(folder_to_compress, zip_output)
#     # elif choice == 'file':

#     print(rts,"///////////++++++++))))))))))))))00000000000000000")

#     file_to_compress = path.strip()
#     zip_output = ("sample.zip").strip()
#     compress_file(file_to_compress, zip_output)
#     # else:
#     #     print("Invalid choice. Please enter 'file' or 'folder'.")
    
#     # Split the zip file into 2 parts
#     # split_choice = input("Do you want to split the zip file into 2 equal parts? (yes/no): ").strip().lower()
#     # if split_choice == 'yes':
#     zip_file_to_split = zip_output.strip()
#     split_zip_file(zip_file_to_split)
    
#     # Share the parts
#     part1 = f"{zip_file_to_split}.part1"
#     part2 = f"{zip_file_to_split}.part2"
    
#     # Details for Computer 1
#     computer_name1="DESKTOP-SJA5CTD"
#     computer1_shared_folder = r"\\DESKTOP-SJA5CTD\Files_Share"
    
#     #OR
#     # computer1_shared_folder = r"\\192.168.241.68\Files_Share"

#     computer1_username = r"desktop-sja5ctd\riss thrissur"
#     #OR
#     # computer1_username = r"192.168.241.68\riss thrissur"
#     computer1_password = r"Riss@2024"
    
#     # Details for Computer 2
#     computer_name2="LAPTOP-DHJ7HU3E"
#     computer2_shared_folder = r"\\LAPTOP-DHJ7HU3E\Files_Share" 
#     #OR
#     # computer2_shared_folder = r"\\192.168.241.239\\Files_Share"
#     computer2_username = r"laptop-dhj7hu3e\USER"
#     #OR
#     # computer2_username = r"192.168.241.239\laptop-dhj7hu3e"
#     computer2_password = r"25112003"
    
#     # Share part1 to Computer 1
#     print("\nSharing Part 1 to Computer 1...")
#     shp1=share_file(part1, computer1_shared_folder, computer1_username, computer1_password,computer_name1)
    
#     # Share part2 to Computer 2
#     print("\nSharing Part 2 to Computer 2...")
#     shp2=share_file(part2, computer2_shared_folder, computer2_username, computer2_password,computer_name2)



#     # Delete the parts after merging
#     print("\nDeleting Zip File, Part 1 and Part 2 from local system...")
#     delete_file(zip_file_to_split)
#     delete_file(part1)
#     delete_file(part2)

#     return shp1,shp2



# def upload_file(path, rts, title):
#     print(rts, "///////////++++++++))))))))))))))00000000000000000")

#     file_to_compress = path.strip()
#     zip_output = f"{title}.zip".strip()  # Using the title parameter to create zip filename
#     compress_file(file_to_compress, zip_output)

#     # Get system details from the provided data
#     computer1 = rts[0]  # First system
#     computer2 = rts[1]  # Second system

#     # Details for Computer 1
#     computer_name1 = computer1['system_name']
#     computer1_shared_folder = rf"\\{computer1['system_name']}\{computer1['file_name']}"
#     computer1_username = computer1['system_user_name']
#     computer1_password = computer1['system_password']

#     # Details for Computer 2
#     computer_name2 = computer2['system_name']
#     computer2_shared_folder = rf"\\{computer2['system_name']}\{computer2['file_name']}"
#     computer2_username = computer2['system_user_name']
#     computer2_password = computer2['system_password']

#     zip_file_to_split = zip_output.strip()
#     split_zip_file(zip_file_to_split)

#     # Share the parts
#     part1 = f"{zip_file_to_split}.part1"
#     part2 = f"{zip_file_to_split}.part2"

#     # Share part1 to Computer 1
#     print("\nSharing Part 1 to Computer 1...")
#     shp1 = share_file(part1, computer1_shared_folder, computer1_username, computer1_password, computer_name1)

#     # Share part2 to Computer 2
#     print("\nSharing Part 2 to Computer 2...")
#     shp2 = share_file(part2, computer2_shared_folder, computer2_username, computer2_password, computer_name2)

#     # Delete the parts after merging
#     print("\nDeleting Zip File, Part 1 and Part 2 from local system...")
#     delete_file(zip_file_to_split)
#     delete_file(part1)
#     delete_file(part2)

#     return shp1, shp2


import os
import shutil
import subprocess
import zipfile


def compress_folder(folder_path, output_path):
    """
    Compress a folder into a zip file.
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(f"Folder compressed into: {output_path}")

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
    part_size = file_size // 2  # Divide file size by 2
    
    with open(zip_file_path, 'rb') as f:
        for part_num in range(1, 3):
            part_path = f"{zip_file_path}.part{part_num}"
            with open(part_path, 'wb') as part_file:
                # Write the appropriate amount of bytes (part_size)
                if part_num == 2:  # Write all remaining data to the last part
                    part_file.write(f.read())
                else:
                    part_file.write(f.read(part_size))
            print(f"Created: {part_path}")


def share_file(file_to_share, target_path, username, password, computer_name):
    """
    Share a file to a specified network path with improved error handling.
    """
    try:
        # Format the network command based on password presence
        map_command = (
            f'net use Z: "{target_path}" /user:"{username}"'
            if password == ""
            else f'net use Z: "{target_path}" /user:"{username}" "{password}"'
        )

        # First ensure Z: drive is disconnected
        print("Cleaning up any existing Z: drive mapping...")
        subprocess.run('net use Z: /delete', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Try to connect to the network share
        print(f"Executing: {map_command}")
        result = subprocess.run(map_command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Failed to map network drive: {result.stderr}")
        
        # Verify the drive is mapped
        if not os.path.exists('Z:'):
            raise Exception("Z: drive not found after mapping")
            
        # Copy the file to the shared folder
        destination_path = os.path.join("Z:\\", os.path.basename(file_to_share))
        
        # Verify source file exists
        if not os.path.exists(file_to_share):
            raise Exception(f"Source file not found: {file_to_share}")
            
        # Copy with verification
        shutil.copy2(file_to_share, destination_path)
        
        # Verify the file was copied successfully
        if not os.path.exists(destination_path):
            raise Exception("File was not copied to destination")
            
        # Verify file sizes match
        if os.path.getsize(file_to_share) != os.path.getsize(destination_path):
            raise Exception("Copied file size does not match source file")
        
        print(f"File '{file_to_share}' successfully copied to {destination_path}")
        print(f"File saved on {computer_name} at: {target_path}\\{os.path.basename(file_to_share)}")
        
    except Exception as e:
        print(f"Error during file sharing: {str(e)}")
        raise
        
    finally:
        try:
            # Always try to disconnect the drive in the finally block
            print("Disconnecting Z: drive...")
            subprocess.run('net use Z: /delete', shell=True, check=True)
            print("Z: drive disconnected successfully")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not disconnect Z: drive: {e}")
    
    return (os.path.basename(file_to_share), computer_name, target_path)
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
    # Example usage
    # Compress the file or folder
def upload_file(path,rts):  
    # choice = input("Do you want to compress a file or folder? (file/folder): ").strip().lower()
    # choice = path.strip().lower()
    # if choice == 'folder':
    #     folder_to_compress = input("Enter the folder path: ").strip()
    #     zip_output = input("Enter the output zip file path: ").strip()
    #     compress_folder(folder_to_compress, zip_output)
    # elif choice == 'file':

    print(rts,"///////////++++++++))))))))))))))00000000000000000")

    file_to_compress = path.strip()
    zip_output = ("sample.zip").strip()
    compress_file(file_to_compress, zip_output)
    # else:
    #     print("Invalid choice. Please enter 'file' or 'folder'.")
    
    # Split the zip file into 2 parts
    # split_choice = input("Do you want to split the zip file into 2 equal parts? (yes/no): ").strip().lower()
    # if split_choice == 'yes':
    zip_file_to_split = zip_output.strip()
    split_zip_file(zip_file_to_split)
    
    # Share the parts
    part1 = f"{zip_file_to_split}.part1"
    part2 = f"{zip_file_to_split}.part2"
    
    # Details for Computer 1
    computer_name1="DESKTOP-SJA5CTD"
    computer1_shared_folder = r"\\DESKTOP-SJA5CTD\Files_Share"
    
    #OR
    # computer1_shared_folder = r"\\192.168.241.68\Files_Share"

    computer1_username = r"desktop-sja5ctd\riss thrissur"
    #OR
    # computer1_username = r"192.168.241.68\riss thrissur"
    computer1_password = r"Riss@2024"
    
    # Details for Computer 2
    computer_name2="LAPTOP-DHJ7HU3E"
    computer2_shared_folder = r"\\LAPTOP-DHJ7HU3E\Files_Share" 
    #OR
    # computer2_shared_folder = r"\\192.168.241.239\\Files_Share"
    computer2_username = r"laptop-dhj7hu3e\USER"
    #OR
    # computer2_username = r"192.168.241.239\laptop-dhj7hu3e"
    computer2_password = r"25112003"
    
    # Share part1 to Computer 1
    print("\nSharing Part 1 to Computer 1...")
    shp1=share_file(part1, computer1_shared_folder, computer1_username, computer1_password,computer_name1)
    
    # Share part2 to Computer 2
    print("\nSharing Part 2 to Computer 2...")
    shp2=share_file(part2, computer2_shared_folder, computer2_username, computer2_password,computer_name2)



    # Delete the parts after merging
    print("\nDeleting Zip File, Part 1 and Part 2 from local system...")
    delete_file(zip_file_to_split)
    delete_file(part1)
    delete_file(part2)

    return shp1,shp2



def upload_file(path, rts, title):
    print(rts, "///////////++++++++))))))))))))))00000000000000000")

    file_to_compress = path.strip()
    zip_output = f"{title}.zip".strip()  # Using the title parameter to create zip filename
    compress_file(file_to_compress, zip_output)

    # Get system details from the provided data
    computer1 = rts[0]  # First system
    computer2 = rts[1]  # Second system

    # Details for Computer 1
    computer_name1 = computer1['system_name']
    computer1_shared_folder = rf"\\{computer1['system_name']}\{computer1['file_name']}"
    computer1_username = computer1['system_user_name']
    computer1_password = computer1['system_password']

    # Details for Computer 2
    computer_name2 = computer2['system_name']
    computer2_shared_folder = rf"\\{computer2['system_name']}\{computer2['file_name']}"
    computer2_username = computer2['system_user_name']
    computer2_password = computer2['system_password']

    zip_file_to_split = zip_output.strip()
    split_zip_file(zip_file_to_split)

    # Share the parts
    part1 = f"{zip_file_to_split}.part1"
    part2 = f"{zip_file_to_split}.part2"

    # Share part1 to Computer 1
    print("\nSharing Part 1 to Computer 1...")
    shp1 = share_file(part1, computer1_shared_folder, computer1_username, computer1_password, computer_name1)

    # Share part2 to Computer 2
    print("\nSharing Part 2 to Computer 2...")
    shp2 = share_file(part2, computer2_shared_folder, computer2_username, computer2_password, computer_name2)

    # Delete the parts after merging
    print("\nDeleting Zip File, Part 1 and Part 2 from local system...")
    delete_file(zip_file_to_split)
    delete_file(part1)
    delete_file(part2)

    return shp1, shp2






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
