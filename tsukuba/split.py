import os

# 기본 설정
numOfLine = 300000
word_type = 'na_keiyoushi'
path_form = f'new/{word_type}/{word_type}'+'_{0:0>4}.txt'
start_num = 1

# 반복 시작
for file_name in os.listdir('.'):
    if '.txt' not in file_name:
        continue

    print(file_name)
    source_file = open(file_name, 'r', encoding='utf-8')

    for file_count in range(start_num, 5000):
        line_count = 0  # 하나의 텍스트 파일에 몇 줄이나 쓸 지 세기 위해 초기화
        print(path_form.format(file_count))

        with open(path_form.format(file_count), 'w', encoding='utf-8') as sf:
            for line_count, line in enumerate(source_file, start=1):
                sf.write(line)
                if line_count == numOfLine: # 설정한 개수만큼 채워지면 그만 쓰기.
                    break

        if line_count < numOfLine: # 텍스트 파일 하나 채웠는데 개수가 설정치에 못미친다는 건 끝났단 의미.
            start_num = file_count + 1  # 다음 번호로 시작.
            break
