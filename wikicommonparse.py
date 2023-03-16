import os

import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class ImgData:
    name: str
    img_url: str

async def download_and_save(url, path, session):
    async with session.get(url) as resp:
        if resp.status == 200:
            print(f'Downloading {url} to {path}...')
            f = await aiofiles.open(path, mode='wb')
            await f.write(await resp.read())
            await f.close()

async def scrape(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                print(f'Parsing {url}...')
                html = await response.text()

                # write html to file
                f = await aiofiles.open('test.html', encoding='utf-8', mode='w')
                await f.write(html)
                await f.close()
        
                soup = BeautifulSoup(html, 'html.parser')

                # print out the title of the page
                print(soup.title.text)
                
                images = []
                images_div = soup.find_all('li', {'class': 'gallerybox'})

                print(f'Found {len(images_div)} images.')

                # print head of images
                for div in images_div[:5]:
                    print(div.find('div', {'class': 'gallerytext'}).find('a').text)

                # count = 0
                for div in images_div:
                    imgs = div.find_all('img')
                    
                    # print imgs status
                    # print(f'Found {len(imgs)} images.')
                    if len(imgs) > 0:
                        img_url = imgs[0]['src']
                        header = div.find('div', {'class': 'gallerytext'})
                        link = header.find('a')
                        title = link.text
                        print(f'Found image: {title} ({img_url})')
                        images.append(ImgData(title, img_url))

                # create images folder if it doesn't exist
                if not os.path.exists('images'):
                    os.makedirs('images')
                
                i = 1
                for image in images:
                    await download_and_save(image.img_url, f'images/{i}.jpg', session)
                    i += 1

async def main():
    await scrape('https://commons.wikimedia.org/wiki/Category:Pictures_of_the_day_(2023)')

if __name__ == '__main__':
    asyncio.run(main())
