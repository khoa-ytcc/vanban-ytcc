import subprocess
import re
import sys

def main():
    try:
        diff = subprocess.check_output(['git', 'diff', '--cached', '-U0'], encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"Lỗi đọc git diff: {e}")
        sys.exit(1)

    leaks = []
    added_lines = [line[1:] for line in diff.splitlines() if line.startswith('+') and not line.startswith('+++')]

    patterns = [
        (r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', 'IP address pattern'),
        (r'password\s*[:=]\s*["\'](?![$%])[^"\']{3,}["\']', 'Hardcoded password literal'),
        (r'pwd\s*[:=]\s*["\'](?![$%])[^"\']{3,}["\']', 'Hardcoded pwd literal')
    ]

    for idx, line in enumerate(added_lines, 1):
        for pat, desc in patterns:
            # Loại trừ các chuỗi version ví dụ 3.8.0, 2.5.0 hoặc doc_schema 2.5
            if pat == r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b':
                # Kiểm tra IP thực tế (4 octets)
                m = re.search(r'\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b', line)
                if m:
                    octets = [int(x) for x in m.groups()]
                    if all(0 <= o <= 255 for o in octets):
                        leaks.append((idx, desc, line.strip()))
            else:
                if re.search(pat, line, re.IGNORECASE):
                    leaks.append((idx, desc, line.strip()))

    if leaks:
        print(f"❌ CẢNH BÁO: Phát hiện {len(leaks)} dòng nghi vấn rò rỉ:")
        for item in leaks:
            print(f"Dòng {item[0]} [{item[1]}]: {item[2]}")
        sys.exit(1)
    else:
        print("✅ AN TOÀN TUYỆT ĐỐI: 0 dòng thêm mới nào chứa IP, mật khẩu hay bí mật CSDL!")
        sys.exit(0)

if __name__ == '__main__':
    main()
