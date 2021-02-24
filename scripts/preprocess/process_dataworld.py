from os import mkdir, listdir, rename
from os.path import join, isfile, exists
import zipfile
from shutil import copy, rmtree


def extract_zip_file(src, zip_file, dest, index):
    path_to_zip_file = join(src, zip_file)
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(join(dest, "temp"+str(index)))

def copy_files(dest, index):

    my_path = join(dest, "temp{0}".format(index))
    data_path = [f for f in listdir(my_path)][0]
    metadata_path = join(my_path, data_path)
    data_path = join(my_path, data_path, "data")

    root_dir = join(dest, str(index))
    if not exists(root_dir):
        mkdir(root_dir)

    error = False
    try:
        csv_lst = [f for f in listdir(data_path) if isfile(join(data_path, f)) and f.find("csv") > 0]
        for i, csv in zip(range(len(csv_lst)), csv_lst):
            dest_file_name = 'Data_{0}{1}.csv'.format(i, index)
            print(dest_file_name)
            copy(join(data_path, csv), join(root_dir, dest_file_name))
    except Exception as ex:
        error = True
        print("temp{0} has no CSV".format(index))

    try:
        json_lst = [f for f in listdir(metadata_path) if isfile(join(metadata_path, f)) and f.find("json") > 0]
        for i, _json in zip(range(len(json_lst)), json_lst):
            dest_file_name = 'Metadata_{0}{1}.json'.format(i, index)
            print(dest_file_name)
            copy(join(metadata_path, _json), join(root_dir, dest_file_name))
    except:
        error = True
        print("temp{0} has no JSON".format(index))

    if not error:
        rmtree(my_path)


if __name__ == '__main__':
    src = r"\data.world\original"
    dest = r"\data.world\processed"

    src_files = [f for f in listdir(src) if isfile(join(src, f))]
    print(len(src_files))

    for i, zip_file in zip(range(len(src_files)), src_files):
        extract_zip_file(src, zip_file, dest, i+1)
        copy_files(dest, i+1)


