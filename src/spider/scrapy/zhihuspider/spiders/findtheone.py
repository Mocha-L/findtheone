# -*- coding: utf-8 -*-
import scrapy
import re
import json
from zhihuspider.items import ZhihuspiderItem, ZhihuspiderImgItem


class FindtheoneSpider(scrapy.Spider):
    name = 'findtheone'
    allowed_domains = ['zhihu.com']

    def start_requests(self):
        url = 'https://www.zhihu.com/api/v4/questions/275359100/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=20&offset=0&sort_by=default'
        yield scrapy.Request(url=url, callback=self.parse_list)
        url = 'https://www.zhihu.com/question/275359100'
        yield scrapy.Request(url=url, callback=self.parse_problems)

    def parse_problems(self, response):
        urls_json = response.xpath("//script[@id='js-initialData']/text()").extract_first()
        urls_json = json.loads(urls_json)
        urls_json = urls_json.get('initialState', {}).get('entities', {}).get('questions', {}).get('275359100', {}).get('detail', '')
        if urls_json and urls_json.find('镜像问题：') != -1:
            urls_json = urls_json[urls_json.find('镜像问题：'):]  #  href="https://www.zhihu.com/question/309872833"
            urls = re.findall('href="(.*?)"', urls_json)
            for url in urls:
                question_id = url[url.rfind('/')+1:]
                if question_id:
                    url = f'https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=20&offset=0&sort_by=default'
                    yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        resp = json.loads(response.body)

        paging = resp.get('paging')
        if not paging.get('is_end'):
            url = paging.get('next')
            yield scrapy.Request(url=url, callback=self.parse_list)

        data = resp.get('data', [])
        for one in data:
            author = one.get('author', {}).get('name')
            author_avatar = one.get('author', {}).get('avatar_url')
            avatar_save_name = author_avatar[author_avatar.rfind('/') + 1:]

            item = ZhihuspiderImgItem()
            item['image_urls'] = [author_avatar]
            item['images'] = avatar_save_name
            yield item

            author_gender = one.get('author', {}).get('gender')
            author_gender = 2 if author == '匿名用户' else author_gender
            content = one.get('content')
            img_list = re.findall('<figure.*?><noscript><img src="(.*?)" ', content)
            if not img_list:
                img_list = None
            content = re.sub('<figure.*?><noscript><img src="(.*?)</figure>',
                             '<p style="color:#aaa">[这里有一张图片，可以在知乎原答案查看]<p>', content)
            create_time = one.get('created_time')
            update_time = one.get('updated_time')

            item = ZhihuspiderItem()
            item['QuestionId'] = one.get('question', {}).get('id')
            item['QuestionTitle'] = one.get('question', {}).get('title')
            item['AnswerId'] = one.get('id')
            item['AuthorName'] = author
            item['AuthUrlToken'] = one.get('author', {}).get('url_token')
            item['AuthorAvatar'] = avatar_save_name
            item['AuthorGender'] = author_gender
            item['VoteupCount'] = one.get('voteup_count', 0)
            item['CommentCount'] = one.get('comment_count', 0)
            item['ContentImg'] = json.dumps(img_list) if img_list else None
            item['TotalContent'] = content
            item['CreateTime'] = create_time
            item['UpdateTime'] = update_time
            yield item

