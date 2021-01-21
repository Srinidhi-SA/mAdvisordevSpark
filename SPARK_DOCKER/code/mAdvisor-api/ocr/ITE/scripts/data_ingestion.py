import os
import random
import shutil
import uuid
from pdf2image import convert_from_path


def random_folder_generator():
    return str(uuid.uuid1())


def ingestion_1(file_full_path, path):
    """
    function for converting pdf to png or jpg

    inputs:
        file_full_path:path of the file to process
        path:the path to which the image has to be stored

    output:
        converted images in pdf_to_images_folder inside the path

    if pdf contains multiples pages,individual pages will be stored with the following naming convention
    pdf_file_name+page number

    """

    try:
        os.makedirs(path)
    except FileExistsError:
        print('Path already exists!')

    filename, file_extension = os.path.splitext(file_full_path)
    print("ingestion module running")

    folder_name = random_folder_generator()
    os.makedirs(os.path.join('ocr/ITE/pdf_to_images_folder', folder_name))
    if file_extension:
        if file_extension == ".pdf":
            pages = convert_from_path(file_full_path)
            index = 1
            for page in pages:
                # page.save(path + "/" + filename.split("/")[-1] + '_page_' + str(index) + '.jpg', 'JPEG')
                page.save(
                    os.path.join(path, folder_name, '{}_page_{}.jpg'.format(filename.split("/")[-1], str(index))),
                    'JPEG')
                index = index + 1
            return os.path.join(path, folder_name), file_extension, filename

        elif file_extension in [".jpg", ".png", ".jpeg", ".JPG", ".PNG", "JPEG"]:
            shutil.copy(file_full_path, path)
            print("no conversion needed")
            return os.path.join(path, file_full_path), file_extension, filename

    else:
        for i in os.listdir(file_full_path):

            filename, file_extension = os.path.splitext(i)
            if file_extension == ".pdf":
                pages = convert_from_path(os.path.join(file_full_path, i))
                index = 1
                for page in pages:
                    # page.save(path + "/" + filename.split("/")[-1] + '_page_' + str(index) + '.jpg', 'JPEG')
                    page.save(os.path.join(path, folder_name, '{}_page_{}.jpg'.format(filename.split("/")[-1],
                                                                                      str(index))),
                              'JPEG')
                    index = index + 1
                return os.path.join(path, folder_name), file_extension, filename

            elif file_extension == ".jpg" or file_extension == ".png" or file_extension == ".jpeg":
                shutil.copy(file_full_path + "/" + i, path)
                print("no conversion needed")
                return os.path.join(path, file_full_path), file_extension, filename
