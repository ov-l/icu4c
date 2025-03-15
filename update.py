
# update from icu/icu4c directory
# - The `common` folder
# - `scriptset.*`, `ucln_in.*`, `uspoof.cpp"` and `uspoof_impl.cpp` from the `i18n` folder
# - `uspoof.h` from the `i18n/unicode` folder
# - `LICENSE` file 

import os
import shutil
import sys



def download_icu4c(version):
    # Create a temp directory and change to temp directory
    os.makedirs('temp', exist_ok=True)
    os.chdir('temp')    
    dash_version = version.replace('.', '-')
    uscore_version = version.replace('.', '_')
    major_version = version.split('.')[0]
    
    url = f'https://github.com/unicode-org/icu/releases/download/release-{dash_version}/icu4c-{uscore_version}-src.tgz'
    os.system(f'wget {url}')
    os.system(f'tar -xzf icu4c-{uscore_version}-src.tgz')
    data_url = f'https://github.com/unicode-org/icu/releases/download/release-{dash_version}/icu4c-{uscore_version}-data.zip'
    os.system(f'wget {data_url}')
    os.system(f'unzip icu4c-{uscore_version}-data.zip')
    # Copy data from the unzipped data folder to icu4c/source/data folder and overwrite all existing data files
    os.system(f'cp -r data/* icu/source/data/')
    # runCOnfigureICU
    os.system(f'./icu/source/runConfigureICU Linux')
    os.system(f'make')
    os.system(f'ICU_DATA_FILTER_FILE=../u_data.json ./icu/source/runConfigureICU Linux --with-data-packaging=common')
    os.system(f'rm -rf ./data/out')
    os.system(f'make')
    os.system(f'cp -r ./data/out/icudt{major_version}l.dat ../')
    os.system('cd ..')


# Create list of files to copy
files = ['i18n/scriptset.cpp', 
         'i18n/scriptset.h', 
         'i18n/ucln_in.cpp', 
         'i18n/ucln_in.h', 
         'i18n/uspoof.cpp', 
         'i18n/uspoof_impl.h',
         'i18n/uspoof_impl.cpp',
         'i18n/unicode/uspoof.h']

def update_icu4c(icu4c_dir, output_dir):
    common_dir = os.path.join(icu4c_dir, 'common')
    i18n_dir = os.path.join(icu4c_dir, 'i18n')
    unicode_dir = os.path.join(i18n_dir, 'unicode')

    output_common_dir = os.path.join(output_dir, 'common')
    output_i18n_dir = os.path.join(output_dir, 'i18n')
    output_unicode_dir = os.path.join(output_i18n_dir, 'unicode')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Copy tree, but update the destination if it already exists
    
    shutil.copytree(common_dir, output_common_dir, dirs_exist_ok=True)

    os.makedirs(output_i18n_dir, exist_ok=True)

    os.makedirs(output_unicode_dir, exist_ok=True)

    for file in files:
        dest_file = os.path.join(output_dir, file)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy(os.path.join(icu4c_dir, file), dest_file)

    shutil.copy(os.path.join(icu4c_dir, '..', 'LICENSE'), output_dir)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python update.py <version>')
        sys.exit(1)

    version = sys.argv[1]

    output_dir = os.getcwd()
    icu4c_dir = f'{output_dir}/temp/icu/source'

    download_icu4c(version)

    if not os.path.exists(icu4c_dir):
        print(f'Error: {icu4c_dir} does not exist')
        sys.exit(1)
    
    update_icu4c(icu4c_dir, output_dir)

    os.system('rm -rf temp')

    print('Done updating ICU4C')
