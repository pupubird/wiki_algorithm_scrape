import requests
import bs4
import re
import csv
import time

current = 0


def main():
    csv_outputs_list = []
    with open('wiki_links.txt', 'r') as f:
        lines = f.readlines()
        outputs = start_thread(0, len(lines), lines)
        csv_outputs_list = outputs
    save(csv_outputs_list)


def start_thread(from_amount, to_amount, lines):
    outputs = []
    for i in range(from_amount, to_amount):
        outputs, header, content, url = get_content(
            outputs, lines[i], i, len(lines))
        outputs.append((header, content, url))
    return outputs


def get_content(outputs, line, i, leng):
    global current
    line = line.strip()
    url = f"https://en.wikipedia.org{line}"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    header = soup.find('h1', {'id': 'firstHeading'}).getText()
    contents = soup.findAll('p')
    content = ''
    for p in contents:
        text = p.getText()
        if text.strip() != '':
            content = text
            break
    content = clean_text(content)
    current += 1
    print(f"\nAppending: {header} \nleft: {current}/{leng}\n")
    # print("sleep for 5 seconds...")
    # time.sleep(5)
    return outputs, header, content, url


def clean_text(text):
    # clean citation like: [1]
    text = re.sub('\[\w{1,}\]', '', text)

    # clean ending like "See examples below: " at the end of the string
    text = re.sub('\.{1}[^.]{1,}:$', '.', text)

    # Strip
    text = text.replace("\n", '')

    # remove all {\displaystyle} with , and .
    text = re.sub('{\\\\displaystyle [^.,]{1,}}', '', text)

    # remove all {\displaystyle} with . (in case of decimal points)
    text = re.sub('{\\\\displaystyle [^,]{1,}}', '', text)
    return text


def save(outputs):
    # [(header,content),(header,content)]
    print("Saving..")
    try:
        with open('output.csv', 'r', encoding='utf-8') as f:
            current_rows = csv.reader(f)
            rows = [row for row in current_rows] + outputs
            with open('output.csv', 'w', encoding='utf-8') as g:
                csv_writer = csv.writer(g)
                rows = [row for row in rows if row != []]
                csv_writer.writerows(rows)
                print("Done")
    except FileNotFoundError:
        with open('output.csv', 'w', encoding='utf-8') as g:
            csv_writer = csv.writer(g)
            csv_writer.writerow(['header', 'content', 'url'])
            rows = [row for row in outputs if row != []]
            csv_writer.writerows(rows)
            print("Done")
