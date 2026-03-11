# SMPL 版本说明（cam00_full/sv1p）

本目录保留了 4 组基于原始 `smpl/` 的对比版本：

- `smpl1/`  
  - 改动：将所有帧的 `Rh` 固定为 `000000.json` 的 `Rh`。  
  - 对应渲染：`render_smpl1/`，视频 `render_smpl1.mp4`。

- `smpl2/`  
  - 改动：将所有帧的 `Rh` 和 `Th` 都固定为 `000000.json` 的值。  
  - 对应渲染：`render_smpl2/`，视频 `render_smpl2.mp4`。

- `smpl3/`  
  - 改动：仅将所有帧的 `Th` 固定为 `000000.json` 的值，`Rh` 保持原始逐帧结果。  
  - 对应渲染：`render_smpl3/`，视频 `render_smpl3.mp4`。

- `smpl4/`  
  - 改动：做时序平滑（非固定）：
    - `Rh`：时间窗口 9 帧均值平滑
    - `Th`：时间窗口 9 帧均值平滑
    - `poses`：时间窗口 7 帧均值平滑
    - `shapes`：全序列均值
  - 对应渲染：`render_smpl4/`，视频 `render_smpl4.mp4`（测试快速版：前 600 帧，640x360，约 20 秒，低码率）。

- `smpl5/`  
  - 改动：将所有帧 `shapes` 固定替换为指定 10 维常量向量（你提供的数值）。  
  - 对应渲染：`render_smpl5/`，视频 `render_smpl5.mp4`（测试快速版：前 600 帧，640x360，约 20 秒，低码率）。

- `smpl401/`  
  - 改动：使用 `smpl4`（时序平滑版）作为输入，不改 json，仅重新做高画质短时渲染。  
  - 对应渲染：`render_smpl401/`，视频 `render_smpl401.mp4`（前 900 帧，30 秒，1280x720，高码率）。

原始未改动结果：

- `smpl/` + `render/` + `render.mp4`
