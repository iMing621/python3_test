import extruct
import requests
import bs4
from w3lib.html import get_base_url

#url="https://gizmodo.com/nine-days-with-an-absurd-9-000-gaming-laptop-1794290421"

#url="https://www.gizmodo.com.au/2018/05/acers-new-swift-5-notebook-weighs-less-than-1kg/"

#url="https://www.goodgearguide.com.au/article/645791/acer-aspire-e15-e5-576-392h-review-bargain-priced-laptop-plenty-productivity-power/"

url="https://www.goodhousekeeping.com/uk/product-reviews/tech/a685384/acer-aspire-3-a315-51/"

headers={}
headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"

payload={}

r = requests.get(url, headers= headers, params=payload)
print(r.status_code)

base_url = get_base_url(r.text, r.url)
print(base_url)

data = extruct.extract(r.text, base_url=base_url, syntaxes=['json-ld'])
#print(data)

# Title
print(data['json-ld'][0]['headline'])

# Author
print(data['json-ld'][0]['author']['name'])

# Site Review Date
print(data['json-ld'][0]['datePublished'])

# Site Review Rating
if 'reviewRating' in data['json-ld'][0]:
  if data['json-ld'][0]['reviewRating']['ratingValue']:
    print(data['json-ld'][0]['reviewRating']['ratingValue'])
else:
  ratingCss="p.body-text strong"

  soupObj=bs4.BeautifulSoup(r.text, 'lxml')
  #print(type(soupObj))

  siteReviewRatingFullText=soupObj.select(ratingCss)
  #print(siteReviewRatingFullText)

  siteReviewRating=siteReviewRatingFullText[0].get_text().split(': ')[1].split('/')[0]
  print(siteReviewRating)

# Site Review ID
siteReviewUrl=data['json-ld'][0]['url'].split('://')[1].split('/')
siteReviewId=siteReviewUrl[4]
print(siteReviewId)

# Pros
ProsCss="div.article-body-content.standard-body-content ul:nth-of-type(2) li"

siteReviewPros=''
reviewPros_ul=soupObj.select(ProsCss)
for li in reviewPros_ul:
  siteReviewPros += li.get_text() + '\n'

print(siteReviewPros)

# Cons
ConsCss="div.article-body-content.standard-body-content ul:nth-of-type(3) li"

siteReviewCons=''
reviewCons_ul=soupObj.select(ConsCss)
for li in reviewCons_ul:
  siteReviewCons += li.get_text() + '\n'

print(siteReviewCons)

# Related Product Link & PRODUCT_SIN
relatedProdCss="div.article-body-content.standard-body-content p.body-text a.body-link"

relatedProductLink=soupObj.select(relatedProdCss)[0]['href']
print(relatedProductLink)

"""
http://www.argos.co.uk/product/7368006?cmpid=GS001&_%24ja=tsid:59130%7Ccid:265006737%7Cagid:14507206137%7Ctid:pla-18283950120%7Ccrid:73382240337%7Cnw:g%7Crnd:5965792410350466151%7Cdvc:c%7Cadp:1o10%7Cmt:%7Cloc:9045899&gclid=Cj0KCQiAnuDTBRDUARIsAL41eDohZs7qBVPMjOI5izBv5dNbQ73-KjG1jlGjRREmozTiGasD7NYajgEaAliCEALw_wcB
"""
if 'argos' in relatedProductLink:
  relatedProductSin=relatedProductLink.split('://')[1].split('?')[0].split('/')[2]
  print(relatedProductSin)
