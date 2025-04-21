Cải tiến: bây giờ chỉ có người win nhấn v trước thì mới reset k lỗi, người thua mà nhấn v trước là toang

Animation:
1: Vào https://www.mixamo.com/ chọn character rồi chọn animation -> tích In Place để animation nó chạy im 1 chỗ -> tải về (để option mặc định, k thay đổi gì cả)

2: Import vào Blender3D, xóa mấy cái k cần thiết đi, giữ lại cái import.

3: Nhấn shift f12 để mở ra màn hình mà góc trên bên trái có chữ "Dope Sheet"

4: Click vào cái dropdown "Dope Sheet" -> Chọn Action Editor

5: Chọn Animation cần đặt tên (cho nó hiện lên màu cam) -> đổi tên ở thanh công cụ ngang hàng với "Action Editor" (bên trái icon cái khiên) -> Enter

6: Chỉnh lại scale xyz cho phù hợp

7: Xuất ra glb/gltf, tùy chọn mặc định là oke thì phải

    ChatGpt chỉ: 
    
      "Trong lúc Export glTF, chọn:
      
      Format: glTF Separate (.gltf + .bin + textures)
      
      Check:
      
      ✅ Animation
      
      ✅ Shape Keys (nếu có)
      
      ✅ Sampling Animations
      
      Animation Mode: Actions
      
      Nếu bạn có nhiều hành động (Action), nên export từng cái một hoặc để Blender merge đúng cách."
      
  8: lúc dùng trong code nhớ gõ đúng tên animation, ví dụ: self.running_actor.loop('running')

# Cách chạy game (Tạm thời)

# Bước 1: Clone project

# Bước 2: Tại thư mục gốc của project chạy lệnh:
  python -m venv .venv
-> Để tạo .venv

# Bước 3: Chạy lệnh .venv\Scripts\Activate.ps1

# Bước 4: Chạy lệnh: pip install -r requirements.txt
-> Để cài thư viện

# Bước 5: Chạy file StartServer.py 

# Bước 6: Chạy file StartClient.py


