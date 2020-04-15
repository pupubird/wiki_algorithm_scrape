import requests
import bs4


def main(url):
    url = url.strip()
    html = requests.get(url)
    content = html.content.decode('utf-8')
    soup = bs4.BeautifulSoup(content, 'html.parser')
    lis = soup.findAll('li')
    res = list()
    for li in lis:
        a_tag_children = li.findChildren('a')
        for a_tag in a_tag_children:
            if not a_tag.get('href', False):
                continue
            a_attr = a_tag['href']
            if "#" in a_attr:
                continue
            # if https:// exists, means its going out of wikipedia
            if '/wiki/' in a_attr and 'http://' not in a_attr and 'https://' not in a_attr:
                parent = li.parent
                while parent:
                    if parent.get('id', False) and a_tag.get('title', False):
                        title = a_tag['title'].lower()
                        if parent['id'] == 'mw-content-text' and 'list of' not in title:
                            res.append(str(a_attr)+'\n')
                            break
                    parent = parent.parent

    # cleaning
    res = set(res)
    title = 'wiki_links'
    try:
        with open(f'{title}.txt', 'r', encoding='utf-8') as f:
            ori_lines = set(f.readlines())
            for item in res:
                ori_lines.add(item)
            with open(f'{title}.txt', 'w', encoding="utf-8") as g:
                g.writelines(ori_lines)
    except FileNotFoundError:
        with open(f'{title}.txt', 'w', encoding="utf-8") as f:
            f.writelines(res)

    return


if __name__ == "__main__":
    res = main()
