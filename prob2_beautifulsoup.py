import re
from bs4 import BeautifulSoup

html = """
    <html>
<head>
<title>My first web page</title>
</head>
<body>
<h1>My first web page</h1>
<h2>What this is tutorial</h2>
<p>A simple page put together using HTML. <em>I said a simple page.</em>.</p>
<ul>
 <li>To learn HTML</li>
 <li>
 To show off
 <ol>
 <li>To my boss</li>
 <li>To my friends</li>
 <li>To my cat</li>
 <li>To the little talking duck in my brain</li>
 </ol>
 </li>
 <li>Because I have fallen in love with my computer and want to give her some HTML loving.</li>
</ul>
<h2>Where to find the tutorial</h2>
<p><a href="http://www.aaa.com"><img src=http://www.aaa.com/badge1.gif></a></p>
<h3>Some random table</h3>
<table>
 <tr class="tutorial1">
 <td>Row 1, cell 1</td>
 <td>Row 1, cell 2<img src=http://www.bbb.com/badge2.gif></td>
 <td>Row 1, cell 3</td>
 </tr>
 <tr class="tutorial2">
 <td>Row 2, cell 1</td>
 <td>Row 2, cell 2</td>
 <td>Row 2, cell 3<img src=http://www.ccc.com/badge3.gif></td>
 </tr>
</table>
</body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# 2a
title = soup.title
print(title)

# 2b
second_li = soup.select('ul li ol li')[1]
print(second_li)

# 2c
second_row = soup.select('table tr.tutorial2 td')
#second_row_text = [cell.text for cell in second_row]
print(second_row)


# 2d
h2_tutorial = soup.find_all('h2')
#h2_tutorial_text = [cell.text for cell in h2_tutorial if 'tutorial' in cell.text.lower()]
print(h2_tutorial)

# 2e
html_cells = soup.find_all(string=re.compile("HTML"))
html_cells_text = [cell.text for cell in html_cells]
print(html_cells)

# 2f
table_row1 = soup.select('table tr:first-child')
print(table_row1)

# 2g
all_images = soup.select('img')
#all_images_src = [cell['src'] for cell in all_images]
print(all_images)