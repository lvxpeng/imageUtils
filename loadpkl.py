import pickle
import numpy as np
import nibabel as nb
import os

def load_pkl(path):
    with open(path, 'rb') as f:
        return pickle.load(f)



def save_as_nii(img, label, number, img_path, label_path):
    number = int(number)
    new_img = nb.nifti1.Nifti1Image(img, None)
    new_label = nb.nifti1.Nifti1Image(label, None)
    img_name = f'{number:03d}_IXI_norm.nii.gz'
    label_name = f'{number:03d}_IXI_norm_seg.nii.gz'
    nb.save(new_label, os.path.join(label_path, label_name))
    nb.save(new_img, os.path.join(img_path, img_name))

def select_img_label(path, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    data_path = os.path.join(path)
    save_img_path = os.path.join(save_path, 'norm')
    save_label_path = os.path.join(save_path, 'norm_seg')
    if not os.path.exists(save_img_path):
        os.makedirs(save_img_path)
    elif not os.path.exists(save_label_path):
        os.makedirs(save_label_path)

    for i, file in enumerate(os.listdir(data_path)):
        if file.endswith('.pkl'):
            file_path = os.path.join(data_path, file)
            img, label = load_pkl(os.path.join(file_path))
            save_as_nii(img, label, i+1, save_img_path, save_label_path)
    print('saved {} imgs and labels'.format(i))


if __name__ == '__main__':
    path = 'D:/idmdownload/IXI_data/Train/'
    save_path = 'D:/temp/sav/'
    select_img_label(path, save_path)