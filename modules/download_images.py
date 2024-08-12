import os
import requests

def download_images(directory='./images'):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    files = [
        'https://cdn.repliers.io/IMG-E7312496_2.jpg?class=large',
        'https://cdn.repliers.io/IMG-W9049857_3.jpg?class=large',
        'https://cdn.repliers.io/IMG-W7299676_19.jpg?class=large',
        'https://cdn.repliers.io/IMG-N9052433_12.jpg?class=large',
        'https://cdn.repliers.io/IMG-N9052433_19.jpg?class=large',
        'https://cdn.repliers.io/IMG-Z8083610_6.jpg?class=large',
        'https://cdn.repliers.io/IMG-W9235941_17.jpg?class=large',
        'https://cdn.repliers.io/IMG-W9018907_11.jpg?class=large',
        'https://cdn.repliers.io/IMG-W9018907_23.jpg?class=large',
        'https://cdn.repliers.io/IMG-W9052988_2.jpg?class=large',
        'https://cdn.repliers.io/IMG-W9052988_5.jpg?class=large',
        'https://cdn.repliers.io/IMG-C9051345_2.jpg?class=large',
        'https://cdn.repliers.io/IMG-W8342790_3.jpg?class=large',


    ]
    
    downloaded_files = []
    
    for url in files:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.join(directory, url.split('/')[-1].split('?')[0])
            with open(file_name, 'wb') as file:
                file.write(response.content)
            downloaded_files.append(file_name)
            print(f'Successfully downloaded {file_name}')
        else:
            print(f'Failed to download {url}')
    
    return downloaded_files