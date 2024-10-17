## Полезные заметки

## Обновление url адресов
```SQL
UPDATE media_files
SET youtube_url = 'https://www.youtube.com/watch?v=Gye9-o_W5MY'
and rutube_url = 'https://rutube.ru/video/fb2d5260b86d5eed450627657d7a2938/?r=plwd'
and plvideo_url = 'https://plvideo.ru/'
WHERE id = 9;
```