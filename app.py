import save_contents
import scrape
import get_contents

links = []
with open('list_of_algorithms_link.txt', 'r') as f:
    links = f.readlines()

for link in links:
    scrape.main(link)
save_contents.main()
get_contents.main()
