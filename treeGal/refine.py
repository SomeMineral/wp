import time

tree_text = open('whole_main_text.txt', 'r', encoding='utf-8')

modified_text = open('modified_main_text.txt', 'w', encoding='utf-8')

cnt = 0

for line in tree_text:
    cnt += 1
    temp = line.replace('==========', '')
    temp = temp.replace('From dcinside app for Android & the_Wiiumm', '')
    temp = temp.replace('From dcinside app for Android', '')
    temp = temp.replace('DCInside for iPhone', '')
    temp = temp.replace('From DC Wave', '')
    temp = temp.replace('- dc official App', '')
    temp = temp.replace('dc official App', '')
    temp = temp.replace('- dc App', '')
    temp = temp.replace('- dc app', '')
    temp = temp.replace('dc App', '')
    temp = temp.replace('- dc official', '')
    temp = temp.replace('dc official', '')
    temp = temp.replace('- dc', '')
    temp = temp.replace('- DCW', '')
    temp = temp.strip()
    temp = temp.replace('\n', '')
    temp = temp.replace('\t', '')
    temp = temp.replace('\r', '')

    if temp in ['', ' ', '\n', '\t', '\r']:
        continue

    modified_text.write(f"{temp}\n")

    if cnt % 1000 == 0:
        print(f"{cnt}개 완료")
        time.sleep(0.5)

tree_text.close()
modified_text.close()

print("종료")