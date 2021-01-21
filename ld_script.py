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
    df['FIPS'] = df.GEO_ID.apply(lambda x: x.split('US')[1] if len(x) > 3 else '_fips')
    df["STATEFP"] = df.GEO_ID.apply(lambda x: x.split('US')[1][:2] if len(x) > 3 else '_statefp')
    df["COUNTYFP"] = df.GEO_ID.apply(lambda x: x.split('US')[1][2:5] if len(x) > 3 else '_countyfp')
    df["TRACTCE"] = df.GEO_ID.apply(lambda x: x.split('US')[1][5:] if len(x) > 3 else '_tractce')
    return df    

def merge_columns_by_add(df, target, columns, column_dict):
    '''
    Function that merges multiple columns into one by addition. Specify an
    existing target column to collapse on. Function will attempt to rename
    the target column to reflect the merge where possible.
    
    Parameters:
        df: dataframe with columns to merge
        target: column name of target column for the merge
        columns: list of column(s) that are to be merged via addition
        column_dict: dictionary of str summaries for each column name
        
    Returns:
        df: Modified dataframe object 
    '''
    
    #Steps to update our column metadata dictionary
    str1 = column_dict[target]
    str2 = column_dict[columns[-1]] # Assumes nice sequential ordering of list
    str1_replace = str(max([int(s) for s in str1.split() if s.isdigit()]))
    str2_replace = str(max([int(s) for s in str2.split() if s.isdigit()])) 
    
    df = df.copy()
    highest_index = int(target[-3:-1]) #Assumes that these chars are ints
    target_ser = df[target].copy()
    
    try:
        columns.pop(columns.index(target))
    except: 
        ValueError
    
    for i in columns:
        
        if int(i[-3:-1]) > highest_index:
            
            highest_index = int(i[-3:-1])
        target_ser += df[i]
        
    df[target] = target_ser
    new_col_name = target[:-1] + '_' + str(highest_index) + 'E'
    column_dict[new_col_name] = str1.replace(str1_replace, str2_replace)
    column_dict.pop(target)
    for i in columns:
        column_dict.pop(i)
    df.drop(columns=columns, inplace=True)
    df.rename(columns={target:new_col_name}, inplace=True)
    return df, column_dict 

def drop_and_normalize(df1, df2):
    df1.drop(columns=['GEO_ID', 'NAME'], inplace=True)
    df2.drop(index=0, axis=0, inplace=True)
    df2.reset_index(drop=True, inplace=True)
    # Subtracting 3 to S0101_data.shape[1] to account for the our creation of 3 new columns
    assert (df1.shape[1]-4 == df2.shape[0]), print('mismatch in metadata and data correspondence')
    return df1, df2

def create_wanted_columns(df1, df2, i_list):
    wc = df2.GEO_ID.iloc[i_list].to_list()
    ac = list(df1.columns[-4:])
    wc.extend(ac)
    return wc