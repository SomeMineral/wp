
import os


lang = ['vietnamese', 'korean', 'english', 'chinese', 'french', 'spanish', 'japanese', 'russian', 'lao', 'khmer']
language = lang[9]

article_box = './{}_article'.format(language)
with open('article_{}.txt'.format(language), 'w', encoding='utf-8') as article:
    for part_path in os.listdir(article_box):
        path = '{0}/{1}'.format(article_box, part_path)
        with open(path, 'r', encoding='utf-8') as part:
            for idx, line in enumerate(part):
                if idx < 2:
                    continue
                line = line.replace('\n', '').strip()
                if line == '':
                    continue
                else:
                    article.write('{}\n'.format(line))
            print('{}_completed'.format(path))

print('complete all')
