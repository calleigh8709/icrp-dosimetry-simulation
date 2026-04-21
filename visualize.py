import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

# 선량 이미지
dose_img = sitk.ReadImage('/Users/hyesujeon/opengate_sim/output/doseoutput_dose.mhd')
dose = sitk.GetArrayFromImage(dose_img)

# 팬텀 이미지
phantom_img = sitk.ReadImage('/Users/hyesujeon/opengate_sim/AF_P.hdr')
phantom = sitk.GetArrayFromImage(phantom_img)

print('Dose shape:', dose.shape)
print('Max dose:', dose.max())
print('Non-zero voxels:', (dose > 0).sum())

# 신장 위치 찾기 (인덱스 89~94)
kidney = (phantom >= 89) & (phantom <= 94)
kidney_slices = np.where(kidney.any(axis=(1,2)))[0]
print('신장 슬라이스 범위:', kidney_slices.min(), '~', kidney_slices.max())
mid_slice = kidney_slices.mean().astype(int)

# 시각화 - 팬텀 + 선량 오버레이
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 왼쪽: 팬텀
axes[0].imshow(phantom[mid_slice], cmap='gray')
axes[0].contour(kidney[mid_slice], colors='red', linewidths=1)
axes[0].set_title(f'Phantom (slice {mid_slice}) - 빨간선=신장')

# 오른쪽: 선량
dose_slice = dose[mid_slice]
vmax = np.percentile(dose[dose > 0], 99) if (dose > 0).sum() > 0 else 1
im = axes[1].imshow(dose_slice, cmap='hot', vmin=0, vmax=vmax)
axes[1].contour(kidney[mid_slice], colors='cyan', linewidths=1)
plt.colorbar(im, ax=axes[1], label='Dose (Gy)')
axes[1].set_title('Dose Distribution - 청록선=신장')

plt.tight_layout()
plt.savefig('/Users/hyesujeon/opengate_sim/output/dose_map.png', dpi=150)
print('저장 완료!')
