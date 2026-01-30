import ftplib
import os
import sys

# Configuration
FTP_HOST = "192.168.2.16"
FTP_USER = "anonymous" # Change if auth is required
FTP_PASS = "anonymous@"
START_PATH = "/public/"

def get_indent(level):
    return "    " * level

def traverse_ftp(ftp, path, level=0):
    """
    Recursively traverses an FTP directory and prints the structure.
    """
    # Print current directory name
    dir_name = os.path.basename(path.rstrip('/'))
    if not dir_name:
        dir_name = path
    
    print(f"{get_indent(level)}[{dir_name}]")

    try:
        ftp.cwd(path)
    except ftplib.error_perm as e:
        print(f"{get_indent(level+1)}<Error: Could not enter directory: {e}>")
        return

    # Get list of files/directories
    try:
        # Try MLSD first for better parsing if supported
        items = list(ftp.mlsd())
        items.sort(key=lambda x: x[0])
        
        for name, facts in items:
            if name in ['.', '..']:
                continue
            
            if facts['type'] == 'dir':
                traverse_ftp(ftp, name, level + 1)
            else:
                print(f"{get_indent(level+1)}{name}")
                
    except ftplib.error_perm:
        # Fallback to NLST if MLSD is not supported
        try:
            files = ftp.nlst()
            files.sort()
            
            for name in files:
                if name in ['.', '..']:
                    continue
                
                # Heuristic: Try to CWD to see if it's a directory
                current_cwd = ftp.pwd()
                try:
                    ftp.cwd(name)
                    # It's a directory, recurse
                    ftp.cwd(current_cwd) # Go back
                    traverse_ftp(ftp, name, level + 1)
                except ftplib.error_perm:
                    # Likely a file
                    print(f"{get_indent(level+1)}{name}")
        except ftplib.error_perm as e:
             print(f"{get_indent(level+1)}<Error listing content: {e}>")

    # Return to parent directory after finishing this level
    if level > 0:
        ftp.cwd('..')

def main():
    print(f"Connecting to {FTP_HOST}...")
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        # Force UTF-8 encoding if possible
        ftp.encoding = "utf-8"
        
        print(f"Connected. Starting crawl from '{START_PATH}'...\n")
        
        # Start traversal
        traverse_ftp(ftp, START_PATH)
        
        ftp.quit()
        print("\nDone.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
