# Some useful scripts that I often need,


# Translates my local C directory into my wsl mnt
def win_to_lin(path: str) -> str:
    '''
    Tranlates the path to my windows C:\ drive to the 
    c mnt in my wsl ubuntu path
    
    Parameters:
        windows path string
    
    Returns:
        corresponding linux path string
    '''    
    path = path.replace('\\', '/')
    path = '/mnt/c' +  r'{}'.format(path[2:])
    return path

def census_data_search(data_dir='data', table_name=None, content_type='data'):
    import os    
    '''Simple function to return the path to specific data I want
    in this projects data folder
    
    Parameters:
        data_dir: string path to data directory, default="data"
        table_name: string for specific table I want
        content_type: data or metadata
        
    Returns:
        path to the correct file
    '''
    if content_type == 'data':
        content= '_data'
    else:
        content= '_metadata'
    
    name = table_name
        
    for f in os.listdir(data_dir):        
        if name in f:            
            for f2 in os.listdir(os.path.join(data_dir, f)):                
                if (name + content) in f2:
                    return(os.path.join(data_dir, f, f2))
    
    print("Might not have the data you are looking for")
    return

def unzip_many_files(zipped_path, unzipped_path, create_new=False):
    '''
    Function to unzip multiple zip files in a directory to another
    directory with an option to create folders to separate
    the original archive contents
    
    Parameters: 
        zipped_path: string path to location of zipped files
        unzipped_path: desired location to extract the files
        create_new: option to recreate the archive structure as folders   
    '''
    import os, zipfile
    
    for archive in os.listdir(st_zipped_path):
        archive_path = os.path.join(st_zipped_path, archive)
        new_directory = archive[:-4]
        if create_new == True:
            os.mkdir(os.path.join(st_unzipped_path, new_directory))
            new_path = os.path.join(st_unzipped_path, new_directory)
            with zipfile.ZipFile(archive_path) as zf:
                zf.extractall(new_path)
        else:
            with zipfile.ZipFile(archive_path) as zf:
                zf.extractall(st_unzipped_path)

def parse_geo_id(df):
    '''
    Function that takes the GEO_ID column of census data and parses the value to create
    4 new columns containing components of State FIPS codes.
    '''
    df['FIPS'] = df.GEO_ID.apply(lambda x: x.split('US')[1] if len(x) > 3 else 'fips')
    df["STATEFP"] = df.GEO_ID.apply(lambda x: x.split('US')[1][:2] if len(x) > 3 else 'statefp')
    df["COUNTYFP"] = df.GEO_ID.apply(lambda x: x.split('US')[1][2:5] if len(x) > 3 else 'countyfp')
    df["TRACTCE"] = df.GEO_ID.apply(lambda x: x.split('US')[1][5:] if len(x) > 3 else 'tractce')
    return df    