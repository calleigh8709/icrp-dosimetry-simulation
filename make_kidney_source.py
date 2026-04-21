import SimpleITK as sitk
import numpy as np

# 팬텀 이미지 읽기
img = sitk.ReadImage('/Users/hyesujeon/opengate_sim/AF_P.hdr')
arr = sitk.GetArrayFromImage(img)

# 신장 인덱스만 추출 (89~94)
kidney_mask = np.zeros_like(arr, dtype=np.float32)
kidney_mask[(arr >= 89) & (arr <= 94)] = 1.0

# 저장
out = sitk.GetImageFromArray(kidney_mask)
out.CopyInformation(img)
sitk.WriteImage(out, '/Users/hyesujeon/opengate_sim/kidney_source.mhd')
print('신장 복셀 수:', (kidney_mask > 0).sum())
